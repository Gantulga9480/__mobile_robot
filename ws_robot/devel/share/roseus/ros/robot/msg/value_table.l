;; Auto-generated. Do not edit!


(when (boundp 'robot::value_table)
  (if (not (find-package "ROBOT"))
    (make-package "ROBOT"))
  (shadow 'value_table (find-package "ROBOT")))
(unless (find-package "ROBOT::VALUE_TABLE")
  (make-package "ROBOT::VALUE_TABLE"))

(in-package "ROS")
;;//! \htmlinclude value_table.msg.html


(defclass robot::value_table
  :super ros::object
  :slots (_table _width _height ))

(defmethod robot::value_table
  (:init
   (&key
    ((:table __table) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:width __width) 0)
    ((:height __height) 0)
    )
   (send-super :init)
   (setq _table __table)
   (setq _width (round __width))
   (setq _height (round __height))
   self)
  (:table
   (&optional __table)
   (if __table (setq _table __table)) _table)
  (:width
   (&optional __width)
   (if __width (setq _width __width)) _width)
  (:height
   (&optional __height)
   (if __height (setq _height __height)) _height)
  (:serialization-length
   ()
   (+
    ;; float32[] _table
    (* 4    (length _table)) 4
    ;; uint32 _width
    4
    ;; uint32 _height
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32[] _table
     (write-long (length _table) s)
     (dotimes (i (length _table))
       (sys::poke (elt _table i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; uint32 _width
       (write-long _width s)
     ;; uint32 _height
       (write-long _height s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32[] _table
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _table (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _table i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; uint32 _width
     (setq _width (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _height
     (setq _height (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get robot::value_table :md5sum-) "e6c7b62a7859ac6c1c2f046f160fa3f8")
(setf (get robot::value_table :datatype-) "robot/value_table")
(setf (get robot::value_table :definition-)
      "float32[] table
uint32 width
uint32 height
")



(provide :robot/value_table "e6c7b62a7859ac6c1c2f046f160fa3f8")


