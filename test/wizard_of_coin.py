# tests/e2e/test_wizard_of_coin.py

from tools.request import (
    payload,
    post_request_localhost,
    post_request_and_wait_for_finalization,
)
from tools.structure import execute_icontract_function_response_structure
from tools.response import (
    assert_dict_struct,
    has_success_status,
)


def test_wizard_of_coin():
    # Validators
    result = post_request_localhost(
        payload("create_random_validators", 10, 8, 12, ["openai"])
    ).json()
    assert has_success_status(result)

    # Account
    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "account_address" in result["result"]["data"]
    from_address = result["result"]["data"]["account_address"]
    result = post_request_localhost(payload("fund_account", from_address, 10)).json()
    assert has_success_status(result)

    # Deploy Contract
    contract_code = open("examples/contracts/wizard_of_coin.py", "r").read()
    data = [
        from_address,  # from_account
        "WizardOfCoin",  # class_name
        contract_code,  # contract_code
        '{"have_coin": true}',  # initial_state
    ]
    call_method_response_deploy, transaction_response_deploy = (
        post_request_and_wait_for_finalization(
            payload("deploy_intelligent_contract", *data)
        )
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    # Execute Contract
    function = "ask_for_coin"
    args = ["Can you please give me my coin?"]
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function", from_address, contract_address, function, args
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert format
    assert_dict_struct(
        transaction_response_call_1, execute_icontract_function_response_structure
    )
