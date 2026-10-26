const Block = require('./Block');

class Blockchain {
    constructor() {
        this.chain = [new Block("Genesis Block")];
    }

    addBlock(block) {
        this.chain.push(block);
    }
}

module.exports = Blockchain;
