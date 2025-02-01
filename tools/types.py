from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional
import base64

import collections.abc

from eth_hash.auto import keccak


class Address:
    SIZE = 20

    __slots__ = ("_as_bytes", "_as_hex")

    _as_bytes: bytes
    _as_hex: str | None

    def __init__(self, val: str | collections.abc.Buffer):
        self._as_hex = None
        if isinstance(val, str):
            if len(val) == 2 + Address.SIZE * 2 and val.startswith("0x"):
                val = bytes.fromhex(val[2:])
            elif len(val) > Address.SIZE:
                val = base64.b64decode(val)
        else:
            val = bytes(val)
        if not isinstance(val, bytes) or len(val) != Address.SIZE:
            raise Exception(f"invalid address {val}")
        self._as_bytes = val

    @property
    def as_bytes(self) -> bytes:
        return self._as_bytes

    @property
    def as_hex(self) -> str:
        if self._as_hex is None:
            simple = self._as_bytes.hex()
            low_up = keccak(simple.encode("ascii")).hex()
            res = ["0", "x"]
            for i in range(len(simple)):
                if low_up[i] in ["0", "1", "2", "3", "4", "5", "6", "7"]:
                    res.append(simple[i])
                else:
                    res.append(simple[i].upper())
            self._as_hex = "".join(res)
        return self._as_hex

    @property
    def as_b64(self) -> str:
        return str(base64.b64encode(self.as_bytes), encoding="ascii")

    @property
    def as_int(self) -> int:
        return int.from_bytes(self._as_bytes, "little", signed=False)

    def __hash__(self):
        return hash(self._as_bytes)

    def __lt__(self, r):
        assert isinstance(r, Address)
        return self._as_bytes < r._as_bytes

    def __le__(self, r):
        assert isinstance(r, Address)
        return self._as_bytes <= r._as_bytes

    def __eq__(self, r):
        if not isinstance(r, Address):
            return False
        return self._as_bytes == r._as_bytes

    def __ge__(self, r):
        assert isinstance(r, Address)
        return self._as_bytes >= r._as_bytes

    def __gt__(self, r):
        assert isinstance(r, Address)
        return self._as_bytes > r._as_bytes

    def __repr__(self) -> str:
        return "addr#" + "".join(["{:02x}".format(x) for x in self._as_bytes])


class Vote(Enum):
    AGREE = "agree"
    DISAGREE = "disagree"

    @classmethod
    def from_string(cls, value: str) -> "Vote":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid vote value: {value}")


class ExecutionMode(Enum):
    LEADER = "leader"
    VALIDATOR = "validator"

    @classmethod
    def from_string(cls, value: str) -> "ExecutionMode":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid execution mode value: {value}")


class ExecutionResultStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    @classmethod
    def from_string(cls, value: str) -> "ExecutionResultStatus":
        try:
            return cls(value.upper())
        except ValueError:
            raise ValueError(f"Invalid execution result status value: {value}")


@dataclass
class PendingTransaction:
    address: str  # Address of the contract to call
    calldata: bytes
    code: bytes | None
    salt_nonce: int

    def is_deploy(self) -> bool:
        return self.code is not None

    def to_dict(self):
        if self.code is None:
            return {
                "address": self.address,
                "calldata": str(base64.b64encode(self.calldata), encoding="ascii"),
            }
        else:
            return {
                "code": str(base64.b64encode(self.code), encoding="ascii"),
                "calldata": str(base64.b64encode(self.calldata), encoding="ascii"),
                "salt_nonce": self.salt_nonce,
            }

    @classmethod
    def from_dict(cls, input: dict) -> "PendingTransaction":
        if "code" in input:
            return cls(
                address="0x",
                calldata=base64.b64decode(input["calldata"]),
                code=base64.b64decode(input["code"]),
                salt_nonce=input.get("salt_nonce", 0),
            )
        else:
            return cls(
                address=input["address"],
                calldata=base64.b64decode(input["calldata"]),
                code=None,
                salt_nonce=0,
            )


@dataclass
class Receipt:
    result: bytes
    calldata: bytes
    gas_used: int
    mode: ExecutionMode
    contract_state: dict[str, dict[str, str]]
    node_config: dict
    eq_outputs: dict[int, str]
    execution_result: ExecutionResultStatus
    vote: Optional[Vote] = None
    pending_transactions: Iterable[PendingTransaction] = ()

    def to_dict(self):
        return {
            "vote": self.vote.value,
            "execution_result": self.execution_result.value,
            "result": base64.b64encode(self.result).decode("ascii"),
            "calldata": str(base64.b64encode(self.calldata), encoding="ascii"),
            "gas_used": self.gas_used,
            "mode": self.mode.value,
            "contract_state": self.contract_state,
            "node_config": self.node_config,
            "eq_outputs": self.eq_outputs,
            "pending_transactions": [
                pending_transaction.to_dict()
                for pending_transaction in self.pending_transactions
            ],
        }

    @classmethod
    def from_dict(cls, input: dict) -> Optional["Receipt"]:
        if input:
            return cls(
                vote=Vote.from_string(input.get("vote")),
                execution_result=ExecutionResultStatus.from_string(
                    input.get("execution_result")
                ),
                result=base64.b64decode(input.get("result")),
                calldata=base64.b64decode(input.get("calldata")),
                gas_used=input.get("gas_used"),
                mode=ExecutionMode.from_string(input.get("mode")),
                contract_state=input.get("contract_state"),
                node_config=input.get("node_config"),
                eq_outputs={int(k): v for k, v in input.get("eq_outputs", {}).items()},
                pending_transactions=[
                    PendingTransaction.from_dict(pending_transaction)
                    for pending_transaction in input.get("pending_transactions", [])
                ],
            )
        else:
            return None
