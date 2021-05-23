
(cl:in-package :asdf)

(defsystem "robot-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "board" :depends-on ("_package_board"))
    (:file "_package_board" :depends-on ("_package"))
    (:file "value_table" :depends-on ("_package_value_table"))
    (:file "_package_value_table" :depends-on ("_package"))
  ))