function lab_02()

x = load("sel.txt");
n = length(x);

fprintf("\n1.a) вычисление оценок mu и S_quad " + ...
    "математического ожидания MX и дисперсии DX соответственно\n");

% точечные оценки
mu = sum(x) / n;
S_quad = sum((x - mu) .^2) / (n - 1);

fprintf("\nmu = %.4f\n", mu);
fprintf("\nS_quad = %.4f\n", S_quad);

gamma = 0.9; % доверительный интервал

% оценка mu

fprintf("\n1.б) вычисление нижней и верхней границдля " + ...
    "gamma-доверительного интервала для математического ожидания MX\n");

% tinv - функция квантилей распределения Стьюдента
quant_St = tinv((1 + gamma) / 2, n - 1); 

lower_mu = mu - (sqrt(S_quad) * quant_St / sqrt(n));
upper_mu = mu + (sqrt(S_quad) * quant_St / sqrt(n));

fprintf("\nНижняя граница gamma-доверительного " + ...
    "интервала для mu = %.4f\n", lower_mu);
fprintf("Верхняя граница gamma-доверительного " + ...
    "интервала для mu = %.4f\n", upper_mu);
fprintf("\ngamma-доверительный интервал для mu: " + ...
    "(%.4f, %.4f)\n", lower_mu, upper_mu);

% оценка S_quad

fprintf("\n1.в) вычисление нижней и верхней границ для " + ...
    "gamma-доверительного интервала для дисперсии DX\n");

% tinv - функция квантилей распределения хи-квадрат
quant_chi1 = chi2inv((1 - gamma) / 2, n - 1);
quant_chi2 = chi2inv((1 + gamma) / 2, n - 1);

lower_sigma = S_quad * (n - 1) / quant_chi2;
upper_sigma = S_quad * (n - 1) / quant_chi1;

fprintf("\nНижняя граница gamma-доверительного интервала " + ...
    "для sigma = %.4f\n", lower_sigma);
fprintf("Верхняя граница gamma-доверительного интервала " + ...
    "для sigma = %.4f\n", upper_sigma);

fprintf("\ngamma-доверительный интервал для " + ...
    "sigma: (%.4f, %.4f)\n", lower_sigma, upper_sigma);

end
