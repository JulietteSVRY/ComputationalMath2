import math
from tabulate import tabulate
import warnings
import colors as color
warnings.filterwarnings("ignore", category=RuntimeWarning)


class Input:
    type_equation = 0
    type_method = 0
    type_input = 0
    a = 0
    b = 0
    accuracy = 0
    file_name = "file_name"

    def __init__(self, type_equation):
        self.type_equation = type_equation
        self.choose_boundaries()
        self.choose_accuracy()
        self.calculation()

    def choose_boundaries(self):
        while True:
            try:
                print(color.UNDERLINE + color.YELLOW, "Выберите формат ввода границ:", color.END)
                print('\t', "1. Файл", '\n',
                      '\t', "2. Консоль")
                self.type_input = int(input("Формат ввода: ").strip())

                if self.type_input == 1:
                    print(color.UNDERLINE + color.YELLOW, "Вы выбрали формат ввода границ через файл.", color.END)
                    print(color.BOLD + color.YELLOW, "Формат файла:", color.END)
                    print('\t', "1 строка: с границами выбранного сегмента, например: -10 10", '\n',
                          '\t', "2 строка: кол-во знаков после запятой для подсчета решения, например: 3")
                    print(color.BOLD + color.YELLOW,
                          "Введите полный путь к файлу, например (H://1/DOWNLOAND/report.txt)", color.END)
                    self.file_name = input("Путь: ")
                    if answers_fun(self.type_equation, float(self.get_data_from_file()[0][0]),
                                   float(self.get_data_from_file()[0][1])) == 1:
                        self.a = float(self.get_data_from_file()[0][0])
                        self.b = float(self.get_data_from_file()[0][1])
                        print("Промежуток: [", self.a, ",", self.b, "]")
                        break
                    elif answers_fun(self.type_equation, float(self.get_data_from_file()[0][0]),
                                     float(self.get_data_from_file()[0][1])) == 0:
                        print(color.BOLD + color.RED,
                              "На промежутке нет корней, попробуйте выбрать другой промежуток!", color.END)
                        continue
                    else:
                        print(color.BOLD + color.RED,
                              "На промежутке находится несколько корней, Попробуйте выбрать другой промежуток!",
                              color.END)
                        continue

                elif self.type_input == 2:
                    print(color.UNDERLINE + color.YELLOW, "Вы выбрали формат ввода границ через консоль.", color.END)
                    print(color.BOLD + color.YELLOW, "Формат ввода границ сегмента, например: -10 10", color.END)
                    segment = list(input("Введите границы сегмента: ").split())
                    if len(segment) == 2 and float(segment[0].strip()) < float(segment[1].strip()):
                        if answers_fun(self.type_equation, float(segment[0].strip()), float(segment[1].strip())) == 1:
                            self.a = float(segment[0].strip())
                            self.b = float(segment[1].strip())
                            break
                        elif answers_fun(self.type_equation, float(segment[0].strip()), float(segment[1].strip())) == 0:
                            print(color.BOLD + color.RED,
                                  "На промежутке нет корней, попробуйте выбрать другой промежуток!", color.END)
                            continue
                        elif answers_fun(self.type_equation, float(segment[0].strip()),
                                         float(segment[1].strip())) == "inf":
                            print(color.BOLD + color.RED,
                                  "Промежуток попадает на участок, где функция не определена! Поменяйте промежуток.",
                                  color.END)
                            continue

                        else:
                            print(color.BOLD + color.RED,
                                  "На промежутке находится несколько корней, Попробуйте выбрать другой промежуток!",
                                  color.END)
                            continue
                    else:
                        get_ready_answer(1)
                        continue
            except ValueError:
                get_ready_answer(1)
            except TypeError:
                get_ready_answer(1)

    def choose_accuracy(self):
        while True:
            try:
                if self.type_input == 1:
                    if float(self.get_data_from_file()[1][0]) <= 0:
                        get_ready_answer(1)
                        continue
                    else:
                        self.accuracy = float(self.get_data_from_file()[1][0])
                        print("Точность: ", self.accuracy)
                        break
                elif self.type_input == 2:
                    print(color.UNDERLINE + color.YELLOW, "Введите кол-во знаков после запятой для подсчета решения.",
                          color.END)
                    accuracy = float(input("Точность: ").strip())
                    if accuracy <= 0:
                        get_ready_answer(1)
                        continue
                    else:
                        self.accuracy = accuracy
                        break
            except ValueError:
                get_ready_answer(1)
            except TypeError:
                get_ready_answer(1)

    def calculation(self):
        while True:
            try:
                calculator = MathMethodLogic(self.type_equation, self.a, self.b, self.accuracy)
                while True:
                    print(color.BOLD + color.YELLOW, "Выберите метод решения:", color.END)
                    print('\t', "1. Метод деления пополам", '\n',
                          '\t', "2. Метод хорд")
                    type_method = int(input("Тип метода (цифра): ").strip())
                    if type_method == 1:
                        calculator.calc_method_bisection()
                        calculator.print_table(1)
                        break
                    elif type_method == 2:
                        calculator.calc_method_chord()
                        if calculator.status == 0:
                            calculator.print_table(2)
                        break
                    else:
                        get_ready_answer(1)
                        continue

                print_result(calculator)
                while True:
                    print("Сохранить вывод в файл?")
                    print('\t', "• Да", '\n',
                          '\t', "• Нет")
                    type_output = input("Введите да/нет: ").strip()
                    if type_output.lower() == "да":
                        with open("output.txt", "w") as file:
                            if type_method == 1:
                                calculator.bisection_table.insert(0, ["№ шага", "a", "b", "x", "f(a)", "f(b)", "f(x)",
                                                                      "|a-b|"])
                                file.write(tabulate(calculator.bisection_table, tablefmt="grid"))
                            elif type_method == 2:
                                calculator.chord_table.insert(0, ["№ итерации", "a", "b", "x", "f(a)", "f(b)",
                                                                  "f(x)", "|a-b|"])
                                file.write(tabulate(calculator.chord_table, tablefmt="grid"))
                            break
                    elif type_output.lower() == "нет":
                        break

                del calculator
                break
            except ValueError:
                get_ready_answer(1)
            except TypeError:
                get_ready_answer(5)

    def get_data_from_file(self):
        try:
            with open(self.file_name) as f:
                data = [list(map(float, row.split())) for row in f.readlines()]
                return data
        except FileNotFoundError:
            get_ready_answer(2)


