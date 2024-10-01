import { createClient } from "genlayer-js";
import { simulator } from "genlayer-js/chains";

class PredictionMarket {
  contractAddress;
  client;

  constructor(contractAddress, account = null) {
    this.contractAddress = contractAddress;
    const config = { chain: simulator, ...(account ? { account } : {}) };
    this.client = createClient(config);
  }

  updateAccount(account) {
    this.client = createClient({ chain: simulator, account });
  }

  async getPredictions() {
    const predictions = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_predictions",
      args: [],
    });
    return Object.entries(predictions).flatMap(([owner, prediction]) => {
      return Object.entries(prediction).map(([id, predictionData]) => ({
        id,
        ...predictionData,
        owner,
      }));
    });
  }

  async getPlayerPoints(address) {
    if (!address) {
      return 0;
    }
    const points = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_player_points",
      args: [address],
    });
    return points;
  }

  async getLeaderboard() {
    const points = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_points",
      args: [],
    });

    return Object.entries(points)
      .map(([address, points]) => ({ address, points }))
      .sort((a, b) => b.points - a.points);
  }

  async createPrediction(gameDate, team1, team2, predictedWinner) {
    const txHash = await this.client.writeContract({
      address: this.contractAddress,
      functionName: "create_prediction",
      args: [gameDate, team1, team2, predictedWinner],
    });
    const receipt = await this.client.waitForTransactionReceipt({
      hash: txHash,
      status: "FINALIZED",
    });
    return receipt;
  }

  async resolvePrediction(predictionId) {
    const txHash = await this.client.writeContract({
      address: this.contractAddress,
      functionName: "resolve_prediction",
      args: [predictionId],
    });
    const receipt = await this.client.waitForTransactionReceipt({
      hash: txHash,
      status: "FINALIZED",
    });
    return receipt;
  }
}

export default PredictionMarket;
