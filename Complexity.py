import random
import time
import matplotlib.pyplot as plt
import numpy as np


def fuzzy_sort(A, leftmost, rightmost, comparisons=0):
    if leftmost < rightmost:
        a, b = find_intersection(A, leftmost, rightmost)
        t = partition_right(A, a, leftmost, rightmost)
        q = partition_left(A, b, leftmost, t)
        comparisons += rightmost - leftmost  # Adding the number of comparisons in the current call
        comparisons = fuzzy_sort(A, leftmost, q - 1, comparisons)
        comparisons = fuzzy_sort(A, t + 1, rightmost, comparisons)
    return comparisons


def find_intersection(A, leftmost, rightmost):
    rand = random.randint(leftmost, rightmost)
    A[rand], A[rightmost] = A[rightmost], A[rand]
    a, b = A[rightmost]
    for i in range(leftmost, rightmost):
        ai, bi = A[i]
        if ai <= b and bi >= a:
            a = max(a, ai)
            b = min(b, bi)
    return a, b

def partition_right(A, a, leftmost, rightmost):
    i = leftmost - 1
    for j in range(leftmost, rightmost):
        if A[j][0] <= a:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[rightmost] = A[rightmost], A[i + 1]
    return i + 1

def partition_left(A, b, leftmost, t):
    i = leftmost - 1
    for j in range(leftmost, t):
        if A[j][1] < b:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[t] = A[t], A[i + 1]
    return i + 1


def read_intervals_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        intervals = [tuple(map(float, line.strip().split())) for line in lines]
    return intervals

def time_analysis(filename, runs=10, n_values=range(10, 101, 10)):
    intervals = read_intervals_from_file(filename)
    execution_times = []
    complexities = []
    
    for n in n_values:
        A = intervals[:n]
        avg_time = 0
        avg_complexity = 0
        for _ in range(runs):
            start_time = time.time()
            comparisons = fuzzy_sort(A, 0, len(A) - 1)
            end_time = time.time()
            avg_time += end_time - start_time
            avg_complexity += comparisons
        execution_times.append(avg_time / runs)
        complexities.append(avg_complexity / runs)
    
    return execution_times, complexities




def plot_complexity_comparison(n_values=range(10, 101, 10)):
    x_np = np.array(n_values)

    plt.plot(n_values, x_np, label='Θ(n)', linestyle='--')
    plt.plot(n_values, x_np * np.log2(x_np), label='Θ(n*log(n))', linestyle='--')

    plt.xlabel('Number of Intervals (n)')
    plt.ylabel('Complexity')
    plt.legend()
    plt.title('Complexity Comparison: Θ(n) vs Θ(n*log(n))')

    plt.show()



overlap_filename = 'overlapping_intervals.txt'
non_overlap_filename = 'non_overlapping_intervals.txt'
plot_complexity_comparison()
