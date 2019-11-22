import random
import sys
from datetime import datetime
from math import sqrt
from time import sleep
from typing import List
import matplotlib.pyplot as plt
import threading as th


def get_time():
    return datetime.today().replace(microsecond=0).isoformat(sep=' ')


def generator(sleep_time: float, q_id: int, out: List[str]):
    out.append(f'{get_time()}-INFO-QUERY FOR ID={q_id}\n')
    sleep(sleep_time)
    out.append(f'{get_time()}-INFO-RESULT QUERY FOR ID={q_id}\n')


def create_log_file(id_count: int = None, output_file_name: str = None, MX: float = None, DX: float = None,
                    show_plot: bool = None, dir_path: str = None):
    """
        id_count - количество id
        output_file_name - путь выходного файла
        MX - мат ожидание нормального (гаусовского) распределения
        DX - DX дисперсия
        show_plot - флаг за отображение и сохранения графика времени "запроса"

        Время работы примерно O(id_count) секунд
    """
    path = sys.argv[0]
    if id_count is None:
        id_count = 100
    if output_file_name is None:
        output_file_name = path[:path.rindex('/') + 1] + 'log.txt'
    if MX is None:
        MX = 5
    if DX is None:
        DX = 1
    if show_plot is None:
        show_plot = True

    out = []
    threads = []

    id_count = 1000

    for i in range(1, id_count + 1):
        time = random.gauss(MX, sqrt(DX)) + (10 if random.random() < 0.01 else 0)
        if show_plot:
            plt.scatter(i, time)
        threads.append(th.Thread(target=generator, args=(time, i, out)))
        sleep(abs(random.gauss(0, 1)))
        threads[-1].start()

    for thread in threads:
        thread.join()

    with open(output_file_name, 'w') as file:
        file.writelines(out)

    if show_plot:
        plt.savefig(path[:path.rindex('/') + 1] + 'log.png')
        plt.show()


if __name__ == '__main__':
    create_log_file()
