# tests/common/request.py
import os
import json
import requests
import time
from dotenv import load_dotenv
from eth_account import Account
import base64

from tools.transactions import sign_transaction, encode_transaction_data

import tools.calldata as calldata

load_dotenv()


def payload(function_name: str, *args) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": function_name,
        "params": [*args],
        "id": 1,
    }


def post_request(
    payload: dict,
    protocol: str = os.environ["RPCPROTOCOL"],
    host: str = os.environ["RPCHOST"],
    port: str = os.environ["RPCPORT"],
):
    return requests.post(
        protocol + "://" + host + ":" + port + "/api",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )


def get_transaction_by_hash(transaction_hash: str):
    payload_data = payload("eth_getTransactionByHash", transaction_hash)
    raw_response = post_request(payload_data)
    parsed_raw_response = raw_response.json()
    return parsed_raw_response["result"]


def get_transaction_count(account_address: str):
    payload_data = payload("eth_getTransactionCount", account_address)
    raw_response = post_request(payload_data)
    parsed_raw_response = raw_response.json()
    return parsed_raw_response["result"]


def call_contract_method(
    contract_address: str,
    from_account: Account,
    method_name: str,
    method_args: list,
):
    encoded_data = encode_transaction_data(
        [calldata.encode({"method": method_name, "args": method_args})]
    )
    method_response = post_request(
        payload(
            "eth_call",
            {
                "to": contract_address,
                "from": from_account.address,
                "data": encoded_data,
            },
        )
    ).json()
    print("method_response", method_response)
    enc_result = method_response["result"]
    return calldata.decode(base64.b64decode(enc_result))


def send_transaction(
    account: Account,
    contract_address: str,
    method_name: str | None,
    method_args: list | None,
    value: int = 0,
):
    call_data = (
        None
        if method_name is None and method_args is None
        else [calldata.encode({"method": method_name, "args": method_args})]
    )
    nonce = get_transaction_count(account.address)
    signed_transaction = sign_transaction(
        account, call_data, contract_address, value, nonce
    )
    return send_raw_transaction(signed_transaction)


def deploy_intelligent_contract(
    account: Account, contract_code: str, method_args: list
) -> tuple[str, dict]:
    nonce = get_transaction_count(account.address)
    deploy_data = [
        contract_code,
        calldata.encode({"method": "__init__", "args": method_args}),
    ]
    signed_transaction = sign_transaction(account, deploy_data, nonce=nonce)
    result = send_raw_transaction(signed_transaction)
    contract_address = result["data"]["contract_address"]
    return contract_address, result


def send_raw_transaction(signed_transaction: str):
    payload_data = payload("eth_sendRawTransaction", signed_transaction)
    raw_response = post_request(payload_data)
    call_method_response = raw_response.json()
    print("call_method_response", call_method_response)
    transaction_hash = call_method_response["result"]

    transaction_response = wait_for_transaction(transaction_hash)
    return transaction_response


def wait_for_transaction(transaction_hash: str, interval: int = 10, retries: int = 15):
    attempts = 0
    while attempts < retries:
        transaction_response = get_transaction_by_hash(str(transaction_hash))
        print("transaction_response", transaction_response)
        status = transaction_response["status"]
        if status == "FINALIZED":
            return transaction_response
        time.sleep(interval)
        attempts += 1

    raise TimeoutError(
        f"Transaction {transaction_hash} not finalized after {retries} retries"
    )
