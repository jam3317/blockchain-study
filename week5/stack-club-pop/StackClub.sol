// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract StackClub {
    address[] members;

    constructor() {
        members.push(msg.sender);
    }

    modifier onlyMember {
        require(isMember(msg.sender), "Only members can do this");
        _;
    }

    function addMember(address member) external onlyMember {
        members.push(member);
    }

    function removeLastMember() external onlyMember {
        members.pop();
    }

    function isMember(address member) public view returns(bool) {
        for (uint i = 0; i < members.length; i++) {
            if (members[i] == member) {
                return true;
            }
        }
        return false;
    }
}
