import time

def timestamp(mili=False, str_type = True):
    """ return timestamp """
    _time = time.time()
    if str_type:
        if mili:
            return str(_time)
        else:
            return str(int(_time))
    else:
        if mili:
            return _time
        else:
            return int(_time)
