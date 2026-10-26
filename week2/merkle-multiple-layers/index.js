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
                nextLayer.push(this.concat(layer[i], layer[i + 1]));
            }
            layer = nextLayer;
        }
        return layer[0];
    }
}

module.exports = MerkleTree;
