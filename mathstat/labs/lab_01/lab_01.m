function lab_01()

x = load('sel.txt'); 

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

delta = (M_max - M_min) / m;

J = M_min : delta : M_max;

% нижняя строка таблицы интервального статистического ряда
J_table = zeros(m, 1);  

for i = 1:m-1
    J_table(i) = sum(x >= J(i) & x < J(i + 1));
    fprintf("%d. [%.3f; %.3f), кол-во элементов: %d\n", i, J(i), J(i + 1), J_table(i));
end

% последний интервал
J_table(m) = sum(x >= J(m) & x <= J(m + 1));
fprintf(" %d. [%.3f; %.3f], кол-во элементов: %d\n", m, J(m), J(m + 1), J_table(m));

fprintf("\nд) построение на одной координатной плоскости гистограммы и \n" + ...
    "графика функции плотности распределения вероятностей нормальной \n" + ...
    "случайной величины с математическим ожиданием mu и дисперсией S_quad\n");

% Гистограмма

histogram(x, m, Normalization="pdf", LineStyle='--', FaceAlpha=0.01);
hold on;

% График функции плотности нормального распределения

x_values = M_min : 1e-3 : M_max;
% normpdf - функция плотности нормального распределения
f = normpdf(x_values, mu, sqrt(S_quad));

plot(x_values, f, 'r', LineWidth=1);
grid;
xlabel("x");
ylabel('f');
legend('histogr', 'f\_density');

fprintf("\nе) построение на другой координатной плоскости графика \n" + ...
    "эмпирической функции распределения и функции распределения \n" + ...
    "нормальной случайной величины с математическим ожиданием \n" + ...
    "mu и дисперсией S_quad\n");

% Эмпирической функции распределния
x = sort(x);

t = zeros(1, n + 2);

t(1)     = x(1) - 1;
t(n + 2) = x(n) + 1;

for i = 2 : n + 1
    t(i) = x(i - 1);
end

% Значения эмпирической функции распреления
F_n = zeros(length(t), 1);

for i = 1 : length(t)
    count = 0;
    for j = 1 : n
        if x(j) < t(i)
            count = count + 1;
        end
    end
    F_n(i) = count / n;
end

figure();

plot(t, F_n, 'b', LineWidth=1);
hold on;

% График функции нормального распределения

% normсdf - функция нормального распределения
F = normcdf(x_values, mu, sqrt(S_quad));

plot(x_values, F, 'r', LineWidth=1, LineStyle='--');
grid;
xlabel("x");
ylabel('F');
legend('F\_empiric', 'F\_normal', Location='northwest');
end