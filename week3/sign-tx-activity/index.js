// Activity: Send a Signed JSON-RPC Request on Sepolia
// 강의는 alchemy-sdk를 쓰지만, 같은 일을 이미 설치된 ethers v5로 한다.
// 실행: node --env-file=week3/sign-tx-activity/.env week3/sign-tx-activity/index.js
const { Wallet, providers, utils } = require("ethers");

const { TEST_PRIVATE_KEY, SEPOLIA_RPC_URL, TO_ADDRESS } = process.env;

async function main() {
    if (!TEST_PRIVATE_KEY || !SEPOLIA_RPC_URL || !TO_ADDRESS) {
        console.log(".env에 TEST_PRIVATE_KEY, SEPOLIA_RPC_URL, TO_ADDRESS를 채워 주세요. (.env.example 참고)");
        process.exit(1);
    }

    const provider = new providers.JsonRpcProvider(SEPOLIA_RPC_URL);
    const wallet = new Wallet(TEST_PRIVATE_KEY, provider);

    const nonce = await provider.getTransactionCount(wallet.address, "latest");

    const transaction = {
        to: TO_ADDRESS,
        value: utils.parseEther("0.001"),          // 0.001 ETH
        gasLimit: 21000,
        maxPriorityFeePerGas: utils.parseUnits("5", "gwei"),
        maxFeePerGas: utils.parseUnits("20", "gwei"),
        nonce,
        type: 2,                                    // EIP-1559 거래
        chainId: 11155111,                          // Sepolia
    };

    const rawTransaction = await wallet.signTransaction(transaction);
    console.log("Raw tx:", rawTransaction);

    const tx = await provider.sendTransaction(rawTransaction);
    console.log(`https://sepolia.etherscan.io/tx/${tx.hash}`);
}

main().catch((e) => {
    console.error(e.message);
    process.exit(1);
});
