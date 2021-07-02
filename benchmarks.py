import numpy
import math

# define the function blocks


def F1(x):
    s = numpy.sum(x**2)
    return s


def getFunctionDetails(a):

    param = {	0: ["F1", -100, 100, 30, 1.0e-5, 0],
              }
    return param.get(a, "nothing")
