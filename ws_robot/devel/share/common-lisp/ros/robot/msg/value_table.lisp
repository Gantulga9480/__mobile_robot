; Auto-generated. Do not edit!


(cl:in-package robot-msg)


;//! \htmlinclude value_table.msg.html

(cl:defclass <value_table> (roslisp-msg-protocol:ros-message)
  ((table
    :reader table
    :initarg :table
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (width
    :reader width
    :initarg :width
    :type cl:integer
    :initform 0)
   (height
    :reader height
    :initarg :height
    :type cl:integer
    :initform 0))
)

(cl:defclass value_table (<value_table>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <value_table>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'value_table)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name robot-msg:<value_table> is deprecated: use robot-msg:value_table instead.")))

(cl:ensure-generic-function 'table-val :lambda-list '(m))
(cl:defmethod table-val ((m <value_table>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot-msg:table-val is deprecated.  Use robot-msg:table instead.")
  (table m))

(cl:ensure-generic-function 'width-val :lambda-list '(m))
(cl:defmethod width-val ((m <value_table>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot-msg:width-val is deprecated.  Use robot-msg:width instead.")
  (width m))

(cl:ensure-generic-function 'height-val :lambda-list '(m))
(cl:defmethod height-val ((m <value_table>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader robot-msg:height-val is deprecated.  Use robot-msg:height instead.")
  (height m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <value_table>) ostream)
  "Serializes a message object of type '<value_table>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'table))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'table))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'width)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'width)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'width)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'width)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'height)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'height)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'height)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'height)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <value_table>) istream)
  "Deserializes a message object of type '<value_table>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'table) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'table)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'width)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'width)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'width)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'width)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'height)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'height)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'height)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'height)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<value_table>)))
  "Returns string type for a message object of type '<value_table>"
  "robot/value_table")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'value_table)))
  "Returns string type for a message object of type 'value_table"
  "robot/value_table")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<value_table>)))
  "Returns md5sum for a message object of type '<value_table>"
  "e6c7b62a7859ac6c1c2f046f160fa3f8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'value_table)))
  "Returns md5sum for a message object of type 'value_table"
  "e6c7b62a7859ac6c1c2f046f160fa3f8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<value_table>)))
  "Returns full string definition for message of type '<value_table>"
  (cl:format cl:nil "float32[] table~%uint32 width~%uint32 height~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'value_table)))
  "Returns full string definition for message of type 'value_table"
  (cl:format cl:nil "float32[] table~%uint32 width~%uint32 height~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <value_table>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'table) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <value_table>))
  "Converts a ROS message object to a list"
  (cl:list 'value_table
    (cl:cons ':table (table msg))
    (cl:cons ':width (width msg))
    (cl:cons ':height (height msg))
))
