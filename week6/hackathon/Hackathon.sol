// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Hackathon {
    struct Project {
        string title;
        uint[] ratings;
    }

    Project[] projects;

    function findWinner() external view returns(Project memory) {
        uint bestIndex;
        uint bestAverage;
        for (uint i = 0; i < projects.length; i++) {
            uint[] storage ratings = projects[i].ratings;
            uint sum;
            for (uint j = 0; j < ratings.length; j++) {
                sum += ratings[j];
            }
            uint average = ratings.length == 0 ? 0 : sum / ratings.length;
            if (average > bestAverage) {
                bestAverage = average;
                bestIndex = i;
            }
        }
        return projects[bestIndex];
    }

    function newProject(string calldata _title) external {
        // creates a new project with a title and an empty ratings array
        projects.push(Project(_title, new uint[](0)));
    }

    function rate(uint _idx, uint _rating) external {
        // rates a project by its index
        projects[_idx].ratings.push(_rating);
    }
}
