#!/usr/bin/python


class A:
  # class variable
  my_list = []

  @classmethod
  def my_method(cls, item):
    cls.my_list.append(item)
    print cls.my_list
    print A.my_list


