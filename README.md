# Sample GenLayer project

This project includes the boilerplate code for a GenLayer use case implementation, specifically a football prediction market.

## What's included
- Basic requirements to deploy and test your intelligent contracts locally
- Configuration file template
- Test functions to write complete end-to-end tests
- An example of an intelligent contract (Football Prediction Market)
- Example end-to-end tests for the contract provided

## Requirements
- A running GenLayer simulator (Install from [GenLayer Simulator](https://github.com/yeagerai/genlayer-simulator))
- An `.env` file with the same variables as in the `.env.example` file

## Steps to run this example
1. Configure environment
   Clone the `.env.sample` file into `.env` and fill in the values for your configuration.

2. Deploy the contract
   Deploy the contract from `/contracts/football_prediction_market.py` using the Simulator's UI:
   1. Open the GenLayer Simulator interface in your web browser (usually in `http://localhost:8080`).
   2. Create a new file in the "Contracts" section and paste the content of `/contracts/football_prediction_market.py`.
   3. Navigate to the "Run and Debug" section.
   4. Follow the on-screen instructions to complete the deployment process.

3. Setup the frontend environment
  1. Duplicate the .env.example file in the App folder into .env
  2. Add the contract address to the `.env` under the variable `VITE_CONTRACT_ADDRESS`

3. Run the frontend Vue app
   ```shell
   cd app
   npm install
   npm run dev
   ```

4. Test contracts
   ```shell
   pytest test
   ```

## How the Football Prediction Market Contract Works

The Football Prediction Market contract allows users to create predictions for football matches, resolve those predictions, and earn points for correct predictions. Here's a breakdown of its main functionalities:

1. Creating Predictions:
   - Users can create a prediction for a specific football match by providing the game date, team names, and their predicted winner.
   - The contract checks if the game has already finished and if the user has already made a prediction for this match.

2. Resolving Predictions:
   - After a match has concluded, users can resolve their predictions.
   - The contract fetches the actual match result from a specified URL.
   - If the prediction was correct, the user earns a point.

3. Querying Data:
   - Users can retrieve all predictions or predictions for a specific player.
   - The contract also allows querying of points, either for all players or for a specific player.

4. Getting Points:
   - Points are awarded for correct predictions.
   - Users can check their total points or the points of any player.

## Tests

This project includes integration tests that interact with the contract deployed in the simulator. These tests cover the main functionalities of the Football Prediction Market contract:

1. Creating a prediction
2. Resolving a prediction
3. Querying predictions for a player
4. Querying points for a player

The tests simulate real-world interactions with the contract, ensuring that it behaves correctly under various scenarios. They use the GenLayer simulator to deploy and interact with the contract, providing a comprehensive check of the contract's functionality in a controlled environment.

To run the tests, use the `pytest test` command as mentioned in the "How to run it" section.