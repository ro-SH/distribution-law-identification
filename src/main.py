import math
import matplotlib.pyplot as plt
import scipy.stats
import tkinter as tk
from tkinter.ttk import Combobox


ROUND_COEF = 15

# Для вывода на UI
TITLE = "Идентификация закона распределения"
CHOOSE_TEXT = "Выберите файл"
INTERVAL_FUNCTION_TEXT = "Формула интервала:"
STURGES = "Формула Стержеса"
BROOKS = "Формула Брукса"
HEINHOLD = "Формула Хайнхольда"
LOAD_TEXT = "Загрузить"
INTERVAL_TEXT = "Количество интервалов:"
AVERAGE_TEXT = "Среднее значение:"
STANDART_DEVIATION_TEXT = "Среднеквадратичное отклонение:"
SKEWNESS_TEXT = "Асимметрия:"
KURTOSIS_TEXT = "Эксцесс:"
CRITICAL_VALUE_SKEWNESS_COEFFICIENT = "Кр. знач. коэффициента асимметрии:"
CRITICAL_VALUE_KURTOSIS_COEFFICIENT = "Кр. знач. коэффициента эксцесса:"
RESULT = "Результат:"
POSITIVE_RESULT = "Распределение близко к нормальному!"
NEGATIVE_RESULT = "Распределение не является нормальным!"


