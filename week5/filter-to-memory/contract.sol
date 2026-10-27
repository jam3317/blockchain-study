// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract Contract {
    function filterEven(uint[] calldata numbers) external pure returns(uint[] memory) {
        // 1. 짝수가 몇 개인지 먼저 센다 (메모리 배열은 크기를 미리 정해야 해서)
        uint count;
        for (uint i = 0; i < numbers.length; i++) {
            if (numbers[i] % 2 == 0) {
                count++;
            }
        }

        // 2. 그 크기로 배열을 만들고 채운다
        uint[] memory evens = new uint[](count);
        uint j;
        for (uint i = 0; i < numbers.length; i++) {
            if (numbers[i] % 2 == 0) {
                evens[j] = numbers[i];
                j++;
            }
        }
        return evens;
    }
}
