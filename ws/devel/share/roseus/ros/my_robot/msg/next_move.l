;; Auto-generated. Do not edit!


(when (boundp 'my_robot::next_move)
  (if (not (find-package "MY_ROBOT"))
    (make-package "MY_ROBOT"))
  (shadow 'next_move (find-package "MY_ROBOT")))
(unless (find-package "MY_ROBOT::NEXT_MOVE")
  (make-package "MY_ROBOT::NEXT_MOVE"))

(in-package "ROS")
;;//! \htmlinclude next_move.msg.html


(defclass my_robot::next_move
  :super ros::object
  :slots (_x _y _dir ))

(defmethod my_robot::next_move
  (:init
   (&key
    ((:x __x) 0)
    ((:y __y) 0)
    ((:dir __dir) 0)
    )
   (send-super :init)
   (setq _x (round __x))
   (setq _y (round __y))
   (setq _dir (round __dir))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:dir
   (&optional __dir)
   (if __dir (setq _dir __dir)) _dir)
  (:serialization-length
   ()
   (+
    ;; uint32 _x
    4
    ;; uint32 _y
    4
    ;; uint32 _dir
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _x
       (write-long _x s)
     ;; uint32 _y
       (write-long _y s)
     ;; uint32 _dir
       (write-long _dir s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _x
     (setq _x (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _y
     (setq _y (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _dir
     (setq _dir (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get my_robot::next_move :md5sum-) "6be196b93b60b5075636cca4033ccd62")
(setf (get my_robot::next_move :datatype-) "my_robot/next_move")
(setf (get my_robot::next_move :definition-)
      "uint32 x
uint32 y
uint32 dir
")



(provide :my_robot/next_move "6be196b93b60b5075636cca4033ccd62")


