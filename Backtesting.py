# encoding: UTF-8

"""
展示如何执行策略回测。
"""

from __future__ import division

import pymongo
from vnpy.trader.vtGlobal import globalSetting

from vnpy.trader.vtObject import VtTickData, VtBarData

########################################################################
class BacktestingEngine(object):
    """
    CTA回测引擎
    函数接口和策略引擎保持一样，
    从而实现同一套代码从回测到实盘。
    """
    
    TICK_MODE = 'tick'
    BAR_MODE = 'bar'
    
    #----------------------------------------------------------------------
    def __init__(self):
        """初始化"""
        
        self.dbClient = None        # 数据库客户端
        self.dbCursor = None        # 数据库指针
        
        self.initData = []          # 初始化用的数据
        self.dbName = ''            # 回测数据库名
        self.symbol = ''            # 回测集合名
        
        
    #----------------------------------------------------------------------
    def output(self, content):
        """输出内容"""
        print str(datetime.now()) + "\t" + content
        
    #----------------------------------------------------------------------
    def setBacktestingMode(self, mode):
        """设置回测模式"""
        self.mode = mode
        
    #----------------------------------------------------------------------
    
    
    #----------------------------------------------------------------------    
    def load_History_Data(self):
        "加载历史数据"
        self.dbClient = pymongo.MongoClient(globalSetting['mongoHost'], globalSetting['mongoPort'])
        colledtion = self.dbClient[self.dbName][self.symbol]
        
        self.output(u'开始载入数据')
        
        # 首先根据回测模式，确认要使用的数据类
        if self.mode == self.BAR_MODE:
            dataClass = VtBarData
            func = self.newBar
        else:
            dataClass = VtTickData
            func = self.newTick
            
            
        
        