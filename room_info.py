# -*- coding: utf-8 -*-

from my_logger import logger


class RoomDetail:
    building = ''
    room = ''
    area = ''
    room_rate = ''
    real_area = ''
    record_price = ''
    decorate_price = ''
    total_price = ''
    stat = ''

    def __init__(self, building, room, area, room_rate, real_area, record_price,
                 decorate_price, total_price, stat):
        self.building = building
        self.room = room
        self.area = area
        self.room_rate = room_rate
        self.real_area = real_area
        self.record_price = record_price
        self.decorate_price = decorate_price
        self.total_price = total_price
        self.stat = stat

    def Print(self):
        logger.info(
            str(self.building) + str(self.room) + str(self.area) +
            str(self.room_rate) + str(self.real_area) + str(self.record_price) +
            str(self.decorate_price) + (self.total_price) + str(self.stat))
