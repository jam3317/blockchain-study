const Block = require('./Block');

class Blockchain {
    constructor() {
        this.chain = [new Block("Genesis Block")];
    }

    addBlock(block) {
        const lastBlock = this.chain[this.chain.length - 1];
        block.previousHash = lastBlock.toHash();
        this.chain.push(block);
    }
}

module.exports = Blockchain;
