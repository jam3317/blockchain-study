// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Party {
    uint256 public deposit;
    address[] public members;
    mapping(address => bool) public hasJoined;

    constructor(uint256 _deposit) {
        deposit = _deposit;
    }

    function rsvp() external payable {
        require(msg.value == deposit, "Must pay exactly the deposit");
        require(!hasJoined[msg.sender], "Already RSVP'd");

        hasJoined[msg.sender] = true;
        members.push(msg.sender);
    }

    function payBill(address venue, uint amount) external {
        (bool paid, ) = venue.call{ value: amount }("");
        require(paid, "Failed to pay the venue");

        // 남은 돈을 참가자 수로 똑같이 나눠 돌려준다
        uint share = address(this).balance / members.length;
        for (uint i = 0; i < members.length; i++) {
            (bool sent, ) = members[i].call{ value: share }("");
            require(sent, "Failed to refund");
        }
    }
}
