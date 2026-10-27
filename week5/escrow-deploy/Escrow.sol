// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract Escrow {
    address public depositor;
    address public beneficiary;
    address public arbiter;
    bool public isApproved;

    event Approved(uint balance);

    constructor(address _arbiter, address _beneficiary) payable {
        arbiter = _arbiter;
        beneficiary = _beneficiary;
        depositor = msg.sender;
    }

    function approve() external {
        require(msg.sender == arbiter, "Only the arbiter can approve");
        uint balance = address(this).balance;
        isApproved = true;
        (bool sent, ) = beneficiary.call{ value: balance }("");
        require(sent, "Failed to send ether");
        emit Approved(balance);
    }
}
