function verifyProof(proof, node, root, concat) {
    let data = node;
    for (const step of proof) {
        data = step.left ? concat(step.data, data) : concat(data, step.data);
    }
    return data === root;
}

module.exports = verifyProof;
