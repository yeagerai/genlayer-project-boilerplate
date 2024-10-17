import json
from backend.node.genvm.icontract import IContract
from backend.node.genvm.equivalence_principle import EquivalencePrinciple


class FootballPredictionMarket(IContract):
    def __init__(self):
        self.predictions = {}
        self.points = {}

    async def _check_match(self, resolution_url: str, team1: str, team2: str) -> dict:
        final_result = {}
        async with EquivalencePrinciple(
            result=final_result,
            principle="The score and the winner has to be exactly the same",
            comparative=True,
        ) as eq:
            web_data = await eq.get_webpage(url=resolution_url)
            task = f"""In the following web page, find the winning team in a football matchup between the following teams:
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
            It is mandatory that you respond only using the JSON above,
            nothing else. Don't include any other words or characters,
            your output must be only JSON without any formatting prefix or suffix.
            This result should be perfectly parseable by a JSON parser without errors.

            Given than <answer> is the JSON object response with score and winner, here are examples about how you shouldn't answer:
            - ```json <answer> ```
            - the anwer is <answer>

            How you should answer: 
            <answer>

            """
            result = await eq.call_llm(task)
            eq.set(result)

        return json.loads(
            final_result["output"].replace("```json", "").replace("```", "")
        )

    async def create_prediction(
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
        # match_status = await self._check_match(match_resolution_url, team1, team2)

        # if int(match_status["winner"]) > -1:
        #    raise Exception("Game already finished")

        if not contract_runner.from_address in self.predictions:
            self.predictions[contract_runner.from_address] = {}

        prediction_id = f"{game_date}_{team1}_{team2}".lower()
        if prediction_id in self.predictions[contract_runner.from_address]:
            raise Exception("Prediction already created")

        prediction = {
            "id": prediction_id,
            "has_resolved": False,
            "game_date": game_date,
            "resolution_url": match_resolution_url,
            "team1": team1,
            "team2": team2,
            "predicted_winner": predicted_winner,
            "real_winner": None,
            "real_score": None,
        }
        self.predictions[contract_runner.from_address][prediction_id] = prediction

    async def resolve_prediction(self, prediction_id: str) -> None:
        if not prediction_id in self.predictions[contract_runner.from_address]:
            raise Exception("Prediction not found")

        if self.predictions[contract_runner.from_address][prediction_id][
            "has_resolved"
        ]:
            raise Exception("Prediction already resolved")

        prediction = self.predictions[contract_runner.from_address][prediction_id]
        prediction_status = await self._check_match(
            prediction["resolution_url"], prediction["team1"], prediction["team2"]
        )

        if int(prediction_status["winner"]) < 0:
            raise Exception("Game not finished")

        prediction["has_resolved"] = True
        prediction["real_winner"] = str(prediction_status["winner"])
        prediction["real_score"] = prediction_status["score"]

        if prediction["real_winner"] == prediction["predicted_winner"]:
            if contract_runner.from_address not in self.points:
                self.points[contract_runner.from_address] = 0
            self.points[contract_runner.from_address] += 1

    def get_predictions(self) -> dict:
        return self.predictions

    def get_player_predictions(self, player_address: str) -> dict:
        if player_address not in self.predictions:
            return {}
        return self.predictions[player_address]

    def get_points(self) -> dict:
        return self.points

    def get_player_points(self, player_address: str) -> int:
        if player_address not in self.points:
            return 0
        return self.points[player_address]
