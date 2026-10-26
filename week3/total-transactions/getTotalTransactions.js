const provider = require('./provider');

async function getTotalTransactions(blockNumber) {
    const response = await provider.send({
        jsonrpc: "2.0",
        id: 1,
        method: "eth_getBlockTransactionCountByNumber",
        params: ["0x" + blockNumber.toString(16)],
    });

    return response.result;
}

module.exports = getTotalTransactions;
