const provider = require('./provider');

async function getTotalBalance(addresses) {
    const requests = addresses.map((address, i) => ({
        jsonrpc: "2.0",
        id: i,
        method: "eth_getBalance",
        params: [address, "latest"],
    }));

    const responses = await provider.send(requests);

    return responses.reduce((total, response) => total + parseInt(response.result), 0);
}

module.exports = getTotalBalance;
