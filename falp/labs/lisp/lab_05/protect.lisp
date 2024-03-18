(defun f(x)
  (let ((n (eval x)))
    (cond ((> n 0)
	       (cond ((oddp n) (+ n 5))
		     (t (+ n 10))))
	      ((< n 0) (- n 5))
	      (t x))))

(defun f2(lst)
  (mapcar #'f lst))


(setf a 13)
(setf b -4)
(setf c 0)
(setf d 2)

(setf lst `(a b c d))

(fiveam:test f_test_1
	(fiveam:is (equal (f2 lst) `(18 -9 c 12))))

(setf lst2 `(a))

(fiveam:test f_test_2
  (fiveam:is (equal (f2 lst2) `(18))))

(fiveam:test f_test_3
  (fiveam:is (equal (f2 lst2) `(18))))

(fiveam::run!)
