def fRange(start: float, stop: float, step: float = 1.0):  # iterate over [start, stop]
    while start <= stop:
        yield start
        start += step
