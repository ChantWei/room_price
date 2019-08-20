# -*- coding: utf-8 -*-

from my_logger import logger

g_cur_point = ""
g_file_name = "./price_check_point"


class PreSellInfo:
    name = ''
    short_url = ''

    def __init__(self, name, short_url):
        self.name = name
        self.short_url = short_url


def LoadCheckPoint():
    global g_file_name
    global g_cur_point
    fd = open(g_file_name, "a+")
    fd.seek(0, 0)
    ct = fd.readline()
    if ct != "":
        g_cur_point = ct.split(',')[1].strip("\n")
    logger.info("get record check point from " + g_file_name + ", url: " + ct)
    fd.close()
    return


def IsNewsBuilding(short_url):
    global g_cur_point
    if short_url == g_cur_point:
        return False
    else:
        return True


def UpdateCheckPoint(update_info):
    global g_cur_point
    new_point = update_info.name + "," + update_info.short_url
    if g_cur_point == update_info.short_url:
        logger.info("old record url, no need update: " + new_point)
        return
    logger.info("record check point is : " + g_cur_point +
                " , will update to : " + new_point)

    global g_file_name
    fd = open(g_file_name, "w")
    fd.seek(0, 0)
    point = new_point + "\n"
    fd.write(point)

    g_cur_point = update_info.short_url
    logger.info(g_file_name + "record check point has update to: " +
                g_cur_point + " for " + update_info.name)
    return


if __name__ == "__main__":
    update_info = PreSellInfo("府", "price.htm")
    LoadCheckPoint()
    UpdateCheckPoint(update_info)

    al = []
    al.append("aaaa")
    al.append("bbb")
    logger.info(al)
