; Auto-generated. Do not edit!


(cl:in-package my_robot-msg)


;//! \htmlinclude board.msg.html

(cl:defclass <board> (roslisp-msg-protocol:ros-message)
  ((robot_x
    :reader robot_x
    :initarg :robot_x
    :type cl:integer
    :initform 0)
   (robot_y
    :reader robot_y
    :initarg :robot_y
    :type cl:integer
    :initform 0)
   (robot_dir
    :reader robot_dir
    :initarg :robot_dir
    :type cl:integer
    :initform 0))
)

(cl:defclass board (<board>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <board>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'board)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name my_robot-msg:<board> is deprecated: use my_robot-msg:board instead.")))

(cl:ensure-generic-function 'robot_x-val :lambda-list '(m))
(cl:defmethod robot_x-val ((m <board>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_robot-msg:robot_x-val is deprecated.  Use my_robot-msg:robot_x instead.")
  (robot_x m))

(cl:ensure-generic-function 'robot_y-val :lambda-list '(m))
(cl:defmethod robot_y-val ((m <board>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_robot-msg:robot_y-val is deprecated.  Use my_robot-msg:robot_y instead.")
  (robot_y m))

(cl:ensure-generic-function 'robot_dir-val :lambda-list '(m))
(cl:defmethod robot_dir-val ((m <board>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_robot-msg:robot_dir-val is deprecated.  Use my_robot-msg:robot_dir instead.")
  (robot_dir m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <board>) ostream)
  "Serializes a message object of type '<board>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'robot_x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'robot_x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'robot_x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'robot_x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'robot_y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'robot_y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'robot_y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'robot_y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'robot_dir)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'robot_dir)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'robot_dir)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'robot_dir)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <board>) istream)
  "Deserializes a message object of type '<board>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'robot_x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'robot_x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'robot_x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'robot_x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'robot_y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'robot_y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'robot_y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'robot_y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'robot_dir)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'robot_dir)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'robot_dir)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'robot_dir)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<board>)))
  "Returns string type for a message object of type '<board>"
  "my_robot/board")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'board)))
  "Returns string type for a message object of type 'board"
  "my_robot/board")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<board>)))
  "Returns md5sum for a message object of type '<board>"
  "ef7ee7650d05aecc708d6053f43fabfb")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'board)))
  "Returns md5sum for a message object of type 'board"
  "ef7ee7650d05aecc708d6053f43fabfb")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<board>)))
  "Returns full string definition for message of type '<board>"
  (cl:format cl:nil "uint32 robot_x~%uint32 robot_y~%uint32 robot_dir~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'board)))
  "Returns full string definition for message of type 'board"
  (cl:format cl:nil "uint32 robot_x~%uint32 robot_y~%uint32 robot_dir~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <board>))
  (cl:+ 0
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <board>))
  "Converts a ROS message object to a list"
  (cl:list 'board
    (cl:cons ':robot_x (robot_x msg))
    (cl:cons ':robot_y (robot_y msg))
    (cl:cons ':robot_dir (robot_dir msg))
))
