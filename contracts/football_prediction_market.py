# { "Depends": "py-genlayer:test" }

import json
from dataclasses import dataclass
from genlayer import *


@dataclass
class Prediction:
    id: str
    has_resolved: bool
    game_date: str
    resolution_url: str
    team1: str
    team2: str
    predicted_winner: str
    real_winner: str
    real_score: str


@gl.contract
class FootballPredictionMarket:
    predictions: TreeMap[Address, TreeMap[str, Prediction]]
    points: TreeMap[Address, u256]

    def __init__(self):
        pass

    def _check_match(self, resolution_url: str, team1: str, team2: str) -> dict:
        def get_match_result() -> str:
            web_data = gl.get_webpage(resolution_url, mode="text")
            print(web_data)

            task = f"""
In the following web page, find the winning team in a matchup between the following teams:
Team 1: {team1}
Team 2: {team2}

Web page content:
{web_data}
End of web page data.

If it says "Kick off [time]" between the names of the two teams, it means the game hasn't started yet.
If you fail to extract the score, assume the game is not resolved yet.

Respond with the following JSON format:
{{
    "score": str, // The score with numbers only, e.g, "1:2", or "-" if the game is not resolved yet
    "winner": int, // The number of the winning team, 0 for draw, or -1 if the game is not yet finished
}}
It is mandatory that you respond only using the JSON format above,
nothing else. Don't include any other words or characters,
your output must be only JSON without any formatting prefix or suffix.
This result should be perfectly parsable by a JSON parser without errors.
            """
            result = gl.exec_prompt(task).replace("```json", "").replace("```", "")
            print(result)
            return json.dumps(json.loads(result), sort_keys=True)

        result_json = json.loads(gl.eq_principle_strict_eq(get_match_result))
        return result_json

    @gl.public.write
    def create_prediction(
        self, game_date: str, team1: str, team2: str, predicted_winner: str
    ) -> None:
        """
        Initializes a new bet with the specified game date and teams.

        Args:
            game_date (str): The date of the game in the format 'YYYY-MM-DD'.
            team1 (str): The name of the first team.
            team2 (str): The name of the second team.

        Attributes:
            has_resolved (bool): Indicates whether the game's resolution has been processed. Default is False.
            game_date (str): The date of the game.
            resolution_url (str): The URL to the game's resolution on BBC Sport.
            team1 (str): The name of the first team.
            team2 (str): The name of the second team.
        """
        match_resolution_url = (
            "https://www.bbc.com/sport/football/scores-fixtures/" + game_date
        )
        # commented to allow to test matches in the past.
        # match_status = await self._check_match(match_resolution_url, team1, team2)

        # if int(match_status["winner"]) > -1:
        #    raise Exception("Game already finished")

        sender_address = gl.message.sender_account

        prediction_id = f"{game_date}_{team1}_{team2}".lower()
        if (
            sender_address in self.predictions
            and prediction_id in self.predictions[sender_address]
        ):
            raise Exception("Prediction already created")

        prediction = Prediction(
            id=prediction_id,
            has_resolved=False,
            game_date=game_date,
            resolution_url=match_resolution_url,
            team1=team1,
            team2=team2,
            predicted_winner=predicted_winner,
            real_winner="",
            real_score="",
        )
        self.predictions.get_or_insert_default(sender_address)[
            prediction_id
        ] = prediction

    @gl.public.write
    def resolve_prediction(self, prediction_id: str) -> None:
        if not prediction_id in self.predictions[gl.message.sender_account]:
            raise Exception("Prediction not found")

        if self.predictions[gl.message.sender_account][prediction_id].has_resolved:
            raise Exception("Prediction already resolved")

        prediction = self.predictions[gl.message.sender_account][prediction_id]
        prediction_status = self._check_match(
            prediction.resolution_url, prediction.team1, prediction.team2
        )

        if int(prediction_status["winner"]) < 0:
            raise Exception("Game not finished")

        prediction.has_resolved = True
        prediction.real_winner = str(prediction_status["winner"])
        prediction.real_score = prediction_status["score"]

        if prediction.real_winner == prediction.predicted_winner:
            if gl.message.sender_account not in self.points:
                self.points[gl.message.sender_account] = 0
            self.points[gl.message.sender_account] += 1

    @gl.public.view
    def get_predictions(self) -> dict:
        return {k.as_hex: v for k, v in self.predictions.items()}

    @gl.public.view
    def get_player_predictions(self, player_address: str) -> dict:
        if not player_address in self.predictions:
            return {}
        return self.predictions[Address(player_address)]

    @gl.public.view
    def get_points(self) -> dict:
        return self.points

    @gl.public.view
    def get_player_points(self, player_address: str) -> int:
        if player_address not in self.points:
            return 0
        return self.points[Address(player_address)]
