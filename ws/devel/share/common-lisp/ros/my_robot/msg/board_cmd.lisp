; Auto-generated. Do not edit!


(cl:in-package my_robot-msg)


;//! \htmlinclude board_cmd.msg.html

(cl:defclass <board_cmd> (roslisp-msg-protocol:ros-message)
  ((reset
    :reader reset
    :initarg :reset
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass board_cmd (<board_cmd>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <board_cmd>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'board_cmd)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name my_robot-msg:<board_cmd> is deprecated: use my_robot-msg:board_cmd instead.")))

(cl:ensure-generic-function 'reset-val :lambda-list '(m))
(cl:defmethod reset-val ((m <board_cmd>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_robot-msg:reset-val is deprecated.  Use my_robot-msg:reset instead.")
  (reset m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <board_cmd>) ostream)
  "Serializes a message object of type '<board_cmd>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'reset) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <board_cmd>) istream)
  "Deserializes a message object of type '<board_cmd>"
    (cl:setf (cl:slot-value msg 'reset) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<board_cmd>)))
  "Returns string type for a message object of type '<board_cmd>"
  "my_robot/board_cmd")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'board_cmd)))
  "Returns string type for a message object of type 'board_cmd"
  "my_robot/board_cmd")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<board_cmd>)))
  "Returns md5sum for a message object of type '<board_cmd>"
  "ba4b0b221fb425ac5eaf73f71ae34971")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'board_cmd)))
  "Returns md5sum for a message object of type 'board_cmd"
  "ba4b0b221fb425ac5eaf73f71ae34971")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<board_cmd>)))
  "Returns full string definition for message of type '<board_cmd>"
  (cl:format cl:nil "bool reset~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'board_cmd)))
  "Returns full string definition for message of type 'board_cmd"
  (cl:format cl:nil "bool reset~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <board_cmd>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <board_cmd>))
  "Converts a ROS message object to a list"
  (cl:list 'board_cmd
    (cl:cons ':reset (reset msg))
))
