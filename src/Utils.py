def fRange(start: float, stop: float, step: float):  # iterate over [start, stop]
    while start <= stop:
        yield start
        start += step
