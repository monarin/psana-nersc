class Base(object):
    def say(self):
        print('base')
    def __del__(self):
        print('base exit')

class Derived(Base):
    def say(self):
        print('derived')
        super().say()

b = Base()
b.say()

d = Derived()
d.say()
