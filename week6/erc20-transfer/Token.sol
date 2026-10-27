// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

contract Token {
    uint public totalSupply;
    string public name = "Study Token";
    string public symbol = "STK";
    uint8 public decimals = 18;

    mapping(address => uint256) balances;

    constructor() {
        totalSupply = 1000 * (10 ** decimals);
        balances[msg.sender] = totalSupply;
    }

    function balanceOf(address account) external view returns (uint256) {
        return balances[account];
    }

    function transfer(address recipient, uint amount) public returns (bool) {
        require(balances[msg.sender] >= amount, "Not enough balance");
        balances[msg.sender] -= amount;
        balances[recipient] += amount;
        return true;
    }
}
