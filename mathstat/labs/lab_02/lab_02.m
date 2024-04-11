function lab_02()

x = load("sel.txt");

N = length(x);

fprintf("\n1.a) вычисление оценок mu и S_quad " + ...
    "математического ожидания MX и дисперсии DX соответственно\n");

% точечные оценки
mu = sum(x) / N;
S_quad = sum((x - mu) .^2) / (N - 1);

fprintf("\nmu = %.4f\n", mu);
fprintf("\nS_quad = %.4f\n", S_quad);

gamma = 0.9; % доверительный интервал

% оценка mu

fprintf("\n1.б) вычисление нижней и верхней границдля " + ...
    "gamma-доверительного интервала для математического ожидания MX\n");

% tinv - функция квантилей распределения Стьюдента
quant_St = tinv((1 + gamma) / 2, N - 1); 

mu_lower = mu - (sqrt(S_quad) * quant_St / sqrt(N));
mu_upper = mu + (sqrt(S_quad) * quant_St / sqrt(N));

fprintf("\nНижняя граница gamma-доверительного " + ...
    "интервала для mu = %.4f\n", mu_lower);
fprintf("Верхняя граница gamma-доверительного " + ...
    "интервала для mu = %.4f\n", mu_upper);
fprintf("\ngamma-доверительный интервал для mu: " + ...
    "(%.4f, %.4f)\n", mu_lower, mu_upper);

% оценка S_quad

fprintf("\n1.в) вычисление нижней и верхней границ для " + ...
    "gamma-доверительного интервала для дисперсии DX\n");

% tinv - функция квантилей распределения хи-квадрат
quant_chi1 = chi2inv((1 - gamma) / 2, N - 1);
quant_chi2 = chi2inv((1 + gamma) / 2, N - 1);

sigma_lower = S_quad * (N - 1) / quant_chi2;
sigma_upper = S_quad * (N - 1) / quant_chi1;

fprintf("\nНижняя граница gamma-доверительного интервала " + ...
    "для sigma = %.4f\n", sigma_lower);
fprintf("Верхняя граница gamma-доверительного интервала " + ...
    "для sigma = %.4f\n", sigma_upper);

fprintf("\ngamma-доверительный интервал для " + ...
    "sigma: (%.4f, %.4f)\n", sigma_lower, sigma_upper);

% подготовка данных для графиков 

mu_N = zeros(N, 1) + mu;
mu_n = zeros(N, 1);
mu_lower_n = zeros(N, 1);
mu_upper_n = zeros(N, 1);

S_quad_N = zeros(N, 1) + S_quad;
S_quad_n = zeros(N, 1);
S_quad_lower_n = zeros(N, 1);
S_quad_upper_n = zeros(N, 1);

for i = 1 : N
    mu_n(i) = sum(x(1 : i)) / i;
    S_quad_n(i) = sum((x(1 : i) - mu_n(i)) .^2) / (i - 1);

    quant_st_i = tinv((1 + gamma) / 2, i - 1);

    mu_lower_n(i) = mu_n(i) - (quant_st_i * sqrt(S_quad_n(i)) / sqrt(i));
    mu_upper_n(i) = mu_n(i) + (quant_st_i * sqrt(S_quad_n(i)) / sqrt(i)); 

    quant_chi1_i = chi2inv((1 - gamma) / 2, i - 1);
    quant_chi2_i = chi2inv((1 + gamma) / 2, i - 1);
    
    S_quad_lower_n(i) = S_quad_n(i) * (i - 1) / quant_chi2_i;
    S_quad_upper_n(i) = S_quad_n(i) * (i - 1) / quant_chi1_i;
end

fprintf('\nЗадание 3.a)\n');
fprintf('График в отдельном окне\n');

plot((1 : N), mu_N, 'r', LineWidth=1);
hold on;
plot((1 : N), mu_n, 'm--', LineWidth=1);
hold on;
plot((1 : N), mu_lower_n, 'b-o', MarkerIndices=1:5:length(mu_lower_n), LineWidth=1);
hold on;
plot((1 : N), mu_upper_n, 'k-*', MarkerIndices=1:5:length(mu_lower_n), LineWidth=1);
hold on;
grid on;
xlabel("n");
ylabel('\mu');
legend('\mu\^(x_N)', '\mu\^(x_n)', '\mu_{-}(x_n)', '\mu^{-}(x_n)');

fprintf('\nЗадание 3.б)\n');
fprintf('График в отдельном окне\n');

figure()

plot((1 : N), S_quad_N, 'r', LineWidth=1);
hold on;
plot((1 : N), S_quad_n, 'm--', LineWidth=1);
hold on;
plot((1 : N), S_quad_lower_n, 'b-o', MarkerIndices=1:5:length(mu_lower_n), LineWidth=1);
hold on;
plot((1 : N), S_quad_upper_n, 'k-*', MarkerIndices=1:5:length(mu_lower_n), LineWidth=1);
hold on;
grid on;
xlabel("n");
ylabel('\sigma');
legend('S^2(x_N)', 'S^2(x_n)', '\sigma^2_{-}(x_n)', '\sigma^{2 -}(x_n)');

end
