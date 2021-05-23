// Auto-generated. Do not edit!

// (in-package robot.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class value_table {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.table = null;
      this.width = null;
      this.height = null;
    }
    else {
      if (initObj.hasOwnProperty('table')) {
        this.table = initObj.table
      }
      else {
        this.table = [];
      }
      if (initObj.hasOwnProperty('width')) {
        this.width = initObj.width
      }
      else {
        this.width = 0;
      }
      if (initObj.hasOwnProperty('height')) {
        this.height = initObj.height
      }
      else {
        this.height = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type value_table
    // Serialize message field [table]
    bufferOffset = _arraySerializer.float32(obj.table, buffer, bufferOffset, null);
    // Serialize message field [width]
    bufferOffset = _serializer.uint32(obj.width, buffer, bufferOffset);
    // Serialize message field [height]
    bufferOffset = _serializer.uint32(obj.height, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type value_table
    let len;
    let data = new value_table(null);
    // Deserialize message field [table]
    data.table = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [width]
    data.width = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [height]
    data.height = _deserializer.uint32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.table.length;
    return length + 12;
  }

  static datatype() {
    // Returns string type for a message object
    return 'robot/value_table';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e6c7b62a7859ac6c1c2f046f160fa3f8';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32[] table
    uint32 width
    uint32 height
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new value_table(null);
    if (msg.table !== undefined) {
      resolved.table = msg.table;
    }
    else {
      resolved.table = []
    }

    if (msg.width !== undefined) {
      resolved.width = msg.width;
    }
    else {
      resolved.width = 0
    }

    if (msg.height !== undefined) {
      resolved.height = msg.height;
    }
    else {
      resolved.height = 0
    }

    return resolved;
    }
};

module.exports = value_table;
