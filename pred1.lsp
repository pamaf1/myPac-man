(defun math ()
  (let ((average 0))
    (cl-csv:do-csv (row #P"result1.csv")
      (let ((sum 0))  
        (with-input-from-string (in (nth 3 row))
        (setq sum (read in))
        (incf average sum))
      )
    )
    (setq average (/ average 100))
    (float average)
  )
)

(defun disper ()
  (let ((average 0) (sum 0))
  (cl-csv:do-csv (row #P"result1.csv")
    (incf average (parse-integer (nth 1 row))))
  (setq average (/ average 100))
  (cl-csv:do-csv (row #P"result1.csv")
    (let ((cur 0))
      (setq cur (parse-integer (nth 1 row)))
      (setq cur (- cur average))
      (setq cur (expt cur 2))
      (incf sum cur)))
  (setq sum (/ sum 100))
  (float sum)
  )
)
