football_prediction_market_contract_schema = {
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "abi": [
            {"inputs": [], "type": "constructor"},
            {
                "inputs": [
                    {"name": "resolution_url", "type": "string"},
                    {"name": "team1", "type": "string"},
                    {"name": "team2", "type": "string"},
                ],
                "name": "_check_match",
                "outputs": [{"name": "", "type": "bytes"}],
                "type": "function",
            },
            {
                "inputs": [
                    {"name": "game_date", "type": "string"},
                    {"name": "team1", "type": "string"},
                    {"name": "team2", "type": "string"},
                    {"name": "predicted_winner", "type": "string"},
                ],
                "name": "create_prediction",
                "outputs": [],
                "type": "function",
            },
            {
                "inputs": [{"name": "player_address", "type": "string"}],
                "name": "get_player_points",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function",
            },
            {
                "inputs": [{"name": "player_address", "type": "string"}],
                "name": "get_player_predictions",
                "outputs": [{"name": "", "type": "bytes"}],
                "type": "function",
            },
            {
                "inputs": [],
                "name": "get_points",
                "outputs": [{"name": "", "type": "bytes"}],
                "type": "function",
            },
            {
                "inputs": [],
                "name": "get_predictions",
                "outputs": [{"name": "", "type": "bytes"}],
                "type": "function",
            },
            {
                "inputs": [{"name": "prediction_id", "type": "string"}],
                "name": "resolve_prediction",
                "outputs": [],
                "type": "function",
            },
        ],
        "class": "FootballPredictionMarket",
    },
}


test_football_prediction_market_predictions_win_unresolved = {
    "2024-06-20_spain_italy": {
        "game_date": "2024-06-20",
        "has_resolved": False,
        "id": "2024-06-20_spain_italy",
        "predicted_winner": "1",
        "real_score": None,
        "real_winner": None,
        "resolution_url": "https://www.bbc.com/sport/football/scores-fixtures/2024-06-20",
        "team1": "Spain",
        "team2": "Italy",
    }
}

test_football_prediction_market_predictions_win_resolved = {
    "2024-06-20_spain_italy": {
        "game_date": "2024-06-20",
        "has_resolved": True,
        "id": "2024-06-20_spain_italy",
        "predicted_winner": "1",
        "real_score": "1:0",
        "real_winner": "1",
        "resolution_url": "https://www.bbc.com/sport/football/scores-fixtures/2024-06-20",
        "team1": "Spain",
        "team2": "Italy",
    }
}

test_football_prediction_market_predictions_draw_unresolved = {
    "2024-06-20_denmark_england": {
        "game_date": "2024-06-20",
        "has_resolved": False,
        "id": "2024-06-20_denmark_england",
        "predicted_winner": "0",
        "real_score": None,
        "real_winner": None,
        "resolution_url": "https://www.bbc.com/sport/football/scores-fixtures/2024-06-20",
        "team1": "Denmark",
        "team2": "England",
    }
}

test_football_prediction_market_predictions_draw_resolved = {
    "2024-06-20_denmark_england": {
        "game_date": "2024-06-20",
        "has_resolved": True,
        "id": "2024-06-20_denmark_england",
        "predicted_winner": "0",
        "real_score": "1:1",
        "real_winner": "0",
        "resolution_url": "https://www.bbc.com/sport/football/scores-fixtures/2024-06-20",
        "team1": "Denmark",
        "team2": "England",
    }
}

test_football_prediction_market_predictions_unsuccess_unresolved = {
    "2024-06-20_spain_italy": {
        "game_date": "2024-06-20",
        "has_resolved": False,
        "id": "2024-06-20_spain_italy",
        "predicted_winner": "2",
        "real_score": None,
        "real_winner": None,
        "resolution_url": "https://www.bbc.com/sport/football/scores-fixtures/2024-06-20",
        "team1": "Spain",
        "team2": "Italy",
    }
}

test_football_prediction_market_predictions_unsuccess_resolved = {
    "2024-06-20_spain_italy": {
        "game_date": "2024-06-20",
        "has_resolved": True,
        "id": "2024-06-20_spain_italy",
        "predicted_winner": "2",
        "real_score": "1:0",
        "real_winner": "1",
        "resolution_url": "https://www.bbc.com/sport/football/scores-fixtures/2024-06-20",
        "team1": "Spain",
        "team2": "Italy",
    }
}
