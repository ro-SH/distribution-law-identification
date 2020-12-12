import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

def main():

    # Данные из файла
    measurements = read_file("../data/A_v10c.txt")

    print(f"Количество измерений: {len(measurements)}")

    # Информация по данным
    result = scipy.stats.describe(measurements, ddof=1, bias=False)
    print(f"Среднее: {result.mean}; Среднеквадратичное отклонение: {result.variance ** 0.5};\nАсимметрия: {result.skewness}; Эксцесс: {result.kurtosis}")


    # Количество интервало по формуле Стаджерса m=3.3 lgn + 1 (с округлением вверх)
    m = math.ceil(3.3 * np.log10(len(measurements)) + 1)

    measurement_max = max(measurements)
    measurement_min = min(measurements)
    step = (measurement_max - measurement_min) / m

    y = [0 for i in range(m)]

    for item in measurements:
        if item == measurement_max:
            y[-1] +=1
        elif item == measurement_min:
            y[0] += 1
        else:
            y[math.ceil((item - measurement_min) / step) - 1] += 1

    print(f"Количество интервалов: {m}; Шаг: {step}")
    print(y)

    # Построение гистограммы
    plt.hist(measurements, m)
    plt.show()

def read_file(filename):
    y = list()
    with open(filename) as f:
        for line in f.readlines():
            y += [float(i.replace(',', '.')) for i in line.split()]
    
    return y


if __name__ == "__main__":
    main()