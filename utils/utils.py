import os
import pickle

def middle(file):
    def wrapper(func):
        def _wrapper(*args, **kargs):
            if os.path.exists(file):
                return pickle.load(open(file, 'rb'))
            else:
                rs = func(*args, **kargs)
                pickle.dump(rs, open(file, 'wb'))
                return rs

        return _wrapper

    return wrapper