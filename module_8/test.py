#!/usr/bin/python


class Add:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def add_number(self):
        return self.a + self.b


def add(a, b):
    
    result = Add(a, b)
    
    print result.add_number()





