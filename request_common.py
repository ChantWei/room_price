# -*- coding: utf-8 -*-
import urllib2
import traceback
from my_logger import logger
import config as my_config


def GetHostUrl():
    config = my_config.GetConfig()
    return config['remote_server']['host_url']


def GetHtml(url):
    config = my_config.GetConfig()
    cookie = config['remote_server']['cookie']
    html = ""
    request = urllib2.Request(
        url,
        headers={
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
        })
    request.add_header("Cookie", cookie)
    while (True):
        try:
            response = urllib2.urlopen(request, timeout=60)
            html = response.read()
            break
        except urllib2.HTTPError, e:
            traceback.print_stack()
            logger.info(e.code)
            logger.error(e.reason)
            logger.error(traceback)

    return html
