# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import request_common
import news_check
from my_logger import logger


class PreSellInfo:
    name = ''
    short_url = ''

    def __init__(self, name, short_url):
        self.name = name
        self.short_url = short_url


def IsNewBuildingsAlias(short_url):
    return news_check.IsNewsBuilding(short_url)


def ParseBuildingInfo(tr, infos):
    td = tr.td
    name = td.a.text.strip()
    url = ''
    for sib in td.next_siblings:
        if (type(sib) == type(td)):
            url = sib.a.attrs['href']
            break

    if not IsNewBuildingsAlias(url):
        logger.info("Had Save This Building Info: " + name)
        return False

    infos.append(PreSellInfo(name, url))
    logger.info("Need To Save This Building Info: " + name)
    return True


def GetPreSellBuildingsAlias():
    idx_url = request_common.GetHostUrl() + "/index.jsp"
    html = request_common.GetHtml(idx_url)
    soup = BeautifulSoup(html, features="html.parser")
    datanow = soup.find(name="div", attrs={"class": "ysz_cont"})
    tbody = datanow.find(name="table", attrs={"class": "gridtable6"})
    infos = []

    # first item
    tr = tbody.tr
    if not ParseBuildingInfo(tr, infos):
        return infos

    # next items
    for sib in tr.next_siblings:
        # if (type(sib) == type(tbody.tr)):
        if (isinstance(sib, type(tbody.tr))):
            if not ParseBuildingInfo(sib, infos):
                return infos

    return infos
