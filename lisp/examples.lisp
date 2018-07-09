(defun inlist (el lst)
	(dolist (e lst)
		(when (equal e el) (return-from inlist t)))
	nil)

(defun pow (b e)
	(if (zerop e)
	1
	(* b (pow b (- e 1)))))

(defun sum (n l)
  (if (zerop n)
    l
    (sum (- n 1) (+ l 1))))
