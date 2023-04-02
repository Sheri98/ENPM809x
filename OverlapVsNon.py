import random
import time
import matplotlib.pyplot as plt

def fuzzy_sort(A, leftmost, rightmost):
    if leftmost < rightmost:
        a, b = find_intersection(A, leftmost, rightmost)
        t = partition_right(A, a, leftmost, rightmost)
        q = partition_left(A, b, leftmost, t)
        fuzzy_sort(A, leftmost, q - 1)
        fuzzy_sort(A, t + 1, rightmost)

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

def time_analysis(filename, runs=10):
    intervals = read_intervals_from_file(filename)
    execution_times = []
    
    for n in range(10, len(intervals), 10):
        A = intervals[:n]
        avg_time = 0
        for _ in range(runs):
            start_time = time.time()
            fuzzy_sort(A, 0, len(A) - 1)
            end_time = time.time()
            avg_time += end_time - start_time
        execution_times.append(avg_time / runs)
    
    return execution_times

def compare_and_plot(overlap_filename, non_overlap_filename, runs=10):
    overlap_times = time_analysis(overlap_filename, runs)
    non_overlap_times = time_analysis(non_overlap_filename, runs)

    x_values = range(10, 10 * len(overlap_times) + 1, 10)

    plt.plot(x_values, overlap_times, label='Overlapping Intervals')
    plt.plot(x_values, non_overlap_times, label='Non-overlapping Intervals')
    
    plt.xlabel('Number of Intervals (n)')
    plt.ylabel('Average Execution Time (s)')
    plt.legend()
    plt.title('Fuzzy Sort: Overlapping vs Non-overlapping Intervals')
    plt.show()

overlap_filename = 'overlapping_intervals.txt'
non_overlap_filename = 'non_overlapping_intervals.txt'

compare_and_plot(overlap_filename, non_overlap_filename)
