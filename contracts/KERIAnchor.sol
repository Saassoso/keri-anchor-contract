// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract KERIAnchor is Ownable {
    // 0 = PENDING, 1 = ACTIVE, 2 = REVOKED
    enum DeviceStatus { PENDING, ACTIVE, REVOKED }
    
    mapping(string => mapping(uint256 => string)) public anchors;
    mapping(string => uint256) public latestSequence;
    mapping(string => DeviceStatus) public deviceStates; 

    event AnchorRegistered(string aid, uint256 sequence, string hash);
    event DeviceStatusChanged(string aid, DeviceStatus status);

    constructor() Ownable(msg.sender) {}

    // The Gatekeeper: Rejects if device is Revoked or Pending
    function registerAnchor(string memory aid, uint256 sequence, string memory hash) public {
        require(deviceStates[aid] == DeviceStatus.ACTIVE, "Access Denied: Device not Authorized");
        require(sequence > latestSequence[aid], "Invalid Sequence");

        anchors[aid][sequence] = hash;
        latestSequence[aid] = sequence;
        
        emit AnchorRegistered(aid, sequence, hash);
    }
    
    // Status Management
    function authorizeDevice(string memory aid) public onlyOwner {
        deviceStates[aid] = DeviceStatus.ACTIVE;
        emit DeviceStatusChanged(aid, DeviceStatus.ACTIVE);
    }

    function revokeDevice(string memory aid) public onlyOwner {
        deviceStates[aid] = DeviceStatus.REVOKED;
        emit DeviceStatusChanged(aid, DeviceStatus.REVOKED);
    }
}