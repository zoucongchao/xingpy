# encoding: UTF-8

"""
ahourth:zou
展示如何执行策略回测。
"""

from __future__ import division

import pymongo
from vnpy.trader.vtGlobal import globalSetting

from vnpy.trader.vtObject import VtTickData, VtBarData
from vnpy.trader.app.ctaStrategy.ctaBase import MINUTE_DB_NAME

from datetime import datetime,timedelta

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
        self.collection = None
        
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
    def setStartDate(self, startDate='20100416', initDays=10):
        """设置回测的启动日期"""
        self.startDate = startDate
        self.initDays = initDays
        
        self.dataStartDate = datetime.strptime(startDate, '%Y%m%d')
        #print self.dataStartDate
        
        initTimeDelta = timedelta(initDays)
        #print initTimeDelta
        
        self.strategyStartDate = self.dataStartDate + initTimeDelta
        
        #print self.strategyStartDate
        
    #----------------------------------------------------------------------
    def setDatabase(self, dbName, symbol):
        """设置历史数据所用的数据库"""
        self.dbName = dbName
        self.symbol = symbol
        
    #----------------------------------------------------------------------
    def setEndDate(self, endDate=''):
        """设置回测的结束日期"""
        self.endDate = endDate
        
        if endDate:
            self.dataEndDate = datetime.strptime(endDate, '%Y%m%d')
            #print self.dataEndDate
            
            # 若不修改时间则会导致不包含dataEndDate当天数据
            self.dataEndDate = self.dataEndDate.replace(hour=23, minute=59)
            #print self.dataEndDate
        
                   
    #----------------------------------------------------------------------    
    def load_History_Data(self):
        self.setDatabase(MINUTE_DB_NAME, 'IF0000')
        "加载历史数据"
        self.dbClient = pymongo.MongoClient(globalSetting['mongoHost'], globalSetting['mongoPort'])
        self.collection = self.dbClient[self.dbName][self.symbol]
        
        self.output(u'开始载入数据')
        
        """
        # 首先根据回测模式，确认要使用的数据类
        if self.mode == self.BAR_MODE:
            dataClass = VtBarData
            func = self.newBar
        else:
            dataClass = VtTickData
            func = self.newTick
        """
            
        # 载入初始化需要用的数据
        flt = {'datetime':{'$gte':self.dataStartDate,
                           '$lt':self.strategyStartDate}}        
        self.initCursor = self.collection.find(flt).sort('datetime')
        
        
        # 载入回测数据
        if not self.dataEndDate:
            flt = {'datetime':{'$gte':self.strategyStartDate}}
        else:
            flt = {'datetime':{'$gte':self.strategyStartDate,
                               '$lte':self.dataEndDate}}
        self.dbCursor = self.collection.find(flt).sort('datetime')
       
        
                               
                       
        
        
        
aa =  BacktestingEngine()

bb = aa.setStartDate() 

ee = aa.setEndDate(endDate='20160508') 

dd = aa.load_History_Data()
    
        