class MainWindow:

    def __init__(self, master):
        self.master = master
        self.master.title(TITLE)

        for i in range(8):
            self.master.rowconfigure(i, pad=5)

        for i in range(4):
            self.master.columnconfigure(i, pad=10)

        # Результаты измерений
        self.measurements = list()

        # Путь к файлу
        self.filepath = tk.StringVar()

        self.filepath_field = tk.Entry(master, width=90, textvariable=self.filepath)
        self.filepath_field.grid(row=0, column=0, columnspan=3)

        # Кнопка выбора пути
        self.choose_button = tk.Button(master, text=CHOOSE_TEXT, command=self.choose_file)
        self.choose_button.grid(row=0, column=3)

        # Выбор формулы
        self.interval_function_text = tk.Label(master, text=INTERVAL_FUNCTION_TEXT)
        self.interval_function_text.grid(row=1, column=1)
        self.interval_combo = Combobox(master, values=[ 
                                                       STURGES,
                                                       BROOKS,
                                                       HEINHOLD],
                                               state="readonly")
        self.interval_combo.current(0)
        self.interval_combo.grid(row=1, column=2, sticky=tk.W)

        # Кнопка загрузки данных
        self.load_button = tk.Button(master, text=LOAD_TEXT, command=self.read_file)
        self.load_button.grid(row=2, column=0, columnspan=4)

        # Количество интервалов
        self.intervals_number = tk.IntVar()

        self.interval_text = tk.Label(master, text=INTERVAL_TEXT)
        self.interval_text.grid(row=3, column=0, sticky=tk.E)
        self.interval_value = tk.Label(master, textvariable=self.intervals_number)
        self.interval_value.grid(row=3, column=1, sticky=tk.W)

        # Среднее значение
        self.average = tk.DoubleVar()

        self.average_text = tk.Label(master, text=AVERAGE_TEXT)
        self.average_text.grid(row=4, column=0, sticky=tk.E)
        self.average_value = tk.Label(master, textvariable=self.average)
        self.average_value.grid(row=4, column=1, sticky=tk.W)

        # Среднеквадратичное отклонение
        self.standard_deviation = tk.DoubleVar()

        self.standard_deviation_text = tk.Label(master, text=STANDART_DEVIATION_TEXT)
        self.standard_deviation_text.grid(row=4, column=2, sticky=tk.E)
        self.standard_deviation_value = tk.Label(master, textvariable=self.standard_deviation)
        self.standard_deviation_value.grid(row=4, column=3, sticky=tk.W)
    
        # Асимметрия
        self.skewness = tk.DoubleVar()

        self.skewness_text = tk.Label(master, text=SKEWNESS_TEXT)
        self.skewness_text.grid(row=5, column=0, sticky=tk.E)
        self.skewness_value = tk.Label(master, textvariable=self.skewness)
        self.skewness_value.grid(row=5, column=1, sticky=tk.W)

        # Эксцесс
        self.kurtosis = tk.DoubleVar()

        self.kurtosis_text = tk.Label(master, text=KURTOSIS_TEXT)
        self.kurtosis_text.grid(row=5, column=2, sticky=tk.E)
        self.kurtosis_value = tk.Label(master, textvariable=self.kurtosis)
        self.kurtosis_value.grid(row=5, column=3, sticky=tk.W)

        # Критическое значение коэффициента асимметрии
        self.variance_d_a = tk.DoubleVar()

        self.variance_d_a_text = tk.Label(master, text=CRITICAL_VALUE_SKEWNESS_COEFFICIENT)
        self.variance_d_a_text.grid(row=6, column=0, sticky=tk.E)
        self.variance_d_a_value = tk.Label(master, textvariable=self.variance_d_a)
        self.variance_d_a_value.grid(row=6, column=1, sticky=tk.W)

        # Критическое значение коэффициента эксцесса
        self.variance_d_e = tk.DoubleVar()

        self.variance_d_e_text = tk.Label(master, text=CRITICAL_VALUE_KURTOSIS_COEFFICIENT)
        self.variance_d_e_text.grid(row=6, column=2, sticky=tk.E)
        self.variance_d_e_value = tk.Label(master, textvariable=self.variance_d_e)
        self.variance_d_e_value.grid(row=6, column=3, sticky=tk.W)

        # Результат
        self.result = tk.StringVar()

        self.result_text = tk.Label(master, text=RESULT)
        self.result_text.grid(row=7, column=1, sticky=tk.E)
        self.result_value = tk.Label(master, textvariable=self.result)
        self.result_value.grid(row=7, column=2, sticky=tk.W)

    # Выбор в диалоговом окне файла для считывания данных
    def choose_file(self):

        new_filepath = tk.filedialog.askopenfilename(defaultextension='.txt',
                  filetypes=[('Txt files','*.txt'),
                             ('All files','*.*')])
        if new_filepath:
            self.filepath.set(new_filepath)

    # Чтение данных из выбранного файла
    def read_file(self):

        try:
            with open(self.filepath.get()) as f:
                self.measurements.clear()
                for line in f.readlines():
                    self.measurements += [float(i.replace(',', '.')) for i in line.split()]
        except:
            tk.messagebox.showerror("Ошибка", "Неверные данные")
            return

        self.show_info()
    
    # Показ результатов вычислений
    def show_info(self):

        # Количество интервалов
        self.calc_intervals()

        # По результатам измерений
        result = scipy.stats.describe(self.measurements, ddof=1, bias=False)
        self.average.set(round(result.mean, ROUND_COEF))
        self.standard_deviation.set(round(result.variance ** 0.5, ROUND_COEF))
        self.skewness.set(round(result.skewness, ROUND_COEF))
        self.kurtosis.set(round(result.kurtosis, ROUND_COEF))

        # Вычисление критических значений по методичке
        self.calc_variances()

        # Результат
        self.show_result()

        # Вывод гистограммы распределения
        plt.hist(self.measurements, bins=self.intervals_number.get(), color="blue", edgecolor="black")
        plt.title("Распределение измерений")
        plt.xlabel("Значение")
        plt.ylabel("Количество измерений")
        plt.show()

    # Вычисление количества интервалов
    def calc_intervals(self):

        if self.interval_combo.get() == STURGES:
            # По формуле Старджеса m=3.3 lgn + 1 (с округлением вверх)
            self.intervals_number.set(math.ceil(3.3 * math.log10(len(self.measurements)) + 1))
        elif self.interval_combo.get() == BROOKS:
            # По формуле Брука m=5 lgn (с округлением вверх)
            self.intervals_number.set(math.ceil(5 * math.log10(len(self.measurements))))
        else:
            # По формуле Хайнхольда m=5 lgn (с округлением вверх)
            self.intervals_number.set(math.ceil(math.sqrt(len(self.measurements))))

    # Вычисление по методичке
    def calc_variances(self):

        n = len(self.measurements)

        # Дисперсия выборочной асимметрии
        variance_a = 6 * (n - 1) / (n + 1) / (n + 3)

        # Дисперсия выборочного эксцесса
        variance_e = 24 * (n - 2) * (n - 3) * n / (n - 1) / (n - 1) / (n + 3) / (n + 5)

        self.variance_d_a.set(round(3 * math.sqrt(variance_a), ROUND_COEF))
        self.variance_d_e.set(round(5 * math.sqrt(variance_e), ROUND_COEF))

    # Вывод результата по сравнению из методички
    def show_result(self):
        
        if abs(self.skewness.get()) <= 3 * self.variance_d_a.get() and abs(self.kurtosis.get()) <= self.variance_d_e.get():
            self.result.set(POSITIVE_RESULT)
            self.result_value.config(fg="green")
        else:
            self.result.set(NEGATIVE_RESULT)
            self.result_value.config(fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
