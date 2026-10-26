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

        const inputAmount = this.inputUTXOs.reduce((sum, utxo) => sum + utxo.amount, 0);
        const outputAmount = this.outputUTXOs.reduce((sum, utxo) => sum + utxo.amount, 0);
        if (inputAmount < outputAmount) {
            throw new Error("Not enough input to cover the outputs!");
        }

        this.inputUTXOs.forEach((utxo) => utxo.spend());

        this.fee = inputAmount - outputAmount;
    }
}

module.exports = Transaction;
