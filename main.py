import numpy as np
import prettytable
def max_row_norms (matrix):
    return np.max(np.sum(np.abs(matrix), axis=1))
print("Введите размерность квадратной матрицы:")
n = int(input())
delta = 10**(-8)
rtol = 10**(-6)
##example = [1, 2, 3, 4, 5, 6]
proper_number_list = list(np.random.randn(1, n) * 100)[0]
matrix_Proper = np.diag(proper_number_list) ## создание диагональной матрицы
while True:
    random_matrix = np.random.randn(n, n) * 100
    if np.linalg.det(random_matrix) != 0:
        break
##print(random_matrix)
A = np.linalg.inv(random_matrix) @ matrix_Proper @ random_matrix ## создание рабочей матрицы A
##A = [[ 75.3291527, -5.82315345,  -9.31919342], [  1.78970067,  35.9243854,  -37.51167932], [  6.26172701, -11.16629923,  95.59824119]]

def Power_law_method(n, A, rtol, delta):
    y_0 = [1] * n  ## задаём начальный вектор
    z_0 = [y_0[i] / max(y_0) for i in range(n)]  ## нормировка (хотя для выбранного вектора это ненужно)
    z_old = np.array(z_0)
    q_old = np.array([y_0[i] / z_old[i] for i in range(n) if abs(z_old[i]) > delta])
    k = 0
    ## Быть внимательным с оператором @.
    # Я проверил, он очень умный
    # (умеет сам транспонировать матрицы (как минимум одномерные вектора),
    # поэтому надо быть аккуратным)
    while True:
        k += 1
        y = A @ z_old  ## Шаг 2
        z_k = np.array([y[i] / max(y) for i in range(n)])
        q_k = []
        # q_k = np.array([y[i]/z_old[i] for i in range(n) if abs(z_old[i]) > delta])      # Шаг 3
        for i in range(n):
            if abs(z_old[i]) > delta:
                q_k.append(y[i] / z_old[i])
            else:
                q_k.append(0)
        q_k = np.array(q_k)
        if max(abs(q_k - q_old)) <= rtol * max(max(abs(q_k)), max(abs(q_old))):  # Проверка на сходимость
            break
        z_old = z_k
        q_old = q_k

    prop_num = sum(q_k) / (np.count_nonzero(q_k))
    return [prop_num, z_k]

def pribl_of_prop_number(n, A, proper_number_list, k = 20):
    step_aprox_pr = np.linspace(-max_row_norms(A), max_row_norms(A), k)

    list_of_approx_prop_numb = [[] for i in range(n)]
    temp_list = [[] for i in range(n)]
    proper_number_list = np.array(proper_number_list)

    temp_matrix = [abs(proper_number_list - step_aprox_pr[i]) for i in range(len(step_aprox_pr))]
    min_index_ap = np.argmin(temp_matrix, axis=1)
    temp_matrix = np.sort(temp_matrix, axis=1)
    for i in range(len(step_aprox_pr)):
        if temp_matrix[i][0] != temp_matrix[i][1]:
            list_of_approx_prop_numb[min_index_ap[i]].append(step_aprox_pr[i])
            temp_list[min_index_ap[i]].append(abs(proper_number_list[min_index_ap[i]] - step_aprox_pr[i]) /
                                              max(abs(proper_number_list - step_aprox_pr[i])))
    best_approx = [list_of_approx_prop_numb[i][np.argmin(temp_list[i])] for i in range(n)]
    if len(set(min_index_ap)) < 3:
        return pribl_of_prop_number(n, A, proper_number_list, k + 100)
    else:
        return best_approx




result_power_law_method = Power_law_method(n, A, rtol, delta)
initial_shift = pribl_of_prop_number(n, A, proper_number_list, 50)
print("Результат первого метода:")
print(result_power_law_method[0], result_power_law_method[1])
print(f"\nсобственные числа:{proper_number_list}")
print(f"приближения:{initial_shift}")

answer = []
## Это обратный степенной метод
for i in range(n):
    z_old = [1] * n
    sig_old = initial_shift[i]
    mu_old = np.array([1] * n)
    w = 0
    while w != 10000:
        w += 1
        if np.linalg.det(A - sig_old * np.eye(n)) == 0:
                sig_old += 1e-20
        y_k = np.linalg.solve(A - sig_old * np.eye(n), z_old)
        z_k = y_k/max(abs(y_k))
        mu_k = []
        for i in range(n):
            if abs(y_k[i]) > delta:
                mu_k.append(z_old[i]/y_k[i])
            else: mu_k.append(0)
        mu_k = np.array(mu_k)
        sig_k = sig_old + sum(mu_k)/np.count_nonzero(mu_k)
        if abs(sig_k - sig_old) < 1e-6 and max(abs(z_k-z_old)) < 1e-6:
            break
        # if max(abs(mu_k - mu_old)) <= rtol * min(max(abs(mu_k)), max(abs(mu_old))):  # Проверка на сходимость
        #     answer.append([sig_k, z_k])
        #     break
        z_old = z_k
        sig_old = sig_k
        mu_old = mu_k
    answer.append([sig_k, z_k])
##

proper_vec_num = np.linalg.eig(A)

for i in range(n):
    print(f"Собственное число_{i+1}: {answer[i][0]}")
    print(f"Собственный вектор_{i+1}: {answer[i][1]}")
    print(f"Произведение Ax = lam * x: {A @ answer[i][1]} = {answer[i][0] * answer[i][1]}\n")

##print(proper_vec_num)
k = 0
prop_vec = 0

# for i in range(n):
#     if abs(answer[i][0] - proper_number_list[0]) < 1e-5:
#         k += 1
#     if abs(answer[i][0] - )

for i in range(n):
    print(f"Встроенный соб. число_{i+1}: {proper_vec_num[0][i]}")
    print(f"Встроенный соб. вектор{i+1}: {proper_vec_num[1][i]}")
    print(f"Произведение Ax = lam * x: {proper_vec_num[1][i] @ A} = {proper_vec_num[0][i] * proper_vec_num[1][i]}")


