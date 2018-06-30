#!/usr/bin/python


class Test:
    def testmethod(self):
        print "hello world we are in test method"
    
    class Testy:
        def testmethod(self):
            print "hello world we are in testy method"
    
    
    
#    a = 1

#    @classmethod
#    def test(cls):
#        print cls.a
#        print "hello world"
#
#    test(Test)

Test().testmethod()

Test().Testy().testmethod()
