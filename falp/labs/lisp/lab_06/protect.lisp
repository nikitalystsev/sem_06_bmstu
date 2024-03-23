(defun el_in_lst(el lst)
    (cond
        ((null lst) (cons el nil))
        ((< el (car lst)) (cons el lst))
        (t (cons (car lst) (el_in_lst el (cdr lst))))
    )
)

(defun mysort(lst)
    (cond
        ((null lst) nil)
        ((null (cdr lst)) lst)
        (t (el_in_lst (car lst) (mysort (cdr lst))))
    )
)

(defun one_lst (lst)
    (cond
        ((null lst) nil)
        ((atom lst) (list lst))
        (t (append (one_lst (car lst)) (one_lst (cdr lst))))
    )
)

(fiveam:test test1
  (setf b '(5 4 3 2 1))
  (fiveam:is (equalp (funcall #'mysort b) '(1 2 3 4 5))))

(fiveam:test test2
  (setf b '(10 4 -2 0 4 3))
  (fiveam:is (equalp (funcall #'mysort b) '(-2 0 3 4 4 10))))

(fiveam:test test3
  (setf b '(7 (9 0) (4 (-3) -5) -10 -6))
  (fiveam:is (equalp (funcall #'mysort (funcall #'one_lst b)) '(-10 -6 -5 -3 0 4 7 9))))

(fiveam:test test4
  (setf b '(7 (9 0 () (() ())) (4 (-3) -5) -10 (-6)))
  (fiveam:is (equalp (funcall #'mysort (funcall #'one_lst b)) '(-10 -6 -5 -3 0 4 7 9))))

(fiveam:run!)
