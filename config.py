# -*- coding: utf-8 -*-

import json, os, sys
from my_logger import logger

g_config = {}


def GetConfig():
    global g_config
    return g_config


def LoadConfig(json_file):
    global g_config
    logger.info("config file is " + json_file)
    with open(json_file, 'r') as b_oj:
        settings = json.load(b_oj)
    g_config = settings
    return g_config


if __name__ == "__main__":
    LoadConfig("./price_cfg.json")
    config = GetConfig()
    print(type(config))
    print(config)
    print(config['remote_server'])
    print(config['email'])
    print(config['email']['reciever'])
