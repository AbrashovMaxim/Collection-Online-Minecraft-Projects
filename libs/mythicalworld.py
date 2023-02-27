from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetMythicalWorld(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [MythicalWorld]')
        driver.get("https://mythicalworld.su/")
        find_all = []

        while len(find_all) < 6:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="right-block-content-item")
            if len(find_all) < 6 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 6 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [MythicalWorld]')
            result = {}

            for i in find_all:
                getName = i.find('b').text.split()
                if len(getName) == 2: getVersion = getName[1]; getName = getName[0]
                else: getVersion = '1.7.10'; getName = getName[0]
                get_split = i.find('span').text.split()
                get_online = get_split[0]
                get_Max_Online = get_split[2]
                arr = []
                arr.append([getName + ' ' + getVersion, get_online, get_Max_Online])
                result[getName + ' ' + getVersion] = arr
    
            driver.quit()
            AppendLogs(current_time, 'Get successful - [MythicalWorld]')
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [MythicalWorld]')
                driver.quit()
                return None
            else:
                AppendLogs(current_time, 'Repeating - [MythicalWorld]')
                driver.quit()
                return GetMythicalWorld(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [MythicalWorld]')
        driver.quit()
        return None