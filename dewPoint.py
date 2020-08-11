import sys
import math as np

# approximation valid for
# 0 degC < T < 60 degC
# 1% < RH < 100%
# 0 degC < Td < 50 degC

# constants
a = 17.271
b = 237.7 # degC

# sys.argv[0] is program name
#T=float(sys.argv[1])
#RH=float(sys.argv[2])


def get_dewpoint(T,RH):

    if RH != 0:
        Td = (b * gamma(T,RH)) / (a - gamma(T,RH))
    else:
        return 999

    return round(Td,1)


def gamma(T,RH):

    g = (a * T / (b + T)) + np.log(RH/100.0)

    return g
