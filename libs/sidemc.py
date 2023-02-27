from bs4 import BeautifulSoup
import cssutils

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetSideMc(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [SideMC]')
        driver.get("https://sidemc.net/")
        find_all = []

        while len(find_all) < 6:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="panel-default")
            if len(find_all) < 6 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 6 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [SideMC]')
            result = {}

            for i in find_all:
                getName = i.find(class_='monitor-title').text
                try: get_online = int(i.find(class_='monitor-num').text)
                except: get_online = int(i.find(class_='monitor-num').text[:1])
                span_style = i.find(class_='monitor-line').find('span')['style']
                style = float(cssutils.parseStyle(span_style).width[:-1])
                if get_online == 0: get_Max_Online = 0
                else: get_Max_Online = int((get_online*100)/style)
                arr = []
                arr.append([getName, get_online, get_Max_Online])
                result[getName] = arr
    
            driver.quit()
            AppendLogs(current_time, 'Get successful - [SideMC]')
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [SideMC]')
                driver.quit()
                return None
            else:
                AppendLogs(current_time, 'Repeating - [SideMC]')
                driver.quit()
                return GetSideMc(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [SideMC]')
        driver.quit()
        return None