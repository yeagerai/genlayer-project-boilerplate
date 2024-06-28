execute_icontract_function_response_structure = {
    "id": int,
    "jsonrpc": str,
    "result": {
        "data": {
            "consensus_data": {
                "consensus_data": str,
                "leader_data": {
                    "result": {
                        "args": list,
                        "class": str,
                        "contract_state": str,
                        "eq_outputs": {"leader": dict},
                        "gas_used": int,
                        "method": str,
                        "mode": str,
                        "node_config": {
                            "config": dict,
                            "model": str,
                            "provider": str,
                            "stake": float,
                        },
                    },
                    "vote": str,
                },
            },
            "created_at": str,
            "data": dict,
            "from_address": str,
            "id": int,
            "status": str,
            "type": int,
            "value": float,
        },
        "message": str,
        "status": str,
    },
}
