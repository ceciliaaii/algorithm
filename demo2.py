import timeit  # 一个时间测试模块，用来计算一段代码执行num次的执行时间
import random

# 优化冒泡排序
def nom_sort(L):  # 标配版函数
    for i in range(len(L) - 1):
        for j in range(1, len(L) - i):
            if L[j - 1] > L[j]:
                L[j - 1], L[j] = L[j], L[j - 1]
    return L


def opt_sort(L):  # 优化版函数
    minindex = 0
    maxindex = len(L)
    for i in range(len(L) // 2):
        swap = False
        for j in range(minindex + 1, maxindex):
            if L[j - 1] > L[j]:
                L[j - 1], L[j] = L[j], L[j - 1]
                maxindex = j
        for k in range(maxindex - 1, minindex, -1):
            if L[k - 1] > L[k]:
                L[k - 1], L[k] = L[k], L[k - 1]
                minindex = k
                swap = True
        if not swap:
            break
    return L


res = []
number = 200  # 20, 200, 2000
M = list(range(0, number))
for i in range(1000):  # 循环次数 10000 1000 100
    random.shuffle(M)  # 随机打散
    N = M[:]
    res.append([timeit.timeit('nom_sort(M)', number=1, globals=globals()),
                timeit.timeit('opt_sort(N)', number=1, globals=globals())])
    # 分别执行两个函数，计算执行number次的总时间，为保证稳定性和公平性用for循环测试多次
print('%.8f %.8f' % tuple([sum([i[j] for i in res]) / len(res) for j in range(2)]))
# 计算两个函数的各自平均秒数
