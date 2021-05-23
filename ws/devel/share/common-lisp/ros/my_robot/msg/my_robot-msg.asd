
(cl:in-package :asdf)

(defsystem "my_robot-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "board" :depends-on ("_package_board"))
    (:file "_package_board" :depends-on ("_package"))
    (:file "board_cmd" :depends-on ("_package_board_cmd"))
    (:file "_package_board_cmd" :depends-on ("_package"))
    (:file "next_move" :depends-on ("_package_next_move"))
    (:file "_package_next_move" :depends-on ("_package"))
  ))