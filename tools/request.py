# tests/common/request.py
import os
import json
import requests
import time

from config.genlayer_config import get_config

config = get_config()


def payload(function_name: str, *args) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": function_name,
        "params": [*args],
        "id": 1,
    }


def post_request(
    payload: dict,
    protocol: str = config["rpc_protocol"],
    host: str = config["rpc_host"],
    port: str = config["rpc_port"],
):
    return requests.post(
        protocol + "://" + host + ":" + port + "/api",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )


def post_request_localhost(payload: dict):
    return post_request(payload, "http", "localhost")


def get_transaction_by_id(transaction_id: str):
    payload_data = payload("get_transaction_by_id", transaction_id)
    raw_response = post_request_localhost(payload_data)
    return raw_response.json()


def post_request_and_wait_for_finalization(
    payload: dict, interval: int = 5, retries: int = 15
):
    raw_response = post_request_localhost(payload)
    call_method_response = raw_response.json()
    if not call_method_response["result"]:
        raise ValueError("No result found in the call_method_response")
    transaction_id = call_method_response["result"]["data"]["transaction_id"]

    attempts = 0
    while attempts < retries:
        transaction_response = get_transaction_by_id(str(transaction_id))
        print("status_response", transaction_response)
        status = transaction_response["result"]["data"]["status"]
        if status == "FINALIZED":
            return (call_method_response, transaction_response)
        time.sleep(interval)
        attempts += 1

    raise TimeoutError(
        f"Transaction {transaction_id} not finalized after {retries} retries"
    )
