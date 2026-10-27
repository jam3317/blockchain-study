// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract MultiSig {
    address[] public owners;
    uint256 public required;
    uint256 public transactionCount;

    struct Transaction {
        address destination;
        uint256 value;
        bool executed;
    }

    mapping(uint256 => Transaction) public transactions;

    constructor(address[] memory _owners, uint256 _required) {
        require(_owners.length > 0, "No owners");
        require(_required > 0, "Required must be at least 1");
        require(_required <= _owners.length, "Required exceeds owner count");
        owners = _owners;
        required = _required;
    }

    function addTransaction(address destination, uint256 value) public returns(uint256) {
        uint256 transactionId = transactionCount;
        transactions[transactionId] = Transaction(destination, value, false);
        transactionCount += 1;
        return transactionId;
    }
}
