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
        votes.push(Vote(choice, msg.sender));
    }

    // 두 함수가 함께 쓰는 도우미: 그 주소의 투표를 찾아 (찾았는지, 투표) 를 돌려준다
    function findVote(address voter) internal view returns(bool found, Vote memory vote) {
        for (uint i = 0; i < votes.length; i++) {
            if (votes[i].voter == voter) {
                return (true, votes[i]);
            }
        }
    }

    function hasVoted(address voter) external view returns(bool) {
        (bool found, ) = findVote(voter);
        return found;
    }

    function findChoice(address voter) external view returns(Choices) {
        (, Vote memory vote) = findVote(voter);
        return vote.choice;
    }
}
