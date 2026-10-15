from s21_graph.models.models import TsmResultPython
from s21_graph.s21_graph import Graph
from s21_graph_algorithms.s21_graph_algorithms import GraphAlgorithms
import time


class S21NavigatorCLI:
    __algo = GraphAlgorithms()
    __graph: Graph | None = None

    def main_loop(self):
        while True:
            if self.__graph is None:
                if not self.__start_menu():
                    break
            else:
                if not self.__main_menu():
                    break

    @staticmethod
    def __main_menu_text():
        print("Консольное приложение для работы с графами.")
        print("На данный момент есть загруженный граф. Выберите действие:")
        print(
            '\tНажмите "1" Для перехода к загрузке другого графа в виде матрицы смежности.'
        )
        print('\tНажмите "2" Для сохранения текущего графа в формате DOT.')
        print('\tНажмите "3" Для сохранения текущего графа в формате PDF.')
        print(
            '\tНажмите "4" Выполнить обход графа в ШИРИНУ с выводом результата обхода в консоль.'
        )
        print(
            '\tНажмите "5" Выполнить обход графа в ГЛУБИНУ с выводом результата обхода в консоль.'
        )
        print(
            '\tНажмите "6" Выполнить поиск кратчайшего пути между произвольными двумя вершинами с выводом результата в консоль.'
        )
        print(
            '\tНажмите "7" Выполнить поиск кратчайших путей между всеми парами вершин в графе с выводом результирующей матрицы в консоль.'
        )
        print(
            '\tНажмите "8" Выполнить поиск минимального остовного дерева в графе с выводом результирующей матрицы смежности в консоль.'
        )
        print('\tНажмите "9" Для перехода в меню решения задачи коммивояжера.')
        print('\tНажмите "q" Для выхода.')

    def __main_menu(self):
        self.__main_menu_text()
        while True:
            temp = input()
            match temp:
                case "1":
                    if not self.__graph_loading():
                        self.__main_menu_text()
                case "2":
                    if not self.__save_graph(True):
                        self.__main_menu_text()
                case "3":
                    if not self.__save_graph(False):
                        self.__main_menu_text()
                case "4":
                    for i in range(1, self.__graph.get_vertices_count() + 1):
                        print(
                            "Со стартовой вершины "
                            + str(i)
                            + " были найдены следующие вершины (в порядке обхода):"
                        )
                        print(self.__algo.breadth_first_search(self.__graph, i))
                    print("")
                    self.__main_menu_text()
                case "5":
                    for i in range(1, self.__graph.get_vertices_count() + 1):
                        print(
                            "Со стартовой вершины "
                            + str(i)
                            + " были найдены следующие вершины (в порядке обхода):"
                        )
                        print(self.__algo.depth_first_search(self.__graph, i))
                    print("")
                    self.__main_menu_text()
                case "6":
                    self.__dijkstra_path_search()
                    self.__main_menu_text()
                case "7":
                    res = self.__algo.get_shortest_paths_between_all_vertices(
                        self.__graph
                    )
                    if res is not None:
                        print(
                            "Таблица кратчайших путей между всеми парами вершин в графе с использованием алгоритма Флойда-Уоршелла:"
                        )
                        for obj in res:
                            print(obj)
                    else:
                        print("Что-то пошло не так")
                    print("")
                    self.__main_menu_text()
                case "8":
                    res = self.__algo.get_least_spanning_tree(self.__graph)
                    if res is not None:
                        print(
                            "Минимальное остовное дерево в графе составленное с помощью алгоритма Прима:"
                        )
                        for obj in res:
                            print(obj)
                    else:
                        print("Что-то пошло не так")
                    print("")
                    self.__main_menu_text()
                case "9":
                    self.__traveling_salesman_problem()
                    self.__main_menu_text()
                case "q":
                    return False
                case _:
                    print("Некорректный ввод.")

    @staticmethod
    def __graph_loading_text():
        print("Пожалуйста, введите путь и название файла с описанием графа.")
        print("Просим убедиться, что описание соответствует следующим требованиям:")
        print("\t1. В первой строке указана размерноть графа;")
        print(
            "\t2. Граф описан в виде матрицы смежности, в качестве разделителя используется пробел;"
        )
        print("\t3. Граф ненулевой;")
        print("\t4. Граф связный;")
        print("\t5. Веса ребер - только натуральные числа.")
        print("Пример:")
        print("\t4")
        print("\t0 2 9 6")
        print("\t2 0 5 4")
        print("\t9 5 0 1")
        print("\t6 4 1 0")

    def __graph_loading(self) -> bool:
        self.__graph_loading_text()
        while True:
            temp_graph = Graph()
            if temp_graph.load_graph_from_file(input()):
                if temp_graph.check_graph_for_requirements():
                    self.__graph = temp_graph
                    return True
                else:
                    print("Некорректный граф.")
            else:
                print("Ошибка пути к файлу или ошибка файла или некорректный граф.")

            while True:
                # print("Некорректный ввод.")
                print('\tНажмите "1" Для повторной попытки ввода.')
                print('\tНажмите "q" Для выхода в меню выше.')
                temp = input()
                match temp:
                    case "1":
                        break
                    case "q":
                        return False
                    case _:
                        print("Некорректный ввод.")

    @staticmethod
    def __start_menu_text():
        print("Консольное приложение для работы с графами.")
        print("На данный момент нет загруженных графов.")
        print('\tНажмите "1" Для перехода к загрузке графа в виде матрицы смежности.')
        print('\tНажмите "q" Для выхода.')

    def __start_menu(self) -> bool:
        self.__start_menu_text()
        while True:
            temp = input()
            match temp:
                case "1":
                    if self.__graph_loading():
                        return True
                    else:
                        self.__start_menu_text()
                case "q":
                    return False
                case _:
                    print("Некорректный ввод.")

    def __save_graph(self, dot_format: bool) -> bool:
        print("Пожалуйста, введите путь и название файла для сохранения.")
        while True:
            if dot_format:
                if self.__graph.export_graph_to_dot(input()):
                    return True
                else:
                    print("Ошибка пути к файлу или ошибка файла или некорректный граф.")
            else:
                if self.__graph.export_graph_to_pdf(input()):
                    return True
                else:
                    print("Ошибка пути к файлу или ошибка файла или некорректный граф.")

            while True:
                # print("Некорректный ввод.")
                print('\tНажмите "1" Для повторной попытки ввода.')
                print('\tНажмите "q" Для выхода в меню выше.')
                temp = input()
                match temp:
                    case "1":
                        break
                    case "q":
                        return False
                    case _:
                        print("Некорректный ввод.")

    def __dijkstra_path_search(self) -> bool:
        print(
            "Пожалуйста, введите две вершины, между которыми должен быть найден путь."
        )
        print("Ваш граф имеет " + str(self.__graph.get_vertices_count()) + " вершин.")
        start: int = 0
        finish: int = 0
        while True:
            try:
                start, finish = map(int, input().split())
            except:
                while True:
                    print("Некорректный ввод.")
                    print('\tНажмите "1" Для повторной попытки ввода.')
                    print('\tНажмите "q" Для выхода в меню выше.')
                    temp = input()
                    match temp:
                        case "1":
                            break
                        case "q":
                            return False
                        case _:
                            print("Некорректный ввод.")
                continue
            break

        if (
            start < 1
            or finish < 1
            or start > self.__graph.get_vertices_count()
            or finish > self.__graph.get_vertices_count()
        ):
            print("Введенные вершины за пределами графа.")
            return False
        else:
            res = self.__algo.get_shortest_path_between_vertices_with_path(
                self.__graph, start, finish
            )
            if res is not None:
                print(
                    "Кратчайший путь из вершины "
                    + str(start)
                    + " до вершины "
                    + str(finish)
                    + " найденный алгоритмом Дейкстры займет:"
                )
                print(res.distance)
                print(res.vertices)
                return True
            else:
                print("Что-то пошло не так")
                return False

    @staticmethod
    def __traveling_salesman_problem_text():
        print("Решение задачи комивояжера.")
        print("Выбрите способ решения:")
        print("\tОтносительно точные:")
        print(
            "\tАТТЕНСЬЁН!!! Крайне не советуем пытаться так посчитать полносвязный граф более 20 вершин."
        )
        print('\t\tНажмите "1" Для решения рекурсивным перебором.')
        print('\t\tНажмите "2" Для решения алгоритмом Хелда-Карпа.')
        print("\tНи разу не точные:")
        print('\t\tНажмите "3" Для решения алгоритмом ближайшего соседа.')
        print(
            "\tНе надейтесь на оптимальное решение за один проход дальнейшими методами. При решении данными методами будет предложено ввести количество желаемых запусков. Будет выведен лучший путь."
        )
        print('\t\tНажмите "4" Для решения МУРАВЬИНЫМ алгоритмом.')
        print('\t\tНажмите "5" Для решения алгоритмом имитации отжига.')
        print(
            '\tНажмите "6" Для сравнения скорости и точности выполнения тремя эвристическими методами (будет предложено ввести количество желаемых запусков).'
        )
        print('\tНажмите "q" Для выхода в меню выше.')

    @staticmethod
    def __print_sp_result(result: TsmResultPython, res_time: float):
        print("Задача выполена за " + str(res_time) + " секунд")
        print(
            "Предложенный выбранной методой путь имеет общий вес: "
            + str(result.distance)
        )
        print("Маршрут этого пути:")
        print(result.vertices)

    def __traveling_salesman_problem(self):
        while True:
            self.__traveling_salesman_problem_text()
            res: TsmResultPython | None = None
            res_time: float = 0
            temp = input()
            match temp:
                case "1":
                    start_time = time.time()
                    res = self.__algo.solve_sp_brute_force(self.__graph)
                    end_time = time.time()
                    res_time = end_time - start_time
                case "2":
                    start_time = time.time()
                    res = self.__algo.solve_sp_held_karp(self.__graph)
                    end_time = time.time()
                    res_time = end_time - start_time
                case "3":
                    start_time = time.time()
                    res = self.__algo.solve_sp_nearest_neighbour(self.__graph)
                    end_time = time.time()
                    res_time = end_time - start_time
                case "4":
                    starts = self.__repeat_count()
                    if starts > 0:
                        start_time = time.time()
                        res = self.__algo.solve_sp_ant_colony(self.__graph, starts)
                        end_time = time.time()
                        res_time = end_time - start_time
                case "5":
                    starts = self.__repeat_count()
                    if starts > 0:
                        start_time = time.time()
                        res = self.__algo.solve_sp_annealing(self.__graph, starts)
                        end_time = time.time()
                        res_time = end_time - start_time
                case "6":
                    self.__compare_algos()
                    continue
                case "q":
                    return False
                case _:
                    print("Некорректный ввод.")
            if res is not None:
                self.__print_sp_result(res, res_time)
            else:
                print("Задача не может быть решена.")
                return False

    @staticmethod
    def __repeat_count() -> int:
        print("Укажите количество повторений алгоритма (от 1 до 100000)")
        starts = 1
        while True:
            try:
                starts = int(input())
            except:
                while True:
                    print("Некорректный ввод.")
                    print('\tНажмите "1" Для повторной попытки ввода.')
                    print('\tНажмите "q" Для выхода в меню выше.')
                    temp = input()
                    match temp:
                        case "1":
                            break
                        case "q":
                            return 0
                        case _:
                            print("Некорректный ввод.")
                continue
            break

        if starts < 1:
            starts = 1
        if starts > 100000:
            starts = 100000
        return starts

    def __compare_algos(self) -> bool:
        starts = self.__repeat_count()
        if starts > 0:

            start_time = time.time()
            for _ in range(starts):
                res_neighbour = self.__algo.solve_sp_nearest_neighbour(self.__graph)
            end_time = time.time()
            res_time_neighbour = end_time - start_time

            start_time = time.time()
            res_ant = self.__algo.solve_sp_ant_colony(self.__graph, starts)
            end_time = time.time()
            res_time_ant = end_time - start_time

            start_time = time.time()
            res_annealing = self.__algo.solve_sp_annealing(self.__graph, starts)
            end_time = time.time()
            res_time_annealing = end_time - start_time

            print("Результат муравьиного метода за " + str(starts) + " повторений:")
            self.__print_sp_result(res_ant, res_time_ant)
            print("")

            print(
                "Результат метода ближайшего соседа за " + str(starts) + " повторений:"
            )
            self.__print_sp_result(res_neighbour, res_time_neighbour)
            print("")

            print("Результат метода имитации отжига за " + str(starts) + " повторений:")
            self.__print_sp_result(res_annealing, res_time_annealing)

            return True
        else:
            return False
