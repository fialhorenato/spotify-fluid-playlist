def partition(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i: i + size]