// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface AggregatorV3Interface {
  function decimals() external view returns (uint8);

  function description() external view returns (string memory);

  function version() external view returns (uint256);

  function getRoundData(uint80 _roundId)
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

  function latestRoundData()
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );
}

contract Fund {
  mapping(address => uint256) public addressToAmountFunded;
  address public owner;
  address[] public funders;

  constructor() {
    owner = msg.sender;
  }

  modifier ownerOnly() {
    require(msg.sender == owner, "Only the owner can perform this action!");
    _; // continue execution
  }

  function getUSDRate() public view returns (uint256) {
    AggregatorV3Interface priceFeed = AggregatorV3Interface(
      0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
    );

    (, int256 answer, , , ) = priceFeed.latestRoundData();

    return uint256(answer * 10000000000);
  }

  function ethToUSD(uint256 ethAmount) public view returns (uint256) {
    uint256 usdRate = getUSDRate();
    return (ethAmount * usdRate) / 1000000000000000000;
  }

  function fund() public payable {
    uint256 minUSD = 50 * 10**18;
    require(ethToUSD(msg.value) >= minUSD, "You need to spend at least $50!");
    addressToAmountFunded[msg.sender] += msg.value;
    funders.push(msg.sender);
  }

  function withdraw() public payable ownerOnly {
    payable(msg.sender).transfer(address(this).balance);

    // Reset funders
    for (uint256 i = 0; i < funders.length; i++) {
      addressToAmountFunded[funders[i]] = 0;
    }

    funders = new address[](0);
  }
}
