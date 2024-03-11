(setf b `(+ * / -))
(setf a b)

(defun b(oper lst_args)
  (apply oper lst_args)
  )

(defun a(num lst_opers)
  (nth num lst_opers)
  )

(apply #'(lambda(num lst_args)
	   (apply (a num a) lst_args)) `(3 (2 4)))