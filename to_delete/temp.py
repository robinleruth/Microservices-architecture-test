class A:
    def print_class(self):
        print(self.__class__.__name__)


class B(A):
    pass


if __name__ == '__main__':
    b = B()
    b.print_class()