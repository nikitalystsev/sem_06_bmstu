function lab_01()
X = load('sel.txt');
X = sort(X);
n = length(X);

fprintf("a) Вычисление максимального значения Mmax и минимального значения Mmin\n");
Mmax = max(X);
Mmin = min(X);
fprintf("\nMmax = %.4f\n", Mmax);
fprintf("\nMmin  = %.4f\n", Mmin);

fprintf("\nb) Вычисление размаха R\n");
R = Mmax - Mmin;
fprintf("\nR = %.4f\n", R);

fprintf("\nc) Вычисление оценок Mu и S_quad математического ожидания MX и дисперсии DX\n");
Mu = sum(X) / n; % Выборочное среднее
S_quad = sum((X - Mu) .^2) / (n - 1); % Исправленная выборочная дисперсия
fprintf("\nMu = %.4f\n", Mu);
fprintf("\nS_quad = %.4f\n", S_quad);

fprintf("\nd) Группировка значений выборки в m = [log2 n] + 2 интервала\n\n");
m = floor(log2(n)) + 2;
fprintf("Кол-во интервалов m = %3d\n\n", m);
delta = (X(n) - X(1)) / m;
borders = Mmin : delta : Mmax;

ni_arr = zeros(m, 1);

for i = 1:m-1
    ni_arr(i) = sum(X >= borders(i) & X < borders(i+1));
    fprintf(" %d. [%.3f; %.3f), кол-во элементов: %d\n", i, borders(i), borders(i + 1), ni_arr(i));
end

% последний интервал
ni_arr(m) = sum(X >= borders(m) & X <= borders(m+1));
fprintf(" %d. [%.3f; %.3f], кол-во элементов: %d\n", m, borders(m), borders(m + 1), ni_arr(m));

fprintf("\ne) График 1");

% Гистограмма

mid_intervals = zeros(m, 1);

for i = 1 : m
    mid_intervals(i) = (borders(i) + borders(i + 1)) / 2;
end

column_values = zeros(m, 1);

for i = 1 : m
    column_values(i) = ni_arr(i) / (n * delta);
end

% Отрисовка гистограммы
bar(mid_intervals, column_values, 1, 'b');
hold on;

% График функции плотности нормального распределения

% Набор значений
x_coords = (Mmin - 1) : 1e-3 : (Mmax + 1);

% normpdf - функция плотности нормального распределения
func_density_norm = normpdf(x_coords, Mu, sqrt(S_quad));

% Отрисовка графика плоности нормального распределения
plot(x_coords, func_density_norm, 'r', 'LineWidth', 2);
grid;

fprintf("\nd) График 2");

% Эмпирической функции распределния

t_arr = zeros(1, n + 2);

t_arr(1)     = X(1) - 1;
t_arr(n + 2) = X(n) + 1;

for ind = 2 : n + 1
    t_arr(ind) = X(ind - 1);
end

% Значения эмпирической функции распреления
func_emperic = zeros(length(t_arr), 1);

for i = 1 : length(t_arr)
    count = 0;

    for j = 1: n
        if X(j) <= t_arr(i)
            count = count + 1;
        end
    end

    func_emperic(i) = count / n;
end

figure();

% Отрисовка эмпирической функции распределения
stairs(t_arr, func_emperic, 'b', 'LineWidth', 1);
hold on;

% График функции нормального распределения

% Набор значений
x_coords = (Mmin - 1) : 1e-3 : (Mmax + 1);

% normсdf - функция нормального распределения
func_norm = normcdf(x_coords, Mu, sqrt(S_quad));

% Отрисовка графика нормального распределения
plot(x_coords, func_norm, 'r', 'LineWidth', 1);
grid;
end