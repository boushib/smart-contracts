// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0;

contract Storage {
  uint256 public dataStore = 0;

  function set(uint256 n) public {
    dataStore = n;
  }

  function get() public view returns (uint256) {
    return dataStore;
  }
}
