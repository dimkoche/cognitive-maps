# coding: utf-8

from smatrix import mmul, mtranspose, mround, msum
import matplotlib
import matplotlib.pyplot as plt

# Количество шагов
steps = 6


def prepare_data(data, koef):
    koef_ = mtranspose(koef)
    # Следующий шаг изменений
    next_step = koef_
    # Сумма следующего шага изменений и всех предыдущих шагов
    sum_step = koef_
    # Изменения в % пошагово
    #step_vectors = []
    # Изменения в % нарастающим итогом
    sum_vectors = []

    for i in xrange(steps):
        next_step = mround(mmul(data, next_step), 1)
        #step_vector.append(mtranspose(next_step)[0])
        sum_step = msum(sum_step, next_step)
        sum_vectors.append(mtranspose(sum_step)[0])
    sum_vectors.insert(0, koef[0])
    return sum_vectors


def draw(data, keys, koef, img_name="figure.png"):
    sum_vectors = prepare_data(data, koef)

    max_v = 0
    min_v = 0
    for r in sum_vectors:
        for v in r:
            if v > max_v:
                max_v = v
            if v < min_v:
                min_v = v

    matplotlib.rc('font', **{'sans-serif': 'Arial', 'family': 'sans-serif'})
    plt.clf()
    plt.plot(sum_vectors)

    plt.ylabel('Procents')
    plt.legend(keys, loc="lower right")
    plt.axis([0, steps, min_v - 5, max_v + 5])

    plt.savefig(img_name)