class MathMethodLogic:
    previous_count = 0
    x0 = 0
    x1 = 0
    lambda_param = 0
    status = 0
    solvable = 1
    type_equation = 0
    type_solver = 0
    a = 0
    b = 0
    steps = 0
    accuracy = 0
    result = 0
    segments = []
    bisection_table = []
    chord_table = []

    def __init__(self, type_equation, a, b, accuracy):
        self.type_equation = type_equation
        self.a = a
        self.b = b
        self.accuracy = accuracy
        self.segments = []
        self.steps = 0
        self.solvable = 1
        self.status = 0
        self.previous_count = 0
        self.result = 0
        self.accuracy = math.pow(10, -1 * accuracy)
        self.x0 = a
        self.x1 = b

    def calc_method_bisection(self):
        self.bisection_table = []
        self.type_solver = 1
        self.steps = 0
        if abs(self.a - self.b) > self.accuracy:
            while True:
                self.steps += 1
                x = (self.a + self.b) / 2
                self.bisection_table.append(
                    [self.steps, self.a, self.b, x,
                     self.function(self.a), self.function(self.b), self.function(x),
                     abs(self.a - self.b)]
                )
                count_x = [x]
                self.segments.append(count_x)
                if self.function(self.a) * self.function(x) < 0:
                    self.b = x
                else:
                    self.a = x
                if abs(self.a - self.b) <= self.accuracy:
                    self.steps += 1
                    x = (self.a + self.b) / 2
                    self.result = x
                    self.bisection_table.append(
                        [self.steps, self.a, self.b, x,
                         self.function(self.a), self.function(self.b), self.function(x),
                         abs(self.a - self.b)]
                    )
                    break
        else:
            self.status = 2
            print_result(self)

    def calc_method_chord(self):
        self.chord_table = []
        self.type_solver = 2
        self.result = self.a - ((self.b - self.a) * self.function(self.a)) / (self.function(self.b) -
                                                                              self.function(self.a))
        if self.a <= self.result <= self.b:
            self.chord_table.append(
                [self.steps, self.a, self.b, self.result, self.function(self.a), self.function(self.b),
                 self.function(self.result)])
            while True:
                self.steps += 1
                self.segments.append([self.result, self.function(self.result)])
                self.do_method_chord()
                if abs(self.function(self.result)) <= self.accuracy or abs(
                        self.result - self.previous_count) <= self.accuracy:
                    self.result = round(self.result, 8)
                    self.status = 0
                    break
                elif self.steps >= 2500000:
                    self.status = 1
                    break
                elif not (self.a <= self.result <= self.b):
                    self.status = 5
                    break
        else:
            self.status = 5

    def function(self, x):
        try:
            if self.type_equation == 1:
                return math.pow(x, 2) - 3
            elif self.type_equation == 2:
                return 5 / x - 2 * x
            elif self.type_equation == 3:
                return math.exp(2 * x) - 2
            elif self.type_equation == 4:
                return -1.8 * math.pow(x, 3) - 2.94 * math.pow(x, 2) + 10.37 * x + 5.38
        except ZeroDivisionError:
            return self.function(x + 1e-8)
        except OverflowError:
            self.status = 3

    def first_derivative(self, x):
        try:
            if self.type_equation == 1:
                return 2 * x
            elif self.type_equation == 2:
                return -5 * math.pow(x, -2) - 2
            elif self.type_equation == 3:
                return 2 * math.exp(2 * x)
            elif self.type_equation == 4:
                return -5.4 * math.pow(x, 2) - 5.88 * x + 10.37
        except ZeroDivisionError:
            return self.first_derivative(x + 1e-8)

    def second_derivative(self, x):
        try:
            if self.type_equation == 1:
                return 2
            elif self.type_equation == 2:
                return 10 * math.pow(x, -3)
            elif self.type_equation == 3:
                return 4 * math.exp(2 * x)
            elif self.type_equation == 4:
                return -10.8 * x - 5.88
        except ZeroDivisionError:
            return self.second_derivative(x + 1e-8)

    def select_approximation(self):
        if (self.function(self.a) * self.second_derivative(self.a)) > 0:
            return self.a
        elif (self.function(self.b) * self.second_derivative(self.b)) > 0:
            return self.b

    def function_1(self, x):
        try:
            if self.type_equation == 1:
                return 3 * math.pow(x, 2) - 1
            elif self.type_equation == 2:
                return -5 / (math.pow(x, 2)) - 2
            elif self.type_equation == 3:
                return 2 * math.pow(math.e, 2 * x)
            elif self.type_equation == 4:
                return 4.45 * 3 * math.pow(x, 2) + 2 * 7.81 * x - 9.62
        except ZeroDivisionError:
            return self.function_1(x + 1e-8)
        except OverflowError:
            self.status = 3

    def function_2(self, x):
        try:
            if self.type_equation == 1:
                return 6 * x
            elif self.type_equation == 2:
                return 10 / (math.pow(x, 3))
            elif self.type_equation == 3:
                return 4 * math.pow(math.e, 2 * x)
            elif self.type_equation == 4:
                return 4.45 * 6 * x + 2 * 7.81
        except ZeroDivisionError:
            return self.function_2(x + 1e-8)
        except OverflowError:
            self.status = 3

    def do_method_chord(self):
        try:
            count = self.result
            self.result = self.result - ((self.a - self.result) * self.function(self.result)) / (
                    self.function(self.a) - self.function(self.result))
            self.previous_count = count
            if self.function(self.a) * self.function(self.result) < 0:
                self.b = self.result
            elif self.function(self.result) * self.function(self.b) < 0:
                self.a = self.result
            self.chord_table.append(
                [self.steps, self.a, self.b, self.result, self.function(self.a), self.function(self.b),
                 self.function(self.result), abs(self.a - self.b)])
        except ValueError:
            self.result = self.result - ((self.a - self.result) * self.function(self.result)) / (
                    self.function(self.a) - self.function(self.result))
        except TypeError:
            self.result = self.result - ((self.a - self.result) * self.function(self.result)) / (
                    self.function(self.a) - self.function(self.result))
        except ZeroDivisionError:
            self.result = self.result - ((self.a - self.result) * self.function(self.result + 1e-8)) / (
                    self.function(self.a) - self.function(self.result + 1e-8))

    def print_table(self, type_table):
        if type_table == 1:
            print(color.BOLD + color.YELLOW, "Метод деления пополам:", color.END)
            print(tabulate(self.bisection_table, headers=["№ шага", "a", "b", "x", "f(a)", "f(b)", "f(x)", "|a-b|"],
                           tablefmt="grid", floatfmt="2.5f"))
        elif type_table == 2:
            print(color.BOLD + color.YELLOW, "Метод хорд:", color.END)
            print(tabulate(self.chord_table,
                           headers=["№ итерации", "a", "b", "x", "f(a)", "f(b)", "f(x)", "|a-b|"],
                           tablefmt="grid", floatfmt="2.5f"))


