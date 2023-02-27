from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetGribLand(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [GribLand]')
        driver.get("https://gribland.net/")
        find_all = []

        while len(find_all) < 2:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="servers-card")
            if len(find_all) < 2 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 2 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [GribLand]')
            result = {}

            for i in range(len(find_all)):
                j = find_all[i]
                if i == 0: get_name = 'OneBlock'
                else: get_name = 'Pixelmon'
                version = '1.7.10'
                get_online = j.find(class_='servers-card__heading-online__count').text

                arr = []
                arr.append([get_name + ' ' + version, get_online, 'Неизвестно'])
                result[get_name + ' ' + version] = arr
    
            driver.quit()
            AppendLogs(current_time, 'Get successful - [GribLand]')      
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [GribLand]')
                driver.quit()
                return None
            else:
                AppendLogs(current_time, 'Repeating - [GribLand]')
                driver.quit()
                return GetGribLand(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [GribLand]')
        driver.quit()
        return None