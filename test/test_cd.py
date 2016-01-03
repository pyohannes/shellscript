import os


def valid_input():
    yield dict(path=os.getcwd()), []


def invalid_input():
    p = os.getcwd()
    while os.path.exists(p):
        p += 'x'
    yield dict(path=p), [] 