def get_ready_answer(type_answer):
    answers = {
        1: color.BOLD + color.RED + "Неправильный ввод!" + color.END,
        2: color.BOLD + color.RED + "Файл не найден!" + color.END,
        3: color.BOLD + color.RED + "Нет решений." + color.END,
        4: color.BOLD + color.RED + "Конкретного решения нет, или его не существует!" + color.END,
        5: color.BOLD + color.RED + "Условие сходимости на выбранном отрезке не выполнено!" + color.END,
        6: color.BOLD + color.RED + "Количество итераций слишком большое, решение не было найдено!" + color.END,
        7: color.BOLD + color.RED + "Начальное приближение было выбрано плохо, решение не было найдено!" + color.END
    }
    print(answers.get(type_answer, color.BOLD + color.RED + "Неправильный выбор готового ответа!" + color.END))


def print_result(calculator):
    if calculator.solvable == 1:
        if calculator.status == 0:
            print()
            print(color.YELLOW + "Корень уравнения: " + color.END, calculator.result)
            print(color.YELLOW + "Количество итераций: " + color.END, calculator.steps)
            print(color.YELLOW + "Точность ответа: " + color.END, calculator.accuracy)
            print(color.YELLOW + "Значение f(x) в корне: " + color.END,
                  calculator.function(calculator.result))
            if calculator.type_solver == 3:
                print(color.YELLOW + "Значение \u03C6(x) в корне: " + color.END,
                      calculator.result + calculator.lambda_param * calculator.function(calculator.result))
    else:
        get_ready_answer(3)


