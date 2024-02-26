; первое задание
; (defun feg(x)
;     (if (evenp x) 
;         x 
;     (+ x 1) 
;     )
; )

; (defun feg2(x)
;     (cond ((evenp x) x)
;         ((not (evenp x)) (+ x 1))
;     )
; )

; (defun feg3(x)
;     (cond ((evenp x) x)
;         ((oddp x) (+ x 1))
;     )
; )

; второе задание

; (defun spec_inc(x)
;     (if (> x 0)
;         (+ x 1)
;     (- x 1)
;     )
; )

; (defun spec_inc2(x)
;     (cond ((> x 0) (+ x 1))
;         ((< x 0) (- x 1))
;     )
; )


;  третье задание

; (defun get_asc_list(x y)
;     (if (> x y)
;         (cons y (cons x nil))
;     (cons x (cons y nil))
;     )
; )

;  четвертое задание

; (defun first_is_between(x y z)
;     (or (and (> x y) (< x z)) (and (> x z) (< x y)))
; )

; пятое задание (на листочке)

; шестое задание 

; (defun is_first_no_less(x y)
;     (or (>= x y))
; )

; седьмое задание (на листочке)

; только if

; (defun first_is_between2(x y z)
;     (if (> x y)
;         (< x z)
;     (> x z)
;     )
; )

; только cond

; (defun first_is_between3(x y z)
;     (cond ((> x y) (< x z))
;         ((> x z) (> x y))
;     )
; )

; девятое задание

; изначальная функция

; (defun how_alike(x y)
;     (cond ((or (= x y) (equal x y)) `the_same)
;         ((and (oddp x) (oddp y)) `both_odd)
;         ((and (evenp x) (evenp y)) `both_even)
;         (t `difference)
;     )
; )

; (defun how_alike2(x y)
;     (if (or (= x y) (equal x y))
;         `the_same
;         (if (and (oddp x) (oddp y))
;             `both_odd
;             (if (and (evenp x) (evenp y))
;                 `both_even
;             `difference
;             )
;         )
;     )
; )

; (defun how_alike3(x y)
;     (or (and (or (= x y) (equal x y)) `the_same)
;         (and (and (oddp x) (oddp y)) `both_odd)
;         (and (and (evenp x) (evenp y)) `both_even)
;         `difference
;     )
; )