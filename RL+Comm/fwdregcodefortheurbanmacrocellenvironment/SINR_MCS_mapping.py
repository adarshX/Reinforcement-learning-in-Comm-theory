# According to as defined in the paper Planning for small cells - WCNC 2014

def SINR_MCS_mapping(sinrdB):

    ii = 0
    CQI = []
    eff = []
    for item in sinrdB:

        if (item < -6.5):
            C = 0
            e = 0

        if (item >= -6.5 and item < -4):
            C = 1
            e = 0.15

        if (item >= -4 and item < -2.6):
            C = 2
            e = 0.23

        if (item >= -2.6 and item < -1):
            C = 3
            e = 0.38

        if (item >= -1 and  item < 1):
            C = 4
            e = 0.6

        if (item >= 1 and item < 3):
            C = 5
            e = 0.88

        if (item >= 3 and  item < 6.6):
            C = 6
            e = 1.18

        if (item >= 6.6 and item < 10):
            C = 7
            e = 1.48

        if (item >= 10 and item < 11.4):
            C = 8
            e = 1.91

        if (item >= 11.4 and item < 11.8):
            C = 9
            e = 2.41

        if (item >= 11.8 and item < 13):
            C = 10
            e = 2.73

        if (item >= 13 and item < 13.8):
            C = 11
            e = 3.32

        if (item >= 13.8 and item < 15.6):
            C = 12
            e = 3.9

        if (item >= 15.6 and item < 16.8):
            C = 13
            e = 4.52

        if (item >= 16.8 and item < 17.6):
            C = 14
            e = 5.12

        if (item >= 17.6):
            C = 15
            e = 5.55

        CQI.append(C)
        eff.append(e) 

    return CQI, eff
