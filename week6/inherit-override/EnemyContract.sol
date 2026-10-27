// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

import "./Hero.sol";

// 사이트에는 숨겨져 있는 테스트용 적 컨트랙트 (로컬 실행용으로 직접 작성)
contract EnemyContract is Enemy {
    event Attacked(Hero.AttackTypes attackType);

    function takeAttack(Hero.AttackTypes attackType) external override {
        emit Attacked(attackType);
    }
}
