from copy import deepcopy
from copy import copy

class testClass(object):
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c



def main():
    test_1 = testClass(0,1,2)
    print(test_1.a,test_1.b,test_1.c)

    test_2 = copy(test_1)

    test_2.a = 1232

    # print(test_1.a,test_1.b,test_1.c)

    # print(test_2.a,test_2.b,test_2.c)


if __name__ == "__main__":
    main()
