# coding: utf-8


def msize(mtx):
    """
    Определение размера матрицы mtx.
    """

    rows = len(mtx)
    cols = len(mtx[0])

    for row in mtx:
        if len(row) != cols:
            raise ValueError(u'Wrong mtx size')
    return rows, cols


def mtranspose(m):
    """
    Транспонирование матрицы
    """
    mt = []

    cols = len(m[0])
    rows = len(m)

    for i in xrange(cols):
        mt.append([m[j][i] for j in xrange(rows)])
    return mt


def mgen(n):
    """
    Генерация квадратной матрицы n*n.
    """

    import random

    def vgen(n):
        return [random.randint(0, 100) for i in xrange(n)]

    return [vgen(n) for i in xrange(n)]


def mround(mtx, n=2):
    """
    Округление каждого элемента матрицы mtx до n знаков после запятой.
    """

    def vround(v, n):
        """
        Округление вектора v до n знаков после запятой.
        """

        return [round(x, n) for x in v]

    return [vround(v, n) for v in mtx]


def msum(mtx1, mtx2):
    """
    Сложение матриц mtx1 и mtx2.
    """

    def vsum(v1, v2):
        """
        Сложение векторов v1 и v2
        """
        return [sum(x) for x in zip(v1, v2)]

    if msize(mtx1) != msize(mtx2):
        raise ValueError(u'Objects are not aligned')

    return map(vsum, mtx1, mtx2)


def mmul(a, b):
    """
    Умножение матриц
    """

    def vmul(v1, v2):
        """
        Умножение векторов v1 и v2
        """

        return sum([v1[i] * v2[i] for i in xrange(len(v1))])

    if msize(a)[1] != msize(b)[0]:
        raise ValueError(u'Objects are not aligned')
    bt = mtranspose(b)
    result = []

    for i in xrange(len(a)):
        v = [vmul(a[i], bt[j]) for j in xrange(len(bt))]
        result.append(v)
    return result
