; Auto-generated. Do not edit!


(cl:in-package my_robot-msg)


;//! \htmlinclude next_move.msg.html

(cl:defclass <next_move> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:integer
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:integer
    :initform 0)
   (dir
    :reader dir
    :initarg :dir
    :type cl:integer
    :initform 0))
)

(cl:defclass next_move (<next_move>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <next_move>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'next_move)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name my_robot-msg:<next_move> is deprecated: use my_robot-msg:next_move instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <next_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_robot-msg:x-val is deprecated.  Use my_robot-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <next_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_robot-msg:y-val is deprecated.  Use my_robot-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'dir-val :lambda-list '(m))
(cl:defmethod dir-val ((m <next_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_robot-msg:dir-val is deprecated.  Use my_robot-msg:dir instead.")
  (dir m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <next_move>) ostream)
  "Serializes a message object of type '<next_move>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'dir)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'dir)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'dir)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'dir)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <next_move>) istream)
  "Deserializes a message object of type '<next_move>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'dir)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'dir)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'dir)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'dir)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<next_move>)))
  "Returns string type for a message object of type '<next_move>"
  "my_robot/next_move")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'next_move)))
  "Returns string type for a message object of type 'next_move"
  "my_robot/next_move")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<next_move>)))
  "Returns md5sum for a message object of type '<next_move>"
  "6be196b93b60b5075636cca4033ccd62")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'next_move)))
  "Returns md5sum for a message object of type 'next_move"
  "6be196b93b60b5075636cca4033ccd62")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<next_move>)))
  "Returns full string definition for message of type '<next_move>"
  (cl:format cl:nil "uint32 x~%uint32 y~%uint32 dir~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'next_move)))
  "Returns full string definition for message of type 'next_move"
  (cl:format cl:nil "uint32 x~%uint32 y~%uint32 dir~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <next_move>))
  (cl:+ 0
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <next_move>))
  "Converts a ROS message object to a list"
  (cl:list 'next_move
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':dir (dir msg))
))
