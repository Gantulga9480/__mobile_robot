;; Auto-generated. Do not edit!


(when (boundp 'robot::board)
  (if (not (find-package "ROBOT"))
    (make-package "ROBOT"))
  (shadow 'board (find-package "ROBOT")))
(unless (find-package "ROBOT::BOARD")
  (make-package "ROBOT::BOARD"))

(in-package "ROS")
;;//! \htmlinclude board.msg.html


(defclass robot::board
  :super ros::object
  :slots (_robot_x _robot_y _robot_dir ))

(defmethod robot::board
  (:init
   (&key
    ((:robot_x __robot_x) 0)
    ((:robot_y __robot_y) 0)
    ((:robot_dir __robot_dir) 0)
    )
   (send-super :init)
   (setq _robot_x (round __robot_x))
   (setq _robot_y (round __robot_y))
   (setq _robot_dir (round __robot_dir))
   self)
  (:robot_x
   (&optional __robot_x)
   (if __robot_x (setq _robot_x __robot_x)) _robot_x)
  (:robot_y
   (&optional __robot_y)
   (if __robot_y (setq _robot_y __robot_y)) _robot_y)
  (:robot_dir
   (&optional __robot_dir)
   (if __robot_dir (setq _robot_dir __robot_dir)) _robot_dir)
  (:serialization-length
   ()
   (+
    ;; uint32 _robot_x
    4
    ;; uint32 _robot_y
    4
    ;; uint32 _robot_dir
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _robot_x
       (write-long _robot_x s)
     ;; uint32 _robot_y
       (write-long _robot_y s)
     ;; uint32 _robot_dir
       (write-long _robot_dir s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _robot_x
     (setq _robot_x (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _robot_y
     (setq _robot_y (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _robot_dir
     (setq _robot_dir (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get robot::board :md5sum-) "ef7ee7650d05aecc708d6053f43fabfb")
(setf (get robot::board :datatype-) "robot/board")
(setf (get robot::board :definition-)
      "uint32 robot_x
uint32 robot_y
uint32 robot_dir
")



(provide :robot/board "ef7ee7650d05aecc708d6053f43fabfb")


