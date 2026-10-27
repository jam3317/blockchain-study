// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

library Prime {
    function dividesEvenly(uint x, uint y) public pure returns (bool) {
        return x % y == 0;
    }

    function isPrime(uint x) public pure returns (bool) {
        if (x < 2) {
            return false;
        }
        for (uint i = 2; i * i <= x; i++) {
            if (dividesEvenly(x, i)) {
                return false;
            }
        }
        return true;
    }
}
