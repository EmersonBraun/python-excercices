#!/usr/bin/python3
def sequence():
    num = 0
    while True:
        num += 1
        yield num


if __name__ == '__main__':
    seq = sequence()
    for i in range(10):
        print(next(seq))
