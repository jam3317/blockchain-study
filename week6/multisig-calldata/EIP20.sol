// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

// 강의 사이트에 숨겨져 있는 테스트용 토큰(EIP20)을 같은 생성자 모양으로 간단히 다시 만든 것.
// 테스트는 transfer와 balanceOf만 쓴다.
contract EIP20 {
    mapping(address => uint256) public balanceOf;
    string public name;
    uint8 public decimals;
    string public symbol;
    uint256 public totalSupply;

    constructor(uint256 _initialAmount, string memory _tokenName, uint8 _decimalUnits, string memory _tokenSymbol) {
        balanceOf[msg.sender] = _initialAmount;
        totalSupply = _initialAmount;
        name = _tokenName;
        decimals = _decimalUnits;
        symbol = _tokenSymbol;
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        require(balanceOf[msg.sender] >= _value, "Not enough tokens");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        return true;
    }
}
