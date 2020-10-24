def f():
    a = 0
    while True:
        yield a
        a += 1


a = f()

def n():
    return next(a)

