
					; задача 1
(defun feg(x)
  (if (evenp x) x (+ x 1)))

(defun feg-v2(x)
  (cond ((evenp x) x)
	(t (+ x 1))))

					; задача 2
(defun spec-inc(x)
  (if (> x 0) (+ x 1) (- x 1)))

(defun spec-inc-v2(x)
  (cond ((> x 0) (+ x 1))
	(t (- x 1))))


					;  задача 3
(defun get-asc-list(x y)
  (if (> x y) (cons y (cons x nil)) (cons x (cons y nil))))

					; задача 4
(defun first-is-between(x y z)
  (or (and (> x y) (< x z)) (and (> x z) (< x y))))

					; задача 5 (на листочке)


					; задача 6
(defun is-first-no-less(x y)
  (>= x y))

					; задача 7 (на листочке)

					; задача 8


					; только if
(defun first-is-between-only-if(x y z)
  (if (> x y) (< x z) (> x z)))

					; только cond
(defun first_is_between-only-cond(x y z)
  (cond ((> x y) (< x z))
	((> x z) (> x y))))

; девятое задание

; изначальная функция

; (defun how_alike(x y)
;     (cond ((or (= x y) (equal x y)) `the_same)
;         ((and (oddp x) (oddp y)) `both_odd)
;         ((and (evenp x) (evenp y)) `both_even)
;         (t `difference)
;     )
; )

(defun how_alike-with-if(x y)
  (if (or (= x y) (equal x y)) `the_same
      (if (and (oddp x) (oddp y)) `both_odd
	  (if (and (evenp x) (evenp y)) `both_even `difference))))

(defun how_alike-with-and-or(x y)
  (or (and (or (= x y) (equal x y)) `the_same)
      (and (and (oddp x) (oddp y)) `both_odd)
      (and (and (evenp x) (evenp y)) `both_even) `difference))
