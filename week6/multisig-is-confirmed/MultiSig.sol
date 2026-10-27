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
    mapping(uint256 => mapping(address => bool)) public confirmations;

    constructor(address[] memory _owners, uint256 _required) {
        require(_owners.length > 0, "No owners");
        require(_required > 0, "Required must be at least 1");
        require(_required <= _owners.length, "Required exceeds owner count");
        owners = _owners;
        required = _required;
    }

    function addTransaction(address destination, uint256 value) internal returns(uint256) {
        uint256 transactionId = transactionCount;
        transactions[transactionId] = Transaction(destination, value, false);
        transactionCount += 1;
        return transactionId;
    }

    function isOwner(address addr) private view returns(bool) {
        for (uint i = 0; i < owners.length; i++) {
            if (owners[i] == addr) {
                return true;
            }
        }
        return false;
    }

    function confirmTransaction(uint256 transactionId) public {
        require(isOwner(msg.sender), "Only owners can confirm");
        confirmations[transactionId][msg.sender] = true;
    }

    function getConfirmationsCount(uint transactionId) public view returns(uint256) {
        uint256 count;
        for (uint i = 0; i < owners.length; i++) {
            if (confirmations[transactionId][owners[i]]) {
                count++;
            }
        }
        return count;
    }

    function submitTransaction(address destination, uint value) external {
        uint256 transactionId = addTransaction(destination, value);
        confirmTransaction(transactionId);
    }

    receive() external payable { }

    function isConfirmed(uint transactionId) public view returns(bool) {
        return getConfirmationsCount(transactionId) >= required;
    }
}
