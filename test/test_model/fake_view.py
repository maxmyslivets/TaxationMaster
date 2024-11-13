class FakeView:

    def __init__(self):
        pass

    @staticmethod
    def log(s: str):

        PRINT_LOG = True

        if PRINT_LOG:
            print("\n\033[33m" + s + "\033[0m")
        else:
            pass
