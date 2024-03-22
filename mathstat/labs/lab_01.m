function lab_01()
    X = load('sel.txt');

    X = sort(X);
    
    fprintf("a) Вычисление максимального значения Mmax и минимального значения Mmin\n");
    
    Mmax = max(X);
    Mmin = min(X);

    fprintf("\nMmax = %.4f\n", Mmax);
    fprintf("\nMmin  = %.4f\n", Mmin);
end