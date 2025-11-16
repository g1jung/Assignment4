"""
quicksort.py

Deterministic and randomized implementations of Quicksort in Python,
plus a simple benchmarking harness.
"""

import random
import time
from typing import List, Callable, Tuple


# ------------------------------
# Deterministic Quicksort
# ------------------------------

def partition_deterministic(arr: List[int], low: int, high: int) -> int:
    """
    Partition using the last element as pivot (deterministic choice).
    Returns final index of the pivot.
    """
    pivot = arr[high]
    i = low - 1  # index of smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Place pivot in the correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_deterministic(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    In-place deterministic Quicksort using last-element pivot.
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        p = partition_deterministic(arr, low, high)
        quicksort_deterministic(arr, low, p - 1)
        quicksort_deterministic(arr, p + 1, high)


# ------------------------------
# Randomized Quicksort
# ------------------------------

def partition_randomized(arr: List[int], low: int, high: int) -> int:
    """
    Partition where the pivot is chosen randomly from [low, high].
    The chosen element is swapped to the end and then standard partition is used.
    """
    pivot_index = random.randint(low, high)
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    # Reuse deterministic partition after moving random pivot to the end
    return partition_deterministic(arr, low, high)


def quicksort_randomized(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    In-place randomized Quicksort.
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        p = partition_randomized(arr, low, high)
        quicksort_randomized(arr, low, p - 1)
        quicksort_randomized(arr, p + 1, high)


# ------------------------------
# Benchmarking Helpers
# ------------------------------

def is_sorted(arr: List[int]) -> bool:
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def benchmark_sort(
    sort_fn: Callable[[List[int]], None],
    arr: List[int]
) -> Tuple[float, bool]:
    """
    Benchmarks a sorting function on a copy of the given array.

    Returns:
        (elapsed_time_in_seconds, is_correctly_sorted)
    """
    data = arr.copy()
    start = time.perf_counter()
    sort_fn(data)
    end = time.perf_counter()
    return end - start, is_sorted(data)


def generate_test_arrays(n: int) -> dict:
    """
    Generate different types of test arrays of size n.
    """
    random_arr = [random.randint(0, 10_000) for _ in range(n)]
    sorted_arr = sorted(random_arr)
    reverse_sorted_arr = list(reversed(sorted_arr))
    return {
        "random": random_arr,
        "sorted": sorted_arr,
        "reverse_sorted": reverse_sorted_arr,
    }


def main():
    """
    Simple CLI benchmark:
    - Generates arrays of a given size
    - Runs deterministic vs randomized quicksort
    - Prints timing and correctness for each input type
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Deterministic vs Randomized Quicksort Benchmark"
    )
    parser.add_argument(
        "-n",
        "--size",
        type=int,
        default=10000,
        help="Size of the input array (default: 10000)",
    )
    args = parser.parse_args()

    arrays = generate_test_arrays(args.size)

    print(f"Array size: {args.size}")
    print("-" * 50)

    for label, arr in arrays.items():
        print(f"Input type: {label}")

        # Deterministic
        det_time, det_ok = benchmark_sort(
            lambda a: quicksort_deterministic(a, 0, len(a) - 1), arr
        )
        print(f"  Deterministic quicksort: {det_time:.6f}s, sorted={det_ok}")

        # Randomized
        rand_time, rand_ok = benchmark_sort(
            lambda a: quicksort_randomized(a, 0, len(a) - 1), arr
        )
        print(f"  Randomized quicksort:   {rand_time:.6f}s, sorted={rand_ok}")

        print()

    print("Note: Absolute times depend on hardware and Python overhead.")


if __name__ == "__main__":
    main()
