#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import get_news
import building_price
import news_check
import email_op
import my_logger
import config as my_config
from my_logger import logger
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def main(argv=None):
    # init logger first
    my_logger.LoggerInit()
    # check opt
    if argv is None:
        argv = sys.argv

    config_file = argv[1]
    if config_file == '':
        logger.info("using default config file: price_cfg.json")
        config_file = './price_cfg.json'

    # load config
    config = my_config.LoadConfig(config_file)
    if config is None:
        logger.error("get config failed, config file is " + config_file)
        return 2

    # get check point
    news_check.LoadCheckPoint()

    all_ok = False
    a = True
    while (a):
        logger.info("start to get news presell buidings")
        buildings_alias_list = get_news.GetPreSellBuildingsAlias()
        bda_cnt = len(buildings_alias_list)
        logger.info("get news presell buidings, count: " + str(bda_cnt))
        if bda_cnt == 0:
            time.sleep(120)
            continue

        logger.info("start to tp get price detail and out to xls")
        files2mail = []
        update_info = get_news.PreSellInfo("", "")
        is_first = True
        for bdinfo in buildings_alias_list:
            logger.info("proc building: " + bdinfo.name)
            if is_first:
                update_info = bdinfo
                is_first = False
            all_ok = building_price.GetAndSavePriceInfo(bdinfo, files2mail)
            if not all_ok:
                logger.info(
                    "get and save price info failed, building alias : " +
                    bdinfo.name.encode(encoding='UTF-8'))

        if all_ok:
            logger.info("these files need to email: ")
            email_op.SendEMail(files2mail)
            news_check.UpdateCheckPoint(update_info)

        time.sleep(120)


if __name__ == "__main__":
    sys.exit(main())
