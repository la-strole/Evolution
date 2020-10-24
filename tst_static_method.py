class fist:
    @staticmethod
    def fun1():
        return 'class first fun1'

    @staticmethod
    def fun2():
        return fist.fun1() + 'class first fun2'


class second(fist):
    @staticmethod
    def fun2():
        return 'class second fun2'

#instnnce of class second
print(second.fun2())
print(second.fun1())