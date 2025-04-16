import { readFileSync } from "fs";
import path from "path";
import { TransactionHash, TransactionStatus, GenLayerClient } from "genlayer-js/types";


export default async function main(client: GenLayerClient<any>) {
  const filePath = path.resolve(process.cwd(), "contracts/football_bets.py");

  try {
    const contractCode = new Uint8Array(readFileSync(filePath));

    await client.initializeConsensusSmartContract();

    const deployTransaction = await client.deployContract({
      code: contractCode,
      args: [],
    });

    const receipt = await client.waitForTransactionReceipt({
      hash: deployTransaction as TransactionHash,
      status: TransactionStatus.ACCEPTED,
      retries: 200,
    });

    if (receipt.consensus_data?.leader_receipt?.execution_result !== "SUCCESS") {
      throw new Error(`Deployment failed. Receipt: ${JSON.stringify(receipt)}`);
    }
  } catch (error) {
    throw new Error((`Error during deployment:, ${error}`));
  }
}
