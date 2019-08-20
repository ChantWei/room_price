# -*- coding: utf-8 -*-

import time
import xlwt
import price_common
from my_logger import logger


def insertrecord(writebuildings, row, queue, rd, high=0, wide=0):
    # if not writebuildings.has_key(row):
    if row not in writebuildings:
        writebuildings[row] = []
    queuelist = writebuildings.get(row)
    queuelist.append([queue, rd, high, wide])


def IsCanGoodFormat(buildings):
    for rd_list in buildings.values():
        for rd in rd_list:
            rd.Print()
            room = price_common.getRoomNum(rd.room)
            if room.isdigit():
                return True
            else:
                return False


def SimpleFormat(buildings):
    return


def GoodFromat(buildings):
    return


def SimpleOut(buildings, title, files2mail):
    xlfile = xlwt.Workbook(encoding='utf-8')
    xltable = xlfile.add_sheet(title)
    xllines = 1
    for rd_list in buildings.values():
        for rd in rd_list:
            # rd.Print()
            xltable.write(xllines, 0, rd.building)
            xltable.write(xllines, 1, rd.room)
            xltable.write(xllines, 2, rd.area)
            xltable.write(xllines, 3, rd.room_rate)
            xltable.write(xllines, 4, rd.real_area)
            xltable.write(xllines, 5, rd.record_price)
            xltable.write(xllines, 6, rd.decorate_price)
            xltable.write(xllines, 7, rd.total_price)
            xltable.write(xllines, 8, rd.stat)

            xllines = xllines + 1

    postfix = time.strftime("_%Y%m%d_%H%M%S.xls", time.localtime())
    filename = "./" + title + postfix

    xlfile.save(filename)
    files2mail.append(filename)
    return True


def GoodOut(buildings, title, files2mail):
    logger.info("----------- GoodOut: " + title)
    for rd_list in buildings.values():
        rd_list.sort(key=price_common.takeSecond, reverse=True)

        mosthighlevl = 1
        maxroomonelevel = 2
        # 遍历builingmap
        fmtbuildings = {}
        for k, rd_list in buildings.items():
            # 获取楼幢 及 单元
            tmpbuilding, tmpUnit = price_common.getBuilding(k)

            # 获取 楼幢的 单元map
            if tmpbuilding not in fmtbuildings:
                fmtbuildings[tmpbuilding] = {}
            tmpUnitMap = fmtbuildings.get(tmpbuilding)

            if tmpUnit not in tmpUnitMap:
                tmpUnitMap[tmpUnit] = {}
            levelMap = tmpUnitMap.get(tmpUnit)

            # 遍历 每栋里的房间
            for rd in rd_list:
                level = int(price_common.getRoomNum(rd.room)) / 100
                if level > mosthighlevl:
                    mosthighlevl = level
                if level not in levelMap:
                    levelMap[level] = []
                roomlist = levelMap.get(level)
                roomlist.append(rd)
                if len(roomlist) > maxroomonelevel:
                    maxroomonelevel = len(roomlist)

    writebuildings = {}
    startrow = 1
    startqueue = 2
    bdst = sorted(fmtbuildings.iteritems(), key=price_common.bd_sort_key)
    for bditem in bdst:
        bd = bditem[0]
        utmp = bditem[1]
        startqueue = startqueue + 2
        currow = startrow
        curqueue = startqueue
        startqueue = startqueue + 2 + (len(utmp) * maxroomonelevel)

        # 楼幢
        bdqueue = curqueue + (len(utmp) * maxroomonelevel) / 2
        logger.info(currow, bdqueue, bd)
        insertrecord(writebuildings, currow, bdqueue, bd)
        unitrow = currow + 1
        unitidx = 1
        leftlevelqueue = curqueue - 1

        rightlevelqueue = curqueue + (len(utmp) * maxroomonelevel)
        roomstartqueue = curqueue
        needlevelqueue = True

        utst = sorted(utmp.iteritems(), key=price_common.ut_sort_key)
        for utitem in utst:
            ut = utitem[0]
            lvmp = utitem[1]
            # 单元
            unitqueue = curqueue + maxroomonelevel * (unitidx - 1)
            logger.info(unitrow, unitqueue, ut)
            insertrecord(writebuildings, unitrow, unitqueue, ut)
            levelrow = unitrow + 2
            roomstartqueue = unitqueue

            realneedlevelqueue = True
            if needlevelqueue:
                realneedlevelqueue = True
                needlevelqueue = False
            else:
                realneedlevelqueue = False

            lvst = sorted(lvmp.iteritems(), reverse=True)

            for roommark in range(0, maxroomonelevel):
                insertrecord(writebuildings, unitrow + 1,
                             roomstartqueue + roommark,
                             str(roommark + 1) + u'号室', 0, 5000)

            for lvitem in lvst:
                lv = lvitem[0]
                rl = lvitem[1]
                if realneedlevelqueue:
                    logger.info(levelrow, leftlevelqueue, lv)
                    logger.info(levelrow, rightlevelqueue, lv)
                    insertrecord(writebuildings, levelrow, leftlevelqueue,
                                 str(lv) + u'楼')
                    insertrecord(writebuildings, levelrow, rightlevelqueue,
                                 str(lv) + u'楼')
                curroomqueue = roomstartqueue
                curroomrow = levelrow
                for rmdt in rl:
                    logger.info(curroomrow, curroomqueue, rmdt.room)
                    detail = rmdt.area + "\n" + rmdt.record_price + "\n" + rmdt.total_price
                    insertrecord(writebuildings, curroomrow, curroomqueue,
                                 detail, 3000, 0)
                    curroomqueue = curroomqueue + 1

                levelrow = levelrow + 1
            unitidx = unitidx + 1

    # logger.info('-------------')

    xlfile = xlwt.Workbook(encoding='utf-8')
    xltable = xlfile.add_sheet(title)
    for row, ql in writebuildings.items():
        for queuerecord in ql:
            logger.info(str(row) + str(queuerecord[0]) + str(queuerecord[1]))
            xltable.write(row, queuerecord[0], queuerecord[1])
            if queuerecord[2] != 0:
                xltable.row(row).height = queuerecord[2]

            if queuerecord[3] != 0:
                xltable.col(queuerecord[0]).width = queuerecord[3]
    postfix = time.strftime("_%Y%m%d_%H%M%S.xls", time.localtime())
    filename = "./" + title + postfix
    xlfile.save(filename)
    files2mail.append(filename)
    return True
