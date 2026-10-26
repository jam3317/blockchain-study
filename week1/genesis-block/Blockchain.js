const Block = require('./Block');

class Blockchain {
    constructor() {
        this.chain = [new Block("Genesis Block")];
    }
}

module.exports = Blockchain;
