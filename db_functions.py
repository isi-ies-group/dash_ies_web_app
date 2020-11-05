# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:18:04 2020

@author: GuillermoMatas
"""

from config import config
import pandas as pd
import numpy as np
import logging
import os

logger = logging.getLogger(__name__)

def createDataFrameFromQuery(df, columns, dates=None):
    if columns:
       
        logger.info('Columnas elegidas' + str(columns) + 'Fechas' + str(dates))
        
        datos = df[columns].loc[dates[0]:dates[1]]
        
        # ['V_Viento':, 'D_Viento':, 'Temp_Air':, 'Rad_Dir':, 'Ele_Sol', 'Ori_Sol', 'Top', 'Mid', 'Bot', 'Cal_Top', 'Cal_Mid', 'Cal_Bot', 'Pres_Aire']
        # 'v_viento', 'd_viento', 'temp_air', 'rad_dir', 'ele_sol', 'ori_sol', 'top', 'mid', 'bot', 'cal_top', 'cal_mid', 'cal_bot', 'pres_aire']
    
    else:
        datos = []    
    
    return datos

def getTimeIntervalDB(df):
   
    return [df.index[0].date(), df.index[-1].date()]