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
end