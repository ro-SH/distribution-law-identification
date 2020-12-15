import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import tkinter as tk
from tkinter.ttk import Combobox


TITLE = "Идентификация закона распределения"
CHOOSE_TEXT = "Выберите файл"
INTERVAL_FUNCTION_TEXT = "Формула интервала:"
STURGES = "Формула Стержеса"
BROOKS = "Формула Брукса"
HEINHOLD = "Формула Хайнхольда"
LOAD_TEXT = "Загрузить"
INTERVAL_TEXT = "Количество интервалов:"
AVERAGE_TEXT = "Среднее значение:"
STANDART_DEVIATION_TEXT = "Среднее отклонение:"
SKEWNESS_TEXT = "Асимметрия:"
KURTOSIS_TEXT = "Эксцесс:"


class MainWindow:

    def __init__(self, master):
        self.master = master
        self.master.title(TITLE)

        for i in range(6):
            self.master.rowconfigure(i, pad=5)

        for i in range(4):
            self.master.columnconfigure(i, pad=10)

        # Результаты измерений
        self.measurements = list()

        # Количество интервалов
        self.intervals_number = tk.IntVar()

        # Среднее значение
        self.average = tk.DoubleVar()

        # Среднеквадратичное отклонение
        self.standard_deviation = tk.DoubleVar()

        # Асимметрия
        self.skewness = tk.DoubleVar()

        # Эксцесс
        self.kurtosis = tk.DoubleVar()

        # Путь к файлу
        self.filepath = tk.StringVar()

        # Поле для пути к файлу
        self.filepath_field = tk.Entry(master, width=75, textvariable=self.filepath)
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
        self.interval_combo.grid(row=1, column=2)

        # Кнопка загрузки данных
        self.load_button = tk.Button(master, text=LOAD_TEXT, command=self.read_file)
        self.load_button.grid(row=2, column=1, columnspan=2)

        # Количество интервалов
        self.interval_text = tk.Label(master, text=INTERVAL_TEXT)
        self.interval_text.grid(row=3, column=0, sticky=tk.E)
        self.interval_value = tk.Label(master, textvariable=self.intervals_number)
        self.interval_value.grid(row=3, column=1, sticky=tk.W)

        # Среднее значение
        self.average_text = tk.Label(master, text=AVERAGE_TEXT)
        self.average_text.grid(row=4, column=0, sticky=tk.E)
        self.average_value = tk.Label(master, textvariable=self.average)
        self.average_value.grid(row=4, column=1, sticky=tk.W)

        # Среднеквадратичное отклонение
        self.standard_deviation_text = tk.Label(master, text=STANDART_DEVIATION_TEXT)
        self.standard_deviation_text.grid(row=4, column=2, sticky=tk.E)
        self.standard_deviation_value = tk.Label(master, textvariable=self.standard_deviation)
        self.standard_deviation_value.grid(row=4, column=3, sticky=tk.W)
    
        # Асимметрия
        self.skewness_text = tk.Label(master, text=SKEWNESS_TEXT)
        self.skewness_text.grid(row=5, column=0, sticky=tk.E)
        self.skewness_value = tk.Label(master, textvariable=self.skewness)
        self.skewness_value.grid(row=5, column=1, sticky=tk.W)

        # Эксцесс
        self.kurtosis_text = tk.Label(master, text=KURTOSIS_TEXT)
        self.kurtosis_text.grid(row=5, column=2, sticky=tk.E)
        self.kurtosis_value = tk.Label(master, textvariable=self.kurtosis)
        self.kurtosis_value.grid(row=5, column=3, sticky=tk.W)

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
        result = scipy.stats.describe(self.measurements, ddof=1, bias=False)
        self.average.set(result.mean)
        self.standard_deviation.set(result.variance ** 0.5)
        self.skewness.set(result.skewness)
        self.kurtosis.set(result.kurtosis)

        # Количество интервалов
        if self.interval_combo.get() == STURGES:
            # По формуле Старджеса m=3.3 lgn + 1 (с округлением вверх)
            self.intervals_number.set(math.ceil(3.3 * np.log10(len(self.measurements)) + 1))
        elif self.interval_combo.get() == BROOKS:
            # По формуле Брука m=5 lgn (с округлением вверх)
            self.intervals_number.set(math.ceil(5 * np.log10(len(self.measurements))))
        else:
            # По формуле Хайнхольда m=5 lgn (с округлением вверх)
            self.intervals_number.set(math.ceil(math.sqrt(len(self.measurements))))

        # Вывод гистограммы распределения
        plt.hist(self.measurements, self.intervals_number.get())
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()