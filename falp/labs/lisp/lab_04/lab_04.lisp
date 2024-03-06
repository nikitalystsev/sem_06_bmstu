; задача 1

(setf lst1 `(a b c))
(setf lst2 `(d e))

(cons lst1 lst2) ;; ((A B C) D E)
(list lst1 lst2) ;; ((A B C) (D E))
(append lst1 lst2) ;; (A B C D E)

; задача 2

(reverse `(a b c)) ;; (c b a)
(reverse `(a b (c (d)))) ;; ((с (d)) b a)
(reverse `(a)) ; (a)
(last `(a b c)) ; (c) возвращает списком, лол
(last `(a)) ; (a) 
(last `((a b c))) ; ((a b c)) 
(reverse ()) ; nil 
(reverse `((a b c))) ; ((a b c)) 
(last `(a b (c))) ; ((c)) 
(last ()) ; nil 

; задача 3

(defun get_last_elem(x)
    (car (last x))
)

(defun get_last_elem2(x)
    (car (reverse x))
)

; задача 4

(defun get_list_without_last(x)
    (nreverse (cdr (reverse x)))
)

(defun get_list_without_last2(x)
    (if (cdr x)
        (cons (car x) (get_list_without_last (cdr x)))
    )
)

; задача 5

(defun swap-first-last(x)
    (let ((_first (car  x))
         (_last (car (last x))))
        (setf (car x) _last)
        (setf (car (last x)) _first)
    )
)

; задача 6

(setf *random-state* (make-random-state T))

(defun get_dice() ; функция для генерации значений игральной кости
    (list (+ (random 6) 1) (+ (random 6) 1))
)

(defun is_repeat(dice)
    (let ((_first (car dice))
          (_second (car (cdr dice))))
         (cond ((or (= _first _second 1) (= _first _second 6)) t)
               (t nil)
         )
    )
)

(defun player_actions(who)
    (let* ((_dice (get_dice))
           (_sum_dice (+ (car _dice) (car (cdr _dice)))))
          (print who)
          (print _dice)
          (cond ((or (= _sum_dice 7) (= _sum_dice 11)) `win)
                ((is_repeat _dice) (player_actions))
                (t _sum_dice)
          )
    )
)

(defun play_dice() 
    (let ((_sum_dice1 (player_actions "first")))
         (cond ((eq _sum_dice1 `win) (print "first player is winner!"))
               (t (let ((_sum_dice2 (player_actions "second")))
                       (cond ((eq _sum_dice2 `win) (print "second player is winner!"))
                             ((< _sum_dice1 _sum_dice2) (print "second player is winner!"))
                             ((> _sum_dice1 _sum_dice2) (print "first player is winner!"))
                             (t (print "draw"))
                       )
                  )
               )
         )
    )
)

; задача 7


; задача 8

(setf lst `((r . m) (u . d) (b . r) (w . q)))

(defun get_capital(table country)
    (cond ((null table) nil)
          ((eq (car (car table)) country) (cdr (car table)))
          (t (get_capital (cdr table) country))
    )
)  

(defun get_country(table capital)
    (cond ((null table) nil)
          ((eq (cdr (car table)) capital) (car (car table)))
          (t (get_country (cdr table) capital))
    )
) 

; задача 9

(setf lst3 `(a b c 3 7 8))

(defun f(n lst) ; если все элементы спикска -- числа
    (setf (car lst) (* (car lst) n))
)

(defun f2(n lst) ; если все элементы спикска -- любые обьекты
    (cond ((null lst) nil)
          (t (cond ((numberp (car lst)) (setf (car lst) (* (car lst) n)))
                (t (f2 n (cdr lst)))
             )
          )
    )
)
