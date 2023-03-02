from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetCenturyMine(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [CenturyMine]')
        driver.get("https://centurymine.net/")
        find_all = []

        while len(find_all) < 6:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="branch")
            if len(find_all) < 6 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 6 and check_kol == 10):
            result = {}
            AppendLogs(current_time, 'Get information - [CenturyMine]')
            for i in find_all:
                getName = i.find(class_='serverName').text
                getVersion = i.find(class_='version').text
                get_online = i.find(class_='now').text
                get_Max_Online = i.find(class_='slots').text.split()[1]
                arr = []
                arr.append([getName + ' ' + getVersion, get_online, get_Max_Online])
                result[getName + ' ' + getVersion] = arr
    
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [CenturyMine]')  
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [CenturyMine]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [CenturyMine]')
                try: driver.quit()
                except: pass
                return GetCenturyMine(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [CenturyMine]')
        try: driver.quit()
        except: pass
        return None