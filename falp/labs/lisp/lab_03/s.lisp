(defun disc(a b c)
    (- (* b b) (* 4 a c))
)

(defun cacl_quadr_equ(a b c)
    (cond ((= a 0)
        (cond ((= b 0)
            (cond ((= c 0)
                `x_any
                )
                (t 
                    `no_solutions
                )
            ))
            (t 
                (/ (- c) b)
            )
        ))
        (t 
            (cond ((< (disc a b c) 0)
                (cons (/ b (* 2 a)) (/ (sqrt (disc a b c)) a))
                )
                (t 
                    (cons (/ (+ (- b) (sqrt (disc a b c))) (* 2 a))
                        (cons (/ (- (- b) (sqrt (disc a b c))) (* 2 a)) nil)
                    )
                )
            )
        )
    )
)