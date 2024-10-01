import { createClient, createAccount as createGenLayerAccount, generatePrivateKey } from "genlayer-js";
import { simulator } from "genlayer-js/chains";

const accountPrivateKey = localStorage.getItem("accountPrivateKey")
  ? localStorage.getItem("accountPrivateKey")
  : null;
console.log("🚀 ~ accountPrivateKey:", accountPrivateKey);
export const account = accountPrivateKey ? createGenLayerAccount(accountPrivateKey) : null;
console.log("🚀 ~ account:", account);

export const createAccount = () => {
  const newAccountPrivateKey = generatePrivateKey();
  localStorage.setItem("accountPrivateKey", newAccountPrivateKey);
  return createGenLayerAccount(newAccountPrivateKey);
};

export const client = createClient({ chain: simulator, account });
