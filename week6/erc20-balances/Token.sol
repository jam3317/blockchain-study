// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract Token {
    uint public totalSupply;
    string public name = "Study Token";
    string public symbol = "STK";
    uint8 public decimals = 18;

    mapping(address => uint256) balances;

    function balanceOf(address account) external view returns (uint256) {
        return balances[account];
    }
}
