import os

from dotenv import load_dotenv

load_dotenv()


def get_config() -> dict:
    config = {
        "rpc_protocol": os.environ["RPCPROTOCOL"],
        "rpc_host": os.environ["RPCHOST"],
        "rpc_port": os.environ["RPCPORT"],
    }
    return config
