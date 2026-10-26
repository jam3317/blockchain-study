const TrieNode = require('./TrieNode');

class Trie {
    constructor() {
        this.root = new TrieNode(null);
    }

    insert(word) {
        let node = this.root;
        for (const letter of word) {
            if (!node.children[letter]) {
                node.children[letter] = new TrieNode(letter);
            }
            node = node.children[letter];
        }
        node.isWord = true;
    }
}

module.exports = Trie;
