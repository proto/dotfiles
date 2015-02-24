#!/usr/local/bin/python

# -*- coding: utf-8 -*-
__author__ = 'proto'
__project__ = 'MacHealthCheck'
__date__ = '13/12/14'
__version__ = '0.0.1'

import sys
from subprocess import check_output
#from emoji import emojize
import re
#from clint.textui import colored


BATTERY = ["/usr/bin/pmset", "-g", "batt"]
AC = "AC"
BT = "Battery"
STAR = ":star:"
BATT = ":battery:"
PLUG = ":electric_plug:"
BS = unichr(9733).encode('utf8')
WS = unichr(9734).encode('utf8')
PWR = unichr(9863).encode('utf8')
BTR = unichr(9851).encode('utf8')

bl = {(0, 20): 'grey', (21, 40): 'red', (41, 60): 'orange', (61, 80): 'yellow', (81, 100): 'green'}

st = {'grey': (1, 4), 'red': (2, 3), 'orange': (3, 2), 'yellow': (4, 1), 'green': (5, 0)}


def main():
    """"
        battery life check
        :return:
    """
    battery_status = get_status()
    print(battery_status)

    return 0


def get_status():
    """
        get battery status
        :return:
    """
    out = check_output(BATTERY).split("\n")
    power_from = out[0].lstrip('Now drawing from').strip('\'').strip(' Power')
    power = out[1]

    bat_pwr = re.search(r'(?P<battery>(\w+%))', power)
    # todo: sistemare
    # bat_rmg = re.search(r'(?P<remaining>(\w+:\w+))', power)
    bat_sts = re.search(r'(?P<status>(\s\w+;))', power)

    p = int(bat_pwr.group('battery').strip('%'))
    # r = bat_rmg.group('remaining')
    s = bat_sts.group('status').strip(';').strip(' ')

    # print str(p), '|',  r, '|', s

    lst = [p]

    def power_status():
        result = []
        for l in lst:
            #print type(l), type(lst), l, lst
            for m in bl:
                if m[0] <= l <= m[1]:
                    result.append(bl[m])
        return result

    ichk = str(power_status()).strip("['").strip("']")
    #print ichk, type(ichk)

    chk = st[str(power_status()).strip("['").strip("']")]
    rchk = ((BS) + ' ') * chk[0]+(WS + ' ') * chk[1]

    if power_from == AC:
        #return emojize(PLUG) + ' ' + rchk
        return PWR + ' ' + rchk
    elif power_from == BT:
        #return emojize(BATT) + ' ' + rchk
        return BTR + ' ' + rchk

#print colored.red(BS + ' ') * 4


if __name__ == "__main__":
    sys.exit(main())
