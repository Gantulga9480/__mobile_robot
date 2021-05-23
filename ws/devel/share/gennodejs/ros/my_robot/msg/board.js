// Auto-generated. Do not edit!

// (in-package my_robot.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class board {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.robot_x = null;
      this.robot_y = null;
      this.robot_dir = null;
    }
    else {
      if (initObj.hasOwnProperty('robot_x')) {
        this.robot_x = initObj.robot_x
      }
      else {
        this.robot_x = 0;
      }
      if (initObj.hasOwnProperty('robot_y')) {
        this.robot_y = initObj.robot_y
      }
      else {
        this.robot_y = 0;
      }
      if (initObj.hasOwnProperty('robot_dir')) {
        this.robot_dir = initObj.robot_dir
      }
      else {
        this.robot_dir = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type board
    // Serialize message field [robot_x]
    bufferOffset = _serializer.uint32(obj.robot_x, buffer, bufferOffset);
    // Serialize message field [robot_y]
    bufferOffset = _serializer.uint32(obj.robot_y, buffer, bufferOffset);
    // Serialize message field [robot_dir]
    bufferOffset = _serializer.uint32(obj.robot_dir, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type board
    let len;
    let data = new board(null);
    // Deserialize message field [robot_x]
    data.robot_x = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [robot_y]
    data.robot_y = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [robot_dir]
    data.robot_dir = _deserializer.uint32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'my_robot/board';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ef7ee7650d05aecc708d6053f43fabfb';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint32 robot_x
    uint32 robot_y
    uint32 robot_dir
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new board(null);
    if (msg.robot_x !== undefined) {
      resolved.robot_x = msg.robot_x;
    }
    else {
      resolved.robot_x = 0
    }

    if (msg.robot_y !== undefined) {
      resolved.robot_y = msg.robot_y;
    }
    else {
      resolved.robot_y = 0
    }

    if (msg.robot_dir !== undefined) {
      resolved.robot_dir = msg.robot_dir;
    }
    else {
      resolved.robot_dir = 0
    }

    return resolved;
    }
};

module.exports = board;
