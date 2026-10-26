// Activity: JSON-RPC Read Requests
// 강의는 axios + 내 Alchemy URL을 쓰지만, 여기서는 Node 기본 fetch와
// 키가 필요 없는 공개 노드를 쓴다. 내 Alchemy URL이 있으면 아래 주소만 바꾸면 된다.
const RPC_URL = process.env.RPC_URL || "https://eth.drpc.org";

async function rpc(method, params = []) {
    const response = await fetch(RPC_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
    });
    const data = await response.json();
    if (data.error) throw new Error(`${method}: ${data.error.message}`);
    return data.result;
}

async function main() {
    // 1. 강의 예제: 메인넷 46147번 블록 (0xb443) 가져오기
    const block = await rpc("eth_getBlockByNumber", ["0xb443", true]);
    console.log("block 46147");
    console.log("  hash:        ", block.hash);
    console.log("  miner:       ", block.miner);
    console.log("  timestamp:   ", new Date(parseInt(block.timestamp) * 1000).toISOString());
    console.log("  transactions:", block.transactions.length);
    if (block.transactions[0]) {
        const tx = block.transactions[0];
        console.log("  first tx:     from", tx.from, "→ to", tx.to, "value", parseInt(tx.value) / 1e18, "ETH");
    }

    // 2. 다른 메서드로 바꿔 보기
    const latest = await rpc("eth_blockNumber");
    console.log("\neth_blockNumber:", parseInt(latest));

    const chainId = await rpc("eth_chainId");
    console.log("eth_chainId:    ", parseInt(chainId), "(1 = 메인넷)");

    const gasPrice = await rpc("eth_gasPrice");
    console.log("eth_gasPrice:   ", (parseInt(gasPrice) / 1e9).toFixed(2), "gwei");

    // 이더리움 재단 기부 주소 (공개된 유명 주소)
    const address = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe";
    const balance = await rpc("eth_getBalance", [address, "latest"]);
    console.log("eth_getBalance: ", (Number(BigInt(balance)) / 1e18).toFixed(4), "ETH  (" + address + ")");

    const nonce = await rpc("eth_getTransactionCount", [address, "latest"]);
    console.log("eth_getTransactionCount:", parseInt(nonce));
}

main().catch((e) => {
    console.error(e.message);
    process.exit(1);
});
