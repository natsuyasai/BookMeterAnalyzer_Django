#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
読書メータ読了リスト管理情報取得用
"""


# import*************************
import sys
from .bookmetercrawling import BookMeterCrawling
from .bookmeterscraping import BookMeterScraping
from .bookmeterscraping import BookInfo
from .dataanalyzer import DataAnalyzer
from .debugprint import DebugPrint
#********************************

# エントリポイント
def execAnalyze(userID : str):
    # データ取得
    scraping = BookMeterScraping(userID)
    bookInfoList = scraping.execScraping()
    # 解析実行
    analyzer = DataAnalyzer(bookInfoList, userID)
    # csv出力
    analyzer.outputCSV()
    # 月別読書量グラフ表示
    analyzer.protBarGraphForMonthReads()
    # TODO:画像ファイル移動
