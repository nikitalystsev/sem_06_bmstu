
					; задача 1
(defun _my-reverse(lst res)
  (cond ((null lst) res)
	(t (_my-reverse (cdr lst) (cons (car lst) res)))))

(defun my-reverse(lst)
  (_my-reverse lst nil))

					; задача 2
(defun get_first_noempt_lst(lst)
  (cond ((null lst) nil)
	((and (listp (car lst)) (> (length (car lst)) 0)) (car lst))
	(t (get_first_noempt_lst (cdr lst)))))

					; задача 3
(defun select_between1(a b lst)
  (cond ((null lst) nil)
	((and (numberp (car lst)) (> (car lst) a) (< (car lst) b))
	 (cons (car lst) (select_between1 a b (cdr lst))))
	((atom (car lst)) (select_between1 a b (cdr lst)))
	(t (select_between1 a b (car lst)))))

					; задача 4
(defun mul_list_by_num(n lst) ; все элементы списка - числа
  (cond ((null lst) nil)
	(t (cons (* (car lst) n) (mul_list_by_num n (cdr lst))))))

(defun _mul_list_by_num2(n lst res) ; все элементы списка - любые объекты
    (cond ((null lst) res)
          ((numberp (car lst)) (_mul_list_by_num2  n (cdr lst) (cons (* (car lst) n) res)))
          ((atom (car lst)) (_mul_list_by_num2 n (cdr lst) (cons (car lst) res)))
          (t (_mul_list_by_num2 n (cdr lst) (cons (_mul_list_by_num2 n (car lst) ()) res)))))

(defun mul_list_by_num2(n lst)
  (reverse (_mul_list_by_num2 n lst ())))

					; задача 5
					; то же самое, что и 3-я

					; задача 6
(defun rec-add(lst) ; одноуровнего смешанного
  (cond ((null lst) 0)
	((numberp (car lst))
	 (+ (car lst) (rec-add (cdr lst))))
	(t (rec-add (cdr lst)))))

(defun _rec-add2(lst end_sum); структурированного
  (cond ((null lst) end_sum)
	((numberp (car lst)) (_rec-add2 (cdr lst) (+ (car lst) end_sum)))
	((atom (car lst)) (_rec-add2 (cdr lst) end_sum))
	(t (_rec-add2 (cdr lst) (_rec-add2 (car lst) end_sum)))))

(defun rec-add2(lst)
  (_rec-add2 lst 0))

					; задача 7
(defun _recnth(n lst ind)
  (cond ((null lst) nil)
	((= ind n) (car lst))
	(t (_recnth n (cdr lst) (+ ind 1)))))

(defun recnth(n lst)
  (_recnth n lst 0))

					; задача 8

(defun allodd(lst)
  (cond ((null lst) t)
	((evenp (car lst)) nil)
	(t (allodd (cdr lst)))))

					; задача 9

(defun get_first_odd(lst)
  (cond ((and (numberp lst) (oddp lst)) lst)
	((atom lst) nil)
	(t (or (get_first_odd (car lst))
	       (get_first_odd (cdr lst))))))

					; задача 10

(defun get_list_square(lst_num)
  (cond ((null lst_num) nil)
	(t (cons (* (car lst_num) (car lst_num)) (get_list_square (cdr lst_num))))))
