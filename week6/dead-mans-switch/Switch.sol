// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract Switch {
    address owner;
    address recipient;
    uint lastAction;

    constructor(address _recipient) payable {
        owner = msg.sender;
        recipient = _recipient;
        lastAction = block.timestamp;
    }

    function ping() external {
        require(msg.sender == owner, "Only the owner can ping");
        lastAction = block.timestamp;
    }

    function withdraw() external {
        require(block.timestamp - lastAction >= 52 weeks, "Owner is still active");
        (bool sent, ) = recipient.call{ value: address(this).balance }("");
        require(sent, "Failed to send ether");
    }
}
