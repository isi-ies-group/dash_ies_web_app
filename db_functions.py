# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:18:04 2020

@author: GuillermoMatas
"""

from config import config
import pandas as pd
import numpy as np

from sqlalchemy import create_engine

from datetime import datetime as dt


def createSQLEngine():
    db_params = config()

    engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**db_params)

    return create_engine(engine_string)


def createTempTable(db_engine):
    try:
        db_engine.connect().execute('''
                CREATE TABLE IF NOT EXISTS dataset AS(
                    SELECT
                        helios.measure_date helios_date, 
                        helios.measure_utc_time helios_utc_time, 
                        geonica.measure_date geonica_date, 
                        geonica.measure_utc_time geonica_utc_time,
                        helios.g_0,
                        helios.g_41, helios.d_0, helios.b,
                        helios.w_vel, helios.w_dir, 
                        helios.t_amb helios_t_amb,
                        geonica.v_viento,
                        geonica.d_viento, geonica.temp_air, geonica.rad_dir,
                        geonica.ele_sol, geonica.ori_sol,
                        geonica.top, geonica.mid, geonica.bot,
                        geonica.cal_top, geonica.cal_mid, geonica.cal_bot,
                        geonica.pres_aire
                   FROM
                        helios
                   FULL JOIN geonica USING(measure_date, measure_utc_time)
                   ORDER BY helios.id
                   );
    
                   ALTER TABLE dataset
                   ADD measure_date DATE;
    
                   UPDATE dataset SET measure_date=
                       CASE
                           WHEN helios_date ISNULL THEN geonica_date
                           WHEN geonica_date ISNULL THEN helios_date
                           ELSE geonica_date
                       END;
    
                   ALTER TABLE dataset
                   ADD measure_utc_time TIMETZ;
    
                   UPDATE dataset SET measure_utc_time=
                   	CASE
                           WHEN helios_utc_time ISNULL THEN geonica_utc_time
                           WHEN geonica_utc_time ISNULL THEN CAST(helios_utc_time AS TIME)
                           ELSE geonica_utc_time
                   	END;
    
                   ALTER TABLE dataset
                       DROP helios_date;
                   ALTER TABLE dataset
                       DROP helios_utc_time;
                   ALTER TABLE dataset
                       DROP geonica_date;
                   ALTER TABLE dataset
                       DROP geonica_utc_time;
                '''
                                    )
    finally:
        return db_engine


def createDataFrameFromQuery(columns, dates=None):
    if columns:
        db_engine = createSQLEngine()
        db_engine = createTempTable(db_engine)
        
        # #Extract info from query
        column_string = "measure_date, measure_utc_time, "+", ".join(columns)
        
        try:
            if not dates:
                query = ("SELECT {} FROM dataset ORDER BY measure_date, measure_utc_time".format(column_string))
            else:
                query = "SELECT {} FROM dataset WHERE measure_date BETWEEN '{}' AND '{}' ORDER BY measure_date, measure_utc_time".format(column_string, str(dates[0]), str(dates[1]))
            
            df = pd.read_sql_query(query, con=db_engine)
        
        
        
            # #Creación de la columna datetime
            df['measure_utc_dt'] = df['measure_date']
            for i in range(len(df['measure_utc_dt'])):
                df['measure_utc_dt'][i] = dt.combine(df['measure_date'][i], df['measure_utc_time'][i])
            
            # #Reorganización de las columnas
            cols = df.columns.tolist()
            cols = cols[-1:]+cols[:-1]
            df = df[cols]
            # #Relleno de los valores nulos
            # df.fillna('NaN', inplace=True)
        
        finally:
            # #Delete table 'dataset'
            db_engine.connect().execute("DROP TABLE IF EXISTS dataset")
    
    else:
        df=[]    
    
    return df


def getTimeIntervalDB():
    db_engine = createSQLEngine()
    db_engine = createTempTable(db_engine)
    db_data = pd.read_sql_query('''SELECT DISTINCT 
                                                measure_date 
                                            FROM 
                                                dataset 
                                            WHERE 
                                                measure_date=
                                                    (SELECT MIN(measure_date) FROM dataset) 
                                                OR 
                                                measure_date=
                                                    (SELECT MAX(measure_date) FROM dataset)
                                            ORDER BY 
                                                measure_date;''',
                                                con=db_engine)

    db_engine.connect().execute("DROP TABLE IF EXISTS dataset")

    # #Extract info from query
    db_date_interval = []
    for row in list(db_data['measure_date']):
        db_date_interval.append(row)

    return db_date_interval
