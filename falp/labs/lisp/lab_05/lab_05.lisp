
					; задача 1
(defun f1-for-elem(elem)
  (cond ((numberp elem) (- elem 10))
	(t elem)))

(defun f1(lst)
  (mapcar #'f1-for-elem lst))

					; задача 2
(defun f2(lst)
  (mapcar #'(lambda(elem)
	      (cond ((numberp elem) (* elem elem))
		    (t elem))) lst))

					; задача 3
(defun f3-1(n lst)
  (mapcar #'(lambda(elem)
	      (* elem n)) lst))

(defun f3-2(n lst)
  (mapcar #'(lambda(elem)
	      (cond ((numberp elem) (* elem n))
		    (t elem))) lst))

					; задача 4
(defun cmp-list(lst1 lst2)
  (reduce #'(lambda(val1 val2)
	      (and val1 val2)) (mapcar #'eql lst1 lst2)))

(defun is-palindrome(lst)
  (apply #'(lambda(lst1 lst2)
	     (cmp-list lst1 lst2)) (list lst (reverse lst))))

					; задача 5

(defun apply-or(lst)
  (reduce #'(lambda(val1 val2)
	      (or val1 val2)) lst))

(defun apply-and(lst)
  (reduce #'(lambda(val1 val2)
	      (and val1 val2)) lst))

(defun -set-equal(lst1 lst2)
  (apply-and (mapcar #'(lambda(elem1)
	      (apply-or (mapcar #'(lambda(elem2)
	     			   (eql elem1 elem2)) lst2))) lst1)))

(defun set-equal(lst1 lst2)
  (let ((len1 (length lst1))
	(len2 (length lst2)))
    (cond ((not (= len1 len2)) nil)
	  (t (-set-equal lst1 lst2)))))

(defun _set-equal(lst1 lst2)
  (let ((inters (intersection lst1 lst2))
	(len1 (length lst1))
	(len2 (length lst2)))
    (and (= len1 len2)
	 (= len2 (length inters)))))
					; задача 6
(defun select-between(n m lst)
  (remove-if #'(lambda(elem)
		 (or (< elem n) (> elem m))) lst))

					; задача 7
(defun decart(lstX lstY)
  (mapcan #'(lambda(x)
	      (mapcar (lambda(y)
			(list x y)) lstY)) lstX))

					; задача 8
					; в отчете

					; задача 9
(defun sum-all-num(list-of-list)
  (reduce #'+ (mapcar #'(lambda(list)
			  (length list)) list-of-list)))
