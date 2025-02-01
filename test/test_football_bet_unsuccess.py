# tests/e2e/test_wizard_of_coin.py

from tools.accounts import create_new_account
from tools.request import (
    deploy_intelligent_contract,
    send_transaction,
    call_contract_method,
    payload,
    post_request,
)
from tools.structure import execute_icontract_function_response_structure
from tools.response import (
    assert_dict_struct,
    assert_dict_exact,
    has_success_status,
)
from test.football_bets_get_contract_schema_for_code import (
    football_bets_contract_schema,
    test_football_bets_unsuccess_unresolved,
    test_football_bets_unsuccess_resolved,
)


def test_football_bets_unsuccess():
    # Account
    account_1 = create_new_account()
    # Validators - not needed for studio.genlayer.com
    # result = post_request(
    #     payload("sim_createRandomValidators", 5, 8, 12, ["openai"], ["gpt-4o"])
    # ).json()
    # assert has_success_status(result)

    # Contract Schema
    contract_code = open("contracts/football_bet_market.py", "r").read()
    result_schema = post_request(
        payload("gen_getContractSchemaForCode", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_exact(result_schema, football_bets_contract_schema)

    # Contract Deploy
    contract_address, transaction_response_deploy = deploy_intelligent_contract(
        account_1,
        contract_code,
        "{}",
    )
    assert has_success_status(transaction_response_deploy)

    # Get Initial State
    contract_all_points_state = call_contract_method(
        contract_address, account_1, "get_points", []
    )
    assert contract_all_points_state == {}

    contract_all_bets_state = call_contract_method(
        contract_address, account_1, "get_bets", []
    )
    assert contract_all_bets_state == {}

    # Create Successful Bet
    create_successful_bet_result = send_transaction(
        account_1,
        contract_address,
        "create_bet",
        ["2024-06-20", "Spain", "Italy", "2"],
    )
    assert has_success_status(create_successful_bet_result)
    assert_dict_struct(
        create_successful_bet_result,
        execute_icontract_function_response_structure,
    )

    # Get Bets
    get_bet_result = call_contract_method(contract_address, account_1, "get_bets", [])
    assert get_bet_result == {
        account_1.address: test_football_bets_unsuccess_unresolved
    }

    # Resolve Successful Bet
    resolve_successful_bet_result = send_transaction(
        account_1, contract_address, "resolve_bet", ["2024-06-20_spain_italy"]
    )
    assert has_success_status(resolve_successful_bet_result)
    assert_dict_struct(
        resolve_successful_bet_result,
        execute_icontract_function_response_structure,
    )

    # Get Bets
    get_bet_result = call_contract_method(contract_address, account_1, "get_bets", [])
    assert get_bet_result == {account_1.address: test_football_bets_unsuccess_resolved}

    # Get Points
    get_points_result = call_contract_method(
        contract_address, account_1, "get_points", []
    )
    assert get_points_result == {}

    # Get Player Points
    get_player_points_result = call_contract_method(
        contract_address, account_1, "get_player_points", [account_1.address]
    )
    assert get_player_points_result == 0

    # Delete Validators - not needed for studio.genlayer.com
    # delete_validators_result = post_request(payload("sim_deleteAllValidators")).json()
    # assert has_success_status(delete_validators_result)
