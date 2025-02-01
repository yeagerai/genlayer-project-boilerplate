from tools.types import Address
import typing
import collections.abc
import dataclasses
import abc
import json

BITS_IN_TYPE = 3

TYPE_SPECIAL = 0
TYPE_PINT = 1
TYPE_NINT = 2
TYPE_BYTES = 3
TYPE_STR = 4
TYPE_ARR = 5
TYPE_MAP = 6

SPECIAL_NULL = (0 << BITS_IN_TYPE) | TYPE_SPECIAL
SPECIAL_FALSE = (1 << BITS_IN_TYPE) | TYPE_SPECIAL
SPECIAL_TRUE = (2 << BITS_IN_TYPE) | TYPE_SPECIAL
SPECIAL_ADDR = (3 << BITS_IN_TYPE) | TYPE_SPECIAL


class CalldataEncodable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __to_calldata__(self) -> typing.Any: ...


def encode(
    x: typing.Any, *, default: typing.Callable[[typing.Any], typing.Any] = lambda x: x
) -> bytes:
    mem = bytearray()

    def append_uleb128(i):
        assert i >= 0
        if i == 0:
            mem.append(0)
        while i > 0:
            cur = i & 0x7F
            i = i >> 7
            if i > 0:
                cur |= 0x80
            mem.append(cur)

    def impl_dict(b: collections.abc.Mapping):
        keys = list(b.keys())
        keys.sort()
        le = len(keys)
        le = (le << 3) | TYPE_MAP
        append_uleb128(le)
        for k in keys:
            if not isinstance(k, str):
                raise Exception(f"key is not string {type(k)}")
            bts = k.encode("utf-8")
            append_uleb128(len(bts))
            mem.extend(bts)
            impl(b[k])

    def impl(b: typing.Any):
        b = default(b)
        if isinstance(b, CalldataEncodable):
            b = b.__to_calldata__()
        if b is None:
            mem.append(SPECIAL_NULL)
        elif b is True:
            mem.append(SPECIAL_TRUE)
        elif b is False:
            mem.append(SPECIAL_FALSE)
        elif isinstance(b, int):
            if b >= 0:
                b = (b << 3) | TYPE_PINT
                append_uleb128(b)
            else:
                b = -b - 1
                b = (b << 3) | TYPE_NINT
                append_uleb128(b)
        elif isinstance(b, Address):
            mem.append(SPECIAL_ADDR)
            mem.extend(b.as_bytes)
        elif isinstance(b, bytes):
            lb = len(b)
            lb = (lb << 3) | TYPE_BYTES
            append_uleb128(lb)
            mem.extend(b)
        elif isinstance(b, str):
            b = b.encode("utf-8")
            lb = len(b)
            lb = (lb << 3) | TYPE_STR
            append_uleb128(lb)
            mem.extend(b)
        elif isinstance(b, collections.abc.Sequence):
            lb = len(b)
            lb = (lb << 3) | TYPE_ARR
            append_uleb128(lb)
            for x in b:
                impl(x)
        elif isinstance(b, collections.abc.Mapping):
            impl_dict(b)
        elif dataclasses.is_dataclass(b):
            assert not isinstance(b, type)
            impl_dict(dataclasses.asdict(b))
        else:
            raise Exception(f"invalid type {type(b)}")

    impl(x)
    return bytes(mem)


def decode(mem0: collections.abc.Buffer) -> typing.Any:
    mem: memoryview = memoryview(mem0)

    def read_uleb128() -> int:
        nonlocal mem
        ret = 0
        off = 0
        while True:
            m = mem[0]
            ret = ret | ((m & 0x7F) << off)
            off += 7
            mem = mem[1:]
            if (m & 0x80) == 0:
                break
        return ret

    def impl() -> typing.Any:
        nonlocal mem
        code = read_uleb128()
        typ = code & 0x7
        if typ == TYPE_SPECIAL:
            if code == SPECIAL_NULL:
                return None
            if code == SPECIAL_FALSE:
                return False
            if code == SPECIAL_TRUE:
                return True
            if code == SPECIAL_ADDR:
                ret_addr = mem[: Address.SIZE]
                mem = mem[Address.SIZE :]
                return Address(ret_addr)
            raise Exception(f"Unknown special {bin(code)} {hex(code)}")
        code = code >> 3
        if typ == TYPE_PINT:
            return code
        elif typ == TYPE_NINT:
            return -code - 1
        elif typ == TYPE_BYTES:
            ret_bytes = mem[:code]
            mem = mem[code:]
            return ret_bytes
        elif typ == TYPE_STR:
            ret_str = mem[:code]
            mem = mem[code:]
            return str(ret_str, encoding="utf-8")
        elif typ == TYPE_ARR:
            ret_arr = []
            for _i in range(code):
                ret_arr.append(impl())
            return ret_arr
        elif typ == TYPE_MAP:
            ret_dict: dict[str, typing.Any] = {}
            prev = None
            for _i in range(code):
                le = read_uleb128()
                key = str(mem[:le], encoding="utf-8")
                mem = mem[le:]
                if prev is not None:
                    assert prev < key
                prev = key
                assert key not in ret_dict
                ret_dict[key] = impl()
            return ret_dict
        raise Exception(f"invalid type {typ}")

    res = impl()
    if len(mem) != 0:
        raise Exception(f"unparsed end {bytes(mem[:5])!r}... (decoded {res})")
    return res


def to_str(d: typing.Any) -> str:
    buf: list[str] = []

    def impl(d: typing.Any) -> None:
        if d is None:
            buf.append("null")
        elif d is True:
            buf.append("true")
        elif d is False:
            buf.append("false")
        elif isinstance(d, str):
            buf.append(json.dumps(d))
        elif isinstance(d, bytes):
            buf.append("b#")
            buf.append(d.hex())
        elif isinstance(d, int):
            buf.append(str(d))
        elif isinstance(d, Address):
            buf.append("addr#")
            buf.append(d.as_bytes.hex())
        elif isinstance(d, dict):
            buf.append("{")
            comma = False
            for k, v in d.items():
                if comma:
                    buf.append(",")
                comma = True
                buf.append(json.dumps(k))
                buf.append(":")
                impl(v)
            buf.append("}")
        elif isinstance(d, list):
            buf.append("[")
            comma = False
            for v in d:
                if comma:
                    buf.append(",")
                comma = True
                impl(v)
            buf.append("]")
        else:
            raise Exception(f"can't encode {d} to calldata")

    impl(d)
    return "".join(buf)
