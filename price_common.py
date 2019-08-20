# -*- coding: utf-8 -*-

# from my_logger import logger


def convertnum2(num):
    if (num == 'numberzero'):
        return '0'
    elif (num == 'numberone'):
        return '1'
    elif (num == 'numbertwo'):
        return '2'
    elif (num == 'numberthree'):
        return '3'
    elif (num == 'numberfour'):
        return '4'
    elif (num == 'numberfive'):
        return '5'
    elif (num == 'numbersix'):
        return '6'
    elif (num == 'numberseven'):
        return '7'
    elif (num == 'numbereight'):
        return '8'
    elif (num == 'numbernine'):
        return '9'
    elif (num == 'numberdor'):
        return '.'
    else:
        num


def parenum(tdsib):
    sign_num = ''
    spanstr = tdsib.span
    a = convertnum2(spanstr.attrs["class"][0])
    sign_num = sign_num + a
    # print(sign_num)
    for numstr in spanstr.next_siblings:
        # print(type(numstr))
        if (numstr == u'㎡' or numstr == '%' or
                unicode(numstr).strip() == u'元/㎡' or numstr == u'元'):
            sign_num = sign_num + unicode(numstr).strip()
            break

        a = convertnum2(numstr["class"][0])
        sign_num = sign_num + a
        # print(sign_num)

    return sign_num


def checkandparsenum(tdsib):
    record_price = ''
    if (tdsib.a.div.span is None):
        record_price = tdsib.a.div.text.strip()
    else:
        record_price = parenum(tdsib)
    return record_price


def takeSecond(rd):
    a = rd.room.split(u"室")[0]
    return int(a)


def getRoomNum(rm):
    a = rm.split(u"室")[0]
    return a


def getBuilding(building):
    unit = "0"
    bs = building.split(u"幢")
    if bs[1] is not None:
        unit = bs[1]
    bd = bs[0] + u"幢"
    return bd, unit


def bd_sort_key(item):
    bd = item[0]
    numdb = getBuilding(bd)
    return numdb


def ut_sort_key(item):
    ut = item[0]
    numut = ut.split(u"幢")
    return numut
