# flake8: noqa

# In[]:
# Controls for webapp
MAGNITUDE_SYMBOLS = {
    "g_0": "G(0) (W/m^2)",
    "g_41": "G(41) (W/m^2)",
    "d_0": "D(0) (W/m^2)",
    "b": "B - 1 (W/m^2)",
    "w_vel": "Wind Speed - 1  (m/s)",
    "w_dir": "Wind Direction - 1 (º)",
    "helios_t_amb": "Air Temperature - 1 (ºC)",
    "v_viento": "Wind Speed - 2 (m/s)",
    "d_viento": "Wind Direction - 2 (º)",
    "temp_air": "Air Temperature - 2 (ºC)",
    "rad_dir": "B - 2 (W/m^2)",
    "ele_sol": "\u03B1 (º)",  # #unicode (alpha)
    "ori_sol": "\u03D5 (º)",  # #unicode (phi)
    "top": "Top (W/m^2)",
    "mid": "Mid (W/m^2)",
    "bot": "Bot (W/m^2)",
    # "cal_top": "Cal Top (W/m^2)",
    # "cal_mid": "Cal Mid (W/m^2)",
    # "cal_bot": "Cal Bot (W/m^2)",
    "pres_aire": "Air Pressure (mBar)",
    "hr": "Relative Humidity (%)", # param nuevo
    "lluvia": "Precipitation (mm)", # param nuevo
}

MAGNITUDE_LABELS = {
    "measure_utc_time": "UTC Time",
    "measure_date": "Date",
    "measure_utc_dt": 'UTC DateTime',
    "g_0": "Global Horizontal Irradiance",
    "g_41": "Global Tilted Irradiance",
    "d_0": "Diffuse Horizontal Irradiance",
    "b": "Direct Normal Irradiance - 1",
    "w_vel": "Wind Speed - 1",
    "w_dir": "Wind Direction - 1",
    "helios_t_amb": "Air Temperature - 1",
    "v_viento": "Wind Speed - 2",
    "d_viento": "Wind Direction - 2",
    "temp_air": "Air Temperature - 2",
    "rad_dir": "Direct Normal Irradiance - 2",
    "ele_sol": "Sun Elevation Angle",
    "ori_sol": "Sun Azimuth",
    "top": "Top",
    "mid": "Mid",
    "bot": "Bot",
    "cal_top": "Cal Top",
    "cal_mid": "Cal Mid",
    "cal_bot": "Cal Bot",
    "pres_aire": "Air Pressure",
    "hr": "Relative Humidity",
    "lluvia": "Precipitation",
}


UNITS = {
    "measure_utc_time": "(HH:MM)",
    "measure_date": "(yyyy-mm-dd)",
    "measure_utc_dt": "(HH:MM, yyyy-mm-dd)",
    "g_0": "(W/m^2)",
    "g_41": "(W/m^2)",
    "d_0": "(W/m^2)",
    "b": "(W/m^2)",
    "w_vel": "(m/s)",
    "w_dir": "(rad)",
    "helios_t_amb": "(ºC)",
    "v_viento": "(m/s)",
    "d_viento": "(º)",
    "temp_air": "(ºC)",
    "rad_dir": "(W/m^2)",
    "ele_sol": "(º)",
    "ori_sol": "(º)",
    "top": "(W/m^2)",
    "mid": "(W/m^2)",
    "bot": "(W/m^2)",
    "cal_top": "(W/m^2)",
    "cal_mid": "(W/m^2)",
    "cal_bot": "(W/m^2)",
    "pres_aire": "(mBar)",
    "hr": "(%)",
    "lluvia": "(mm)",
}

VAR_CATEGORIES = {
    "date_time": ["measure_utc_time", "measure_date", "measure_utc_dt"],
    "irradiance": ["g_0", "g_41", "d_0", "b", "rad_dir", "top", "mid", "bot",
                   "cal_top", "cal_mid", "cal_bot"],
    "temperature": ["helios_t_amb", "temp_air"],
    "sun angle": ["ele_sol", "ori_sol"],
    "pressure": ["pres_aire"],
    "wind speed": ["w_vel", "v_viento"],
    "wind direction": ["w_dir", "d_viento"],
    "relative humidity": ["hr"],
    "precipitation": ["lluvia"],
}

DATATABLE_OPTION = {
    "none": "None",
    "plot_data": "Displayed data",
    "full_data": "Full Dataset"
}

SENSORS_DESCRIPTION = {
    "Global Horizontal Irradiance": "Eppley - PSP",
    "Global Tilted Irradiance": "Eppley - PSP",
    "Diffuse Horizontal Irradiance": "Eppley - PSP",
    "Direct Normal Irradiance - 1": "Eppley - NIP",
    "Wind Speed - 1": "GILL - Windsonic",
    "Wind Direction - 1": "GILL - Windsonic",
    "Air Temperature - 1": "Young -YSI44031",
    "Wind Speed - 2": "GILL - Windsonic",
    "Wind Direction - 2": "GILL - Windsonic",
    "Air Temperature - 2": "Geonica - STH-S331",
    "Direct Normal Irradiance - 2": "Kipp & Zonen - CHP1",
    "Top": "SAV - ICU-3J25 Spectroheliometer",
    "Mid": "SAV - ICU-3J25 Spectroheliometer",
    "Bot": "SAV - ICU-3J25 Spectroheliometer",
    "Air Pressure": "Young - 61302L",
    "Relative Humidity": "Geonica - STH-S331",
    "Precipitation": "Pronamic - DK-8600",
}

HELP_BTN = {
    # identifier: {header: header_text, body: body_text}
    'date': {'header': 'Select Time interval', 'body': 'This option allows the user to choose the date range to be displayed'},
    'graph_var': {'header': 'Select Variable\n to Plot', 'body': 'This option allows the user to choose the variables to plot:\n'+''.join(f'* {k} ({v})\n' for k,v in SENSORS_DESCRIPTION.items())},
    'datatable': {'header': 'Select DataTable visibility options', 'body': 'This option allows the user to choose among "None", "Displayed data" and "Full Dataset"'},
    'download': {'header': "Download Full Dataset", 'body': 'This option allows the user to download a CSV file containing all the variables data between the selected dates.'}
}

