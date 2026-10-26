const { providers } = require('ethers');
const { ganacheProvider } = require('./config');

const provider = new providers.Web3Provider(ganacheProvider);

/**
 * Given an ethereum address find all the addresses
 * that were sent ether from that address
 * @param {string} address - The hexadecimal address for the sender
 * @async
 * @returns {Array} all the addresses that received ether
 */
async function findEther(address) {
    const addresses = [];
    const latest = await provider.getBlockNumber();
    for (let i = 0; i <= latest; i++) {
        const block = await provider.getBlockWithTransactions(i);
        for (const tx of block.transactions) {
            if (tx.from === address) {
                addresses.push(tx.to);
            }
        }
    }
    return addresses;
}

module.exports = findEther;
