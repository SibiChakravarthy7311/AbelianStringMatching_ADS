import pickle
from collections import defaultdict
from matplotlib import pyplot
import numpy as np
import timeit
from functools import partial
from time import time
from DataGenerator import generateData


# graph plotting helper function
def plot_time(func, inputs, repeats, n_tests):
    x, y, y_err = [], [], []
    cnt = 1
    for i in inputs:
        print(cnt)
        cnt += 1
        y_string = i[0]
        x_string = i[1]
        m = len(y_string)
        n = len(x_string)
        timer = timeit.Timer(partial(func, y_string, x_string, m, n))
        t = timer.repeat(repeat=repeats, number=n_tests)
        x.append(len(i[1]))
        y.append(np.mean(t))
        y_err.append(np.std(t) / np.sqrt(len(t)))
    pyplot.errorbar(x, y, yerr=y_err, fmt='-o', label=func.__name__)


# to run functions and plot graph
def plot_times(functions, inputs, repeats=3, n_tests=1, file_name_prefix=""):
    for func in functions:
        plot_time(func, inputs, repeats, n_tests)
    pyplot.legend()
    pyplot.xlabel("Input")
    pyplot.ylabel("Time [s]")
    # pyplot.show()
    if not file_name_prefix:
        pyplot.show()
    else:
        pyplot.savefig(file_name_prefix + str(round(time() * 1000)))


# O(m + sigma), where sigma = the character size in the whole set
def computeParikhVector(s):
    parikhVector = defaultdict(int)
    for i in s:
        parikhVector[i] += 1
    return parikhVector


# to compare the equality of 2 parikh vectors
def checkParikhVector(vector1, vector2):
    if len(vector1) != len(vector2):
        return False
    for key in vector1:
        if vector2[key] != vector1[key]:
            return False
    return True


# Brute force approach to find the abelian matches
def bruteForceApproach(y, x, m, n):
    parikhVector = computeParikhVector(y)
    indices = []
    for i in range(n - m):
        parikhVectorX = defaultdict(int)
        ind = i
        for j in range(m):
            parikhVectorX[x[ind]] += 1
            ind += 1
        if checkParikhVector(parikhVector, parikhVectorX):
            indices.append(i)
    return indices


# Sliding window approach
def slidingWindowApproach(y, x, m, n):
    left = 0
    right = 0
    parikhWindow = computeParikhVector(y)
    indices = []
    while right < m:
        parikhWindow[x[right]] -= 1
        right += 1
    difference = sum(abs(value) for value in parikhWindow.values())
    if difference == 0:
        indices.append(0)
    while right < n:
        remove = x[left]
        add = x[right]
        if parikhWindow[remove] < 0:
            difference -= 1
        else:
            difference += 1
        parikhWindow[remove] += 1
        if parikhWindow[add] > 0:
            difference -= 1
        else:
            difference += 1
        parikhWindow[add] -= 1
        left += 1
        if difference == 0:
            indices.append(left)
        right += 1
    return indices


# to compute the heap mapping for each value in the alphabet size m, 26 in our case
def computeHeapMapping():
    x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    h = dict()
    value = 1
    for i in x:
        h[i] = value
        value <<= 1
    return h


# Heap counting abelian matching method
def heapCountingAbelianMatching(y, x, m, n):
    h = computeHeapMapping()
    a = b = 0
    indices = []
    for i in range(m):
        a = a + h[x[i]]
        b = b + h[y[i]]
    if a == b:
        indices.append(0)
    right = m
    left = 0
    while right < n:
        a += h[x[right]] - h[x[left]]
        left += 1
        if a == b:
            indices.append(left)
        right += 1
    return indices


# to compute heap mapping within a fixed size alphabet
def computeFixedHeapMapping(alphabets):
    h = dict()
    value = 1
    for alphabet in alphabets:
        h[alphabet] = value
        value <<= 1
    return h


# Heap counting abelian matching method with reduced alphabet size
def heapCountingAbelianMatchingAlphabetReduced(y, x, m, n):
    alphabets = list(set(x))
    alphabets.sort()
    h = computeFixedHeapMapping(alphabets)
    a = b = 0
    indices = []
    for i in range(m):
        a = a + h[x[i]]
        b = b + h[y[i]]
    if a == b:
        indices.append(0)
    right = m
    left = 0
    while right < n:
        a += h[x[right]] - h[x[left]]
        left += 1
        if a == b:
            indices.append(left)
        right += 1
    return indices


# computing a parikh table instead of a parikh vector
def computeTableMapping(alphabets):
    table = [-1] * 123
    value = 1
    for alphabet in alphabets:
        table[ord(alphabet)] = value
        value <<= 1
    return table


# Heap counting abelian matching method with reduced alphabet size
def tableCountingAbelianMatchingAlphabetReduced(y, x, m, n):
    alphabets = list(set(x))
    alphabets.sort()
    table = computeTableMapping(alphabets)
    a = b = 0
    indices = []
    for i in range(m):
        a = a + table[ord(x[i])]
        b = b + table[ord(y[i])]
    if a == b:
        indices.append(0)
    right = m
    left = 0
    while right < n:
        a += table[ord(x[right])] - table[ord(x[left])]
        left += 1
        if a == b:
            indices.append(left)
        right += 1
    return indices


# Heap counting abelian matching method with reduced alphabet size
def tableCountingAbelianMatchingAlphabetReducedRedux(y, x, m, n):
    alphabets = list(set(x))
    alphabets.sort()
    table = computeTableMapping(alphabets)
    a = b = 0
    indices = []
    for i in range(m):
        a = a + table[ord(x[i])]
        b = b + table[ord(y[i])]
    difference = a - b
    if not difference:
        indices.append(0)
    right = m
    left = 0
    while right < n:
        difference += table[ord(x[right])] - table[ord(x[left])]
        left += 1
        if not difference:
            indices.append(left)
        right += 1
    return indices


generateData()
with open('data.pickle', 'rb') as f:
    loaded_data = pickle.load(f)
# plot_times([bruteForceApproach, slidingWindowApproach, heapCountingAbelianMatching,
#                 heapCountingAbelianMatchingAlphabetReduced, tableCountingAbelianMatchingAlphabetReduced,
#                 tableCountingAbelianMatchingAlphabetReducedRedux],
#                loaded_data, repeats=3, n_tests=1, file_name_prefix="plot-")
plot_times([slidingWindowApproach, heapCountingAbelianMatching,
                heapCountingAbelianMatchingAlphabetReduced, tableCountingAbelianMatchingAlphabetReduced,
                tableCountingAbelianMatchingAlphabetReducedRedux],
               loaded_data, repeats=1, n_tests=1, file_name_prefix="plot-")


