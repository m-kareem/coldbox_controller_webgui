# -- approximate dewPoint calculator

import sys
import math as np
#from meteocalc import Temp, dew_point

import modules.GUIlogger as GUIlogger
logger = GUIlogger.init_logger(__name__)

# sys.argv[0] is program name
#T=float(sys.argv[1])
#RH=float(sys.argv[2])


def get_dewpoint(T,RH):
    # approximation valid for
    # 0 degC < T < 60 degC
    # 1% < RH < 100%
    # 0 degC < Td < 50 degC

    # constants
    a = 17.271
    b = 237.7 # degC
    if (T is not None) and (RH is not None) and (RH != 0):
        gamma = (a * T / (b + T)) + np.log(RH/100.0)
        dp_aprox = (b * gamma) / (a - gamma)
    else:
        return -999

    return round(dp_aprox,1)



#---------------------------------
'''
def get_dewpoint2(T,RH):
    #-- Formula: 243.04*(ln(RH/100)+((17.625*T)/(243.04+T)))/(17.625-ln(RH/100)-((17.625*T)/(243.04+T)))
    dp = dew_point(temperature=T, humidity=RH)
    return round(dp.c,1)
'''

if __name__ == '__main__':
    print('--- dewpoint calculator ---')

    print(get_dewpoint(23,50))
    #print(get_dewpoint2(23,40))
