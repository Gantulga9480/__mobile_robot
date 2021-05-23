;; Auto-generated. Do not edit!


(when (boundp 'my_robot::board_cmd)
  (if (not (find-package "MY_ROBOT"))
    (make-package "MY_ROBOT"))
  (shadow 'board_cmd (find-package "MY_ROBOT")))
(unless (find-package "MY_ROBOT::BOARD_CMD")
  (make-package "MY_ROBOT::BOARD_CMD"))

(in-package "ROS")
;;//! \htmlinclude board_cmd.msg.html


(defclass my_robot::board_cmd
  :super ros::object
  :slots (_reset ))

(defmethod my_robot::board_cmd
  (:init
   (&key
    ((:reset __reset) nil)
    )
   (send-super :init)
   (setq _reset __reset)
   self)
  (:reset
   (&optional __reset)
   (if __reset (setq _reset __reset)) _reset)
  (:serialization-length
   ()
   (+
    ;; bool _reset
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _reset
       (if _reset (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _reset
     (setq _reset (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get my_robot::board_cmd :md5sum-) "ba4b0b221fb425ac5eaf73f71ae34971")
(setf (get my_robot::board_cmd :datatype-) "my_robot/board_cmd")
(setf (get my_robot::board_cmd :definition-)
      "bool reset

")



(provide :my_robot/board_cmd "ba4b0b221fb425ac5eaf73f71ae34971")


