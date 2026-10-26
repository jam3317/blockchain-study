class Tree {
    constructor() {
        this.root = null;
    }

    addNode(node) {
        if (!this.root) {
            this.root = node;
            return;
        }
        this.addChild(this.root, node);
    }

    addChild(parent, child) {
        if (child.data < parent.data) {
            if (parent.left) {
                this.addChild(parent.left, child);
            } else {
                parent.left = child;
            }
        } else {
            if (parent.right) {
                this.addChild(parent.right, child);
            } else {
                parent.right = child;
            }
        }
    }

    hasNode(number) {
        let current = this.root;
        while (current) {
            if (number === current.data) {
                return true;
            }
            current = number < current.data ? current.left : current.right;
        }
        return false;
    }
}

module.exports = Tree;
