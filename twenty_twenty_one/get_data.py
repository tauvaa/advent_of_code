import os
def get_data(filename):
    with open(filename) as f:
        data = f.read()
        return data
