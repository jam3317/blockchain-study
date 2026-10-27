// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract Contract {
    enum Choices { Yes, No }

    struct Vote {
        Choices choice;
        address voter;
    }

    Vote[] public votes;

    function createVote(Choices choice) external {
        require(!hasVoted(msg.sender), "Already voted");
        votes.push(Vote(choice, msg.sender));
    }

    function changeVote(Choices choice) external {
        for (uint i = 0; i < votes.length; i++) {
            if (votes[i].voter == msg.sender) {
                votes[i].choice = choice;   // storage 배열 원소를 직접 고친다
                return;
            }
        }
        revert("No existing vote");
    }

    function findVote(address voter) internal view returns(bool found, Vote memory vote) {
        for (uint i = 0; i < votes.length; i++) {
            if (votes[i].voter == voter) {
                return (true, votes[i]);
            }
        }
    }

    function hasVoted(address voter) public view returns(bool) {
        (bool found, ) = findVote(voter);
        return found;
    }

    function findChoice(address voter) external view returns(Choices) {
        (, Vote memory vote) = findVote(voter);
        return vote.choice;
    }
}
