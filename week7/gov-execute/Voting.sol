// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Voting {
    enum VoteStates { Absent, Yes, No }

    struct Proposal {
        address target;
        bytes data;
        uint yesCount;
        uint noCount;
    }

    Proposal[] public proposals;
    mapping(uint => mapping(address => VoteStates)) voteStates;

    mapping(address => bool) members;
    mapping(uint => bool) executed;

    event ProposalCreated(uint proposalId);
    event VoteCast(uint proposalId, address voter);

    constructor(address[] memory _members) {
        members[msg.sender] = true;
        for (uint i = 0; i < _members.length; i++) {
            members[_members[i]] = true;
        }
    }

    modifier onlyMember {
        require(members[msg.sender], "Only members");
        _;
    }

    function newProposal(address target, bytes calldata data) external onlyMember {
        emit ProposalCreated(proposals.length);
        proposals.push(Proposal(target, data, 0, 0));
    }

    function castVote(uint proposalId, bool support) external onlyMember {
        Proposal storage proposal = proposals[proposalId];
        VoteStates previous = voteStates[proposalId][msg.sender];

        // 이전 표를 먼저 빼고
        if (previous == VoteStates.Yes) {
            proposal.yesCount--;
        } else if (previous == VoteStates.No) {
            proposal.noCount--;
        }

        // 새 표를 더한다
        if (support) {
            proposal.yesCount++;
        } else {
            proposal.noCount++;
        }
        voteStates[proposalId][msg.sender] = support ? VoteStates.Yes : VoteStates.No;

        emit VoteCast(proposalId, msg.sender);

        // 찬성 10표가 모이면 한 번만 실행
        if (proposal.yesCount == 10 && !executed[proposalId]) {
            executed[proposalId] = true;
            (bool success, ) = proposal.target.call(proposal.data);
            require(success, "Execution failed");
        }
    }
}
