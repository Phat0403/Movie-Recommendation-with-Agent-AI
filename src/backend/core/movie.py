import time

def get_current_year():
    """
    Get the current year.
    """
    return int(time.strftime("%Y", time.localtime()))

if __name__ == "__main__":
    print(get_current_year())