# Sample GenLayer project
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)
[![Discord](https://dcbadge.vercel.app/api/server/8Jm4v89VAu?compact=true&style=flat)](https://discord.gg/8Jm4v89VAu)
[![Telegram](https://img.shields.io/badge/Telegram--T.svg?style=social&logo=telegram)](https://t.me/genlayer)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/yeagerai.svg?style=social&label=Follow%20%40GenLayer)](https://x.com/GenLayer)
[![GitHub star chart](https://img.shields.io/github/stars/yeagerai/genlayer-project-boilerplate?style=social)](https://star-history.com/#yeagerai/genlayer-js)

## 👀 About
This project includes the boilerplate code for a GenLayer use case implementation, specifically a football prediction market.

## 📦 What's included
- Basic requirements to deploy and test your intelligent contracts locally
- Configuration file template
- Test functions to write complete end-to-end tests
- An example of an intelligent contract (Football Prediction Market)
- Example end-to-end tests for the contract provided

## 🛠️ Requirements
- A running GenLayer simulator (Install from [GenLayer Simulator](https://github.com/yeagerai/genlayer-simulator)). This repository code does not need to be located in the same directory as the Genlayer Simulator.

## 🚀 Steps to run this example

### 1. Configure environment
   Rename the `.env.example` file to `.env`, then fill in the values for your configuration.

### 2. Deploy the contract
   Deploy the contract from `/contracts/football_prediction_market.py` using the Simulator's UI:
   1. Open the GenLayer Simulator interface in your web browser (usually at http://localhost:8080).
   2. Create a new file in the "Contracts" section and paste the content of `/contracts/football_prediction_market.py` (the content is different than the existing contract from the examples).
   3. Navigate to the "Run and Debug" section.
   4. Follow the on-screen instructions to complete the deployment process.

### 3. Setup the frontend environment
  1. All the content of the dApp is located in the `/app` folder.
  2. Rename the `.env.example` file in the `/app` folder to `.env`.
  3. Add the deployed contract address to the `/app/.env` under the variable `VITE_CONTRACT_ADDRESS`

### 4. Run the frontend Vue app
   Ensure your GenLayer Simulator is running, and execute the following commands in your terminal:
   ```shell
   cd app
   npm install
   npm run dev
   ```
   The terminal should display a link to access your frontend app (usually at http://localhost:5173/).
   For more information on the code see [GenLayerJS](https://github.com/yeagerai/genlayer-js).
   
### 5. Test contracts
1. Install the Python packages listed in the `requirements.txt` file in a virtual environment.
2. Make sure your GenLayer Simulator is running. Then execute the following command in your terminal:
   ```shell
   pytest test
   ```

## ⚽ How the Football Prediction Market Contract Works

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

## 🧪 Tests

This project includes integration tests that interact with the contract deployed in the simulator. These tests cover the main functionalities of the Football Prediction Market contract:

1. Creating a prediction
2. Resolving a prediction
3. Querying predictions for a player
4. Querying points for a player

The tests simulate real-world interactions with the contract, ensuring that it behaves correctly under various scenarios. They use the GenLayer simulator to deploy and interact with the contract, providing a comprehensive check of the contract's functionality in a controlled environment.

To run the tests, use the `pytest test` command as mentioned in the "Steps to run this example" section.


## 💬 Community
Connect with the GenLayer community to discuss, collaborate, and share insights:
- **[Discord Channel](https://discord.gg/8Jm4v89VAu)**: Our primary hub for discussions, support, and announcements.
- **[Telegram Group](https://t.me/genlayer)**: For more informal chats and quick updates.

Your continuous feedback drives better product development. Please engage with us regularly to test, discuss, and improve GenLayer.

## 📖 Documentation
For detailed information on how to use GenLayerJS SDK, please refer to our [documentation](https://docs.genlayer.io/).

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
