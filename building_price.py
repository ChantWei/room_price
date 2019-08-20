# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import room_info
import price_common
import request_common
import format_out
from my_logger import logger


def AddRecord(buildings, building, rd):
    # buildnum = int(building.split(u"幢")[0])
    buildnum = building
    if buildnum not in buildings:
        item_list = []
        item_list.append(rd)
        buildings[buildnum] = item_list
        # print("new building ", buildnum)
        # print(buildings)
    else:
        item_list = buildings[buildnum]
        item_list.append(rd)
        # print("add new building ", buildnum)


def ParseItem(buildings, tr):
    tdsib = tr.td
    building = tdsib.a.text

    i = 0
    for tdsib in tr.td.next_siblings:
        if (type(tr) == type(tdsib)):
            i = i + 1
            if (i == 1):
                room = tdsib.a.div.text
            elif (i == 2):
                area = price_common.parenum(tdsib)
            elif (i == 3):
                room_rate = price_common.parenum(tdsib)
            elif (i == 4):
                real_area = price_common.parenum(tdsib)
            elif (i == 5):
                record_price = price_common.checkandparsenum(tdsib)
                if (record_price == '-'):
                    return
            elif (i == 6):
                decorate_price = price_common.checkandparsenum(tdsib)
            elif (i == 7):
                total_price = price_common.checkandparsenum(tdsib)
            elif (i == 8):
                stat = ""
                if (tdsib.div.font is None):
                    stat = tdsib.div.a.text.strip()
                else:
                    stat = tdsib.div.font.text.strip()

    rd = room_info.RoomDetail(building, room, area, room_rate, real_area,
                              record_price, decorate_price, total_price, stat)
    rd.Print()
    AddRecord(buildings, building, rd)


def ParseBuildingByLoop(buildings, tab):
    # logger.info(tab.size
    sib = tab.tr
    # print(sib)
    ParseItem(buildings, sib)

    for sib in tab.tr.next_siblings:
        # if (type(sib) == type(tab.tr)):
        if (isinstance(sib, type(tab.tr))):
            ParseItem(buildings, sib)


def ParseBuildingDetail(buildings, html):
    soup = BeautifulSoup(html, features="html.parser")
    datanow = soup.find(name="div", attrs={"class": "onbuildshow_contant"})
    datanow = datanow.find(
        name="div", attrs={"class": "onbuildshow_contant"})  # 嵌套的class
    tab = datanow.tbody
    ParseBuildingByLoop(buildings, tab)


def GetFirstPreSellId(build_info_url):
    logger.info("get first presell id, url: " + build_info_url)
    html = request_common.GetHtml(build_info_url)
    soup = BeautifulSoup(html)
    datanow = soup.find(
        name="div", attrs={
            "class": "lptypebar",
            "id": "building_dd"
        })
    datanow = soup.find(name="div", attrs={"class": "lptypebarin"})
    presell_id = ""
    tab = datanow.a
    i = 1
    for sib in tab.next_siblings:
        if (type(sib) == type(tab)):
            presell_id = sib.attrs["id"]
            logger.info(str(i) + "  " + str(presell_id))
            break

    id = presell_id.split('_')[1]
    logger.info("presell id: " + presell_id)
    return id


def GetPageCnt(base_url):
    logger.info("get page count, url: " + base_url)
    html = request_common.GetHtml(base_url)
    soup = BeautifulSoup(html)
    datanow = soup.find(name="div", attrs={"class": "spagenext"})
    # print(datanow.span.text)
    a = datanow.span.text
    # a = "页数 1/14	总数：189套（含限制房产）"
    logger.info(a)
    cnt = a.split("/")[1].split("	")[0]
    return cnt


def GetAndSavePriceInfo(bdinfo, files2mail):
    buildings = {}
    title = bdinfo.name
    build_info_url = request_common.GetHostUrl() + bdinfo.short_url
    presell_id = GetFirstPreSellId(build_info_url)
    url_param = "?isopen=&presellid=" + presell_id + "&buildingid=&area=&allprice=&housestate=&housetype=&page="
    base_url = request_common.GetHostUrl() + bdinfo.short_url + url_param
    strcnt = GetPageCnt(base_url)
    if not unicode(strcnt).isnumeric():
        logger.info("get total page count failed")
        return False

    cnt = int(strcnt)
    logger.info("total page count: " + str(cnt))
    all_page = []
    for num in range(1, cnt + 1):
        item_page = base_url + str(num)
        all_page.append(item_page)

    i = 1
    for url in all_page:
        time.sleep(1)
        logger.info("start parse, page: " + str(i))
        html = request_common.GetHtml(url)
        ParseBuildingDetail(buildings, html)
        logger.info("parse end, page: " + str(i))
        i = i + 1

    if (format_out.IsCanGoodFormat(buildings)):
        format_out.GoodOut(buildings, title, files2mail)
    else:
        format_out.SimpleOut(buildings, title, files2mail)

    return True
