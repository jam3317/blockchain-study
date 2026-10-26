class Transaction {
    constructor(inputUTXOs, outputUTXOs) {
        this.inputUTXOs = inputUTXOs;
        this.outputUTXOs = outputUTXOs;
    }

    execute() {
        const anySpent = this.inputUTXOs.some((utxo) => utxo.spent);
        if (anySpent) {
            throw new Error("Cannot include a spent UTXO as an input!");
        }
    }
}

module.exports = Transaction;
