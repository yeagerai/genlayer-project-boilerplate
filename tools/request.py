# tests/common/request.py
import os
import json
import requests
import time
from dotenv import load_dotenv
from eth_account import Account

from tools.transactions import sign_transaction, encode_transaction_data

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


def post_request_localhost(payload: dict):
    return post_request(payload, "http", "localhost")


def get_transaction_by_hash(transaction_hash: str):
    payload_data = payload("eth_getTransactionByHash", transaction_hash)
    raw_response = post_request_localhost(payload_data)
    parsed_raw_response = raw_response.json()
    return parsed_raw_response["result"]


def call_contract_method(
    contract_address: str,
    from_account: Account,
    method_name: str,
    method_args: list,
):
    params_as_string = json.dumps(method_args)
    encoded_data = encode_transaction_data([method_name, params_as_string])
    method_response = post_request_localhost(
        payload(
            "eth_call",
            {
                "to": contract_address,
                "from": from_account.address,
                "data": encoded_data,
            },
        )
    ).json()
    return method_response["result"]


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
        else [method_name, json.dumps(method_args)]
    )
    signed_transaction = sign_transaction(account, call_data, contract_address, value)
    return send_raw_transaction(signed_transaction)


def deploy_intelligent_contract(
    account: Account, contract_code: str, constructor_params: str
) -> tuple[str, dict]:
    deploy_data = [contract_code, constructor_params]
    signed_transaction = sign_transaction(account, deploy_data)
    result = send_raw_transaction(signed_transaction)
    contract_address = result["data"]["contract_address"]
    return contract_address, result


def send_raw_transaction(signed_transaction: str):
    payload_data = payload("eth_sendRawTransaction", signed_transaction)
    raw_response = post_request_localhost(payload_data)
    call_method_response = raw_response.json()
    transaction_hash = call_method_response["result"]

    transaction_response = wait_for_transaction(transaction_hash)
    return transaction_response


def wait_for_transaction(transaction_hash: str, interval: int = 10, retries: int = 15):
    attempts = 0
    while attempts < retries:
        transaction_response = get_transaction_by_hash(str(transaction_hash))
        status = transaction_response["status"]
        if status == "FINALIZED":
            return transaction_response
        time.sleep(interval)
        attempts += 1

    raise TimeoutError(
        f"Transaction {transaction_hash} not finalized after {retries} retries"
    )
