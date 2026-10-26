#!/bin/sh
# Solidity 단계 폴더 하나를 컴파일하고 테스트한다.
# 사용법: sh tools/sol-test.sh week4/booleans
STAGE="${1%/}"
TESTS=$(ls "$STAGE"/*.js 2>/dev/null | grep -v -E '/(config|hardhat\.config)\.js$')
STAGE="$STAGE" npx hardhat test $TESTS
