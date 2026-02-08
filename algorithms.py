"""
Sorting algorithms as generators for visualization.
Each yield: (array_snapshot, compare_indices, sorted_indices, comparisons, accesses).
"""

from typing import Generator

# Yield type: (snapshot, compare_inds, sorted_inds, comparisons, accesses)
SortStep = tuple[list[int], list[int], list[int], int, int]


def quicksort(arr: list[int]) -> Generator[SortStep, None, None]:
    """
    In-place QuickSort. Yields on each comparison and swap.
    Red = indices being compared; Green = pivot in final position.
    """
    comparisons = 0
    accesses = 0

    def partition(
        a: list[int], low: int, high: int, sorted_so_far: list[int]
    ) -> Generator[SortStep, None, int]:
        nonlocal comparisons, accesses
        pivot = a[high]
        accesses += 1
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            accesses += 2  # read a[j], read pivot (a[high])
            yield (a[:], [j, high], sorted_so_far[:], comparisons, accesses)
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    accesses += 4  # 2 reads + 2 writes
                    yield (a[:], [i, j], sorted_so_far[:], comparisons, accesses)
        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            accesses += 4
            yield (a[:], [i + 1, high], sorted_so_far[:], comparisons, accesses)
        pivot_idx = i + 1
        sorted_so_far.append(pivot_idx)
        yield (a[:], [], sorted_so_far[:], comparisons, accesses)
        return pivot_idx

    def _quicksort(
        a: list[int], low: int, high: int, sorted_so_far: list[int]
    ) -> Generator[SortStep, None, None]:
        if low < high:
            part_gen = partition(a, low, high, sorted_so_far)
            try:
                while True:
                    step = next(part_gen)
                    yield step
            except StopIteration as e:
                pivot_idx = e.value
            for step in _quicksort(a, low, pivot_idx - 1, sorted_so_far):
                yield step
            for step in _quicksort(a, pivot_idx + 1, high, sorted_so_far):
                yield step

    if len(arr) <= 1:
        yield (arr[:], [], list(range(len(arr))) if arr else [], 0, 0)
        return
    sorted_so_far: list[int] = []
    yield from _quicksort(arr, 0, len(arr) - 1, sorted_so_far)


def mergesort(arr: list[int]) -> Generator[SortStep, None, None]:
    """
    MergeSort. Yields on each comparison and merge write.
    Green = indices that are in their final sorted position (after merge).
    """
    comparisons = 0
    accesses = 0

    def merge(
        a: list[int],
        left: int,
        mid: int,
        right: int,
        sorted_so_far: list[int],
    ) -> Generator[SortStep, None, None]:
        nonlocal comparisons, accesses
        left_half = a[left : mid + 1]
        right_half = a[mid + 1 : right + 1]
        accesses += (mid - left + 1) + (right - mid)
        i = j = 0
        k = left
        while i < len(left_half) and j < len(right_half):
            comparisons += 1
            accesses += 2
            yield (
                a[:],
                [k],
                sorted_so_far[:],
                comparisons,
                accesses,
            )
            if left_half[i] <= right_half[j]:
                a[k] = left_half[i]
                accesses += 1
                i += 1
            else:
                a[k] = right_half[j]
                accesses += 1
                j += 1
            yield (a[:], [k], sorted_so_far[:], comparisons, accesses)
            k += 1
        while i < len(left_half):
            a[k] = left_half[i]
            accesses += 1
            yield (a[:], [k], sorted_so_far[:], comparisons, accesses)
            i += 1
            k += 1
        while j < len(right_half):
            a[k] = right_half[j]
            accesses += 1
            yield (a[:], [k], sorted_so_far[:], comparisons, accesses)
            j += 1
            k += 1
        sorted_so_far.extend(range(left, right + 1))

    def _mergesort(
        a: list[int], left: int, right: int, sorted_so_far: list[int]
    ) -> Generator[SortStep, None, None]:
        if left >= right:
            return
        mid = (left + right) // 2
        yield from _mergesort(a, left, mid, sorted_so_far)
        yield from _mergesort(a, mid + 1, right, sorted_so_far)
        yield from merge(a, left, mid, right, sorted_so_far)

    if len(arr) <= 1:
        yield (
            arr[:],
            [],
            list(range(len(arr))) if arr else [],
            0,
            0,
        )
        return
    sorted_so_far: list[int] = []
    yield from _mergesort(arr, 0, len(arr) - 1, sorted_so_far)


def heapsort(arr: list[int]) -> Generator[SortStep, None, None]:
    """
    In-place HeapSort (max-heap). Yields on each comparison and swap.
    Green = indices that are in their final sorted position (after extract-max).
    """
    n = len(arr)
    comparisons = 0
    accesses = 0
    sorted_so_far: list[int] = []

    def heapify(a: list[int], size: int, root: int) -> Generator[SortStep, None, None]:
        nonlocal comparisons, accesses
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        if left < size:
            comparisons += 1
            accesses += 2
            yield (a[:], [root, left], sorted_so_far[:], comparisons, accesses)
            if a[left] > a[largest]:
                largest = left
        if right < size:
            comparisons += 1
            accesses += 2
            yield (a[:], [root, right], sorted_so_far[:], comparisons, accesses)
            if a[right] > a[largest]:
                largest = right
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            accesses += 4
            yield (a[:], [root, largest], sorted_so_far[:], comparisons, accesses)
            yield from heapify(a, size, largest)

    if n <= 1:
        yield (arr[:], [], list(range(len(arr))) if arr else [], 0, 0)
        return

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        for step in heapify(arr, n, i):
            yield step

    # Extract elements one by one
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        accesses += 4
        yield (arr[:], [0, end], sorted_so_far[:], comparisons, accesses)
        sorted_so_far.append(end)
        for step in heapify(arr, end, 0):
            yield step
    sorted_so_far.append(0)
    yield (arr[:], [], sorted_so_far[:], comparisons, accesses)
