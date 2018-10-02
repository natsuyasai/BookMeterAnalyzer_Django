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
from celery import shared_task
import sys
import os
from django.core.files import File
sys.path.append('../../')
from proj_bookmeteranalyzer import celery
from proj_bookmeteranalyzer import settings
sys.path.append('../../')
from bookmeteranalyzer import models
#********************************

# エントリポイント
@shared_task
def execAnalyze(userID : str) -> str:
    # データ取得
    scraping = BookMeterScraping(userID)
    bookInfoList = scraping.execScraping()
    # 解析実行
    analyzer = DataAnalyzer(bookInfoList, userID)
    # csv出力
    analyzer.outputCSV()
    # 月別読書量グラフ表示
    analyzer.protBarGraphForMonthReads()
    
    # DBに登録
    analyze_rslt = models.AnalyzeResult()
    # 結果の画像を登録
    img_filename = userID + '.png'
    img_file_path = settings.OUT_ROOT_DIR + img_filename
    img_open = open(img_file_path, 'rb')
    # 解析用csv登録
    csv_filename = userID + '.csv'
    csv_file_path = settings.OUT_ROOT_DIR + csv_filename
    csv_open = open(csv_file_path, 'rb')
    analyze_rslt.user_id = userID
    analyze_rslt.img_file.save(img_filename, File(img_open), save=True)
    analyze_rslt.csv_file.save(csv_filename, File(csv_open), save=True)
    img_open.close()
    csv_open.close()
    os.remove(img_file_path)
    os.remove(csv_file_path)
    return userID
