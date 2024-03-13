(setf b `(+ * / -))
(setf a `b)

(defun b(num)
  (nth num b)
  )

(defun a(num lst_args)
  (apply (b num) lst_args)
  )

(apply (funcall a 2) `(3 4))