def answers_fun(type_equation, a, b):
    equations_answers = {
        1: [-1.732, 1.732],
        2: [-1.581, 1.581],
        3: [0.347],
        4: [-3.158, -0.474, 1.998]
    }
    if type_equation == 1:
        if a < equations_answers.get(type_equation)[0] and equations_answers.get(type_equation)[1] < b:
            return 2
        elif a > equations_answers.get(type_equation)[0] and equations_answers.get(type_equation)[1] > b:
            return 0
        else:
            return 1
    elif type_equation == 2:
        if a < equations_answers.get(type_equation)[0] and equations_answers.get(type_equation)[1] < b:
            return 2
        elif a > equations_answers.get(type_equation)[0] and equations_answers.get(type_equation)[1] > b:
            return 0
        elif a < 0 < b:
            return "inf"
        else:
            return 1
    elif type_equation == 3:
        if a > equations_answers.get(type_equation)[0] or equations_answers.get(type_equation)[0] > b:
            return 0
        else:
            return 1
    elif type_equation == 4:
        if (a < equations_answers.get(type_equation)[0] and equations_answers.get(type_equation)[2] < b) or (
                a < equations_answers.get(type_equation)[0] and equations_answers.get(type_equation)[1] < b) or (
                a < equations_answers.get(type_equation)[1] and equations_answers.get(type_equation)[2] < b):
            return 2
        elif b < equations_answers.get(type_equation)[0] or a > equations_answers.get(type_equation)[2] or (
                a > equations_answers.get(type_equation)[0] and b < equations_answers.get(type_equation)[1]) or (
                a > equations_answers.get(type_equation)[1] and b < equations_answers.get(type_equation)[2]):
            return 0
        else:
            return 1
