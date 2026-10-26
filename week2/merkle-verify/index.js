class MerkleTree {
    constructor(leaves, concat) {
        this.leaves = leaves;
        this.concat = concat;
    }

    getRoot() {
        let layer = this.leaves;
        while (layer.length > 1) {
            layer = this.nextLayer(layer);
        }
        return layer[0];
    }

    // 한 층을 두 개씩 묶어 위층을 만든다. 짝이 없으면 그대로 올린다.
    nextLayer(layer) {
        const next = [];
        for (let i = 0; i < layer.length; i += 2) {
            const left = layer[i];
            const right = layer[i + 1];
            next.push(right === undefined ? left : this.concat(left, right));
        }
        return next;
    }

    getProof(index) {
        const proof = [];
        let layer = this.leaves;
        while (layer.length > 1) {
            const isLeft = index % 2 === 0;
            const pairIndex = isLeft ? index + 1 : index - 1;
            if (pairIndex < layer.length) {
                proof.push({ data: layer[pairIndex], left: !isLeft });
            }
            layer = this.nextLayer(layer);
            index = Math.floor(index / 2);
        }
        return proof;
    }
}

module.exports = MerkleTree;
