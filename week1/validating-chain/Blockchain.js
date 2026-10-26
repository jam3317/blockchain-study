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

    isValid() {
        for (let i = 1; i < this.chain.length; i++) {
            const previous = this.chain[i - 1];
            const current = this.chain[i];
            if (current.previousHash.toString() !== previous.toHash().toString()) {
                return false;
            }
        }
        return true;
    }
}

module.exports = Blockchain;
