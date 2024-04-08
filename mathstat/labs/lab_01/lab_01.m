function lab_01()

x = load('sel.txt'); 
x = sort(x);

n = length(x);

fprintf("a) Вычисление максимального значения M_max " + ...
    "и минимального значения M_min\n");

M_max = max(x);
M_min = min(x);

fprintf("\nM_max = %.4f\n", M_max);
fprintf("M_min  = %.4f\n", M_min);

fprintf("\nб) Вычисление размаха R\n");

R = M_max - M_min;

fprintf("\nR = %.4f\n", R);

fprintf("\nв) Вычисление оценок mu и S_quad " + ...
    "математического ожидания MX и дисперсии DX\n");

mu = sum(x) / n; 
S_quad = sum((x - mu) .^2) / (n - 1); 

fprintf("\nmu = %.4f\n", mu);
fprintf("\nS_quad = %.4f\n", S_quad);

fprintf("\nг) Группировка значений выборки в m = [log2 n] + 2 интервала\n\n");

m = floor(log2(n)) + 2;

fprintf("Кол-во интервалов m = %3d\n\n", m);

delta = (x(n) - x(1)) / m;

J = M_min : delta : M_max;

Ji_arr = zeros(m, 1);

for i = 1:m-1
    Ji_arr(i) = sum(x >= J(i) & x < J(i + 1));
    fprintf(" %d. [%.3f; %.3f), кол-во элементов: %d\n", i, J(i), J(i + 1), Ji_arr(i));
end

% последний интервал
Ji_arr(m) = sum(x >= J(m) & x <= J(m + 1));
fprintf(" %d. [%.3f; %.3f], кол-во элементов: %d\n", m, J(m), J(m + 1), Ji_arr(m));

fprintf("\nд) построение на одной координатной плоскости гистограммы и \n" + ...
    "графика функции плотности распределения вероятностей нормальной \n" + ...
    "случайной величины с математическим ожиданием mu и дисперсией S_quad\n");

% Гистограмма

mid_intervals = zeros(m, 1);

for i = 1 : m
    mid_intervals(i) = (J(i) + J(i + 1)) / 2;
end

f_n = zeros(m, 1);

for i = 1 : m
    f_n(i) = Ji_arr(i) / (n * delta);
end

% Отрисовка гистограммы
bar(mid_intervals, f_n, 1, 'b');
hold on;

% График функции плотности нормального распределения
x_values = M_min : 1e-3 : M_max;
% normpdf - функция плотности нормального распределения
func_density_norm = normpdf(x_values, mu, sqrt(S_quad));
% Отрисовка графика плотности нормального распределения
plot(x_values, func_density_norm, 'r', 'LineWidth', 2);
grid;

fprintf("\nе) построение на другой координатной плоскости графика \n" + ...
    "эмпирической функции распределения и функции распределения \n" + ...
    "нормальной случайной величины с математическим ожиданием \n" + ...
    "mu и дисперсией S_quad\n");

% Эмпирической функции распределния

t = zeros(1, n + 2);

t(1)     = x(1) - 1;
t(n + 2) = x(n) + 1;

for i = 2 : n + 1
    t(i) = x(i - 1);
end

t_size = length(t);

% Значения эмпирической функции распреления
F_n = zeros(t_size, 1);

for i = 1 : t_size
    count = 0;

    for j = 1 : n
        if x(j) <= t(i)
            count = count + 1;
        end
    end

    F_n(i) = count / n;
end

figure();

% Отрисовка эмпирической функции распределения
plot(t, F_n, 'b', 'LineWidth', 1);
hold on;

% График функции нормального распределения

% Набор значений
x_values = M_min : 1e-3 : M_max;

% normсdf - функция нормального распределения
func_norm = normcdf(x_values, mu, sqrt(S_quad));

% Отрисовка графика нормального распределения
plot(x_values, func_norm, 'r', 'LineWidth', 1);
grid;
end