class MerkleTree {
    constructor(leaves, concat) {
        this.leaves = leaves;
        this.concat = concat;
    }

    getRoot() {
        let layer = this.leaves;
        while (layer.length > 1) {
            const nextLayer = [];
            for (let i = 0; i < layer.length; i += 2) {
                const left = layer[i];
                const right = layer[i + 1];
                if (right === undefined) {
                    nextLayer.push(left);
                } else {
                    nextLayer.push(this.concat(left, right));
                }
            }
            layer = nextLayer;
        }
        return layer[0];
    }
}

module.exports = MerkleTree;
