from multiprocessing import Manager, Value
class P:
    def __init__(self):
        self.a='a'
        self.b='a'
        self.c='a'
    def __str__(self) -> str:
        return f'a:{self.a}'

manager=Manager()
a=manager.dict({})
# a[1][1]=P()
a[1]=P()
# a[1][1]={'a':'1'}
print(a)
