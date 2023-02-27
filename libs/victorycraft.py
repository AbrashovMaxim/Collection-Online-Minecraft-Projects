from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetVictoryCraft(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [VictoryCraft]')
        driver.get("https://victorycraft.ru/")
        find_all = []

        while len(find_all) < 13:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find = soup.find(class_='sidebar-servers-list')
            if find != None: find_all = find.find_all("div", recursive=False)
            if len(find_all) < 13 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 13 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [VictoryCraft]')
            result = {}

            for i in find_all:
                get_split = i.find(class_='server-item__name').text.split()
                getName = get_split[1]
                if get_split[0][1:len(get_split[0])-1].lower() == 'новый': getVersion == '1.7.10'
                else: getVersion = get_split[0][1:len(get_split[0])-1]
                get_split = i.find(class_='server-item__amount').text.split()
                if len(get_split) > 1:
                    get_online = get_split[0]
                    get_Max_Online = get_split[2]
                else:
                    get_online = get_split[0]
                    get_Max_Online = get_split[0]
                arr = []
                arr.append([getName + ' ' + getVersion, get_online, get_Max_Online])
                result[getName + ' ' + getVersion] = arr
    
            driver.quit()
            AppendLogs(current_time, 'Get successful - [VictoryCraft]')  
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [VictoryCraft]')
                driver.quit()
                return None
            else:
                AppendLogs(current_time, 'Repeating - [VictoryCraft]')
                driver.quit()
                return GetVictoryCraft(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [VictoryCraft]')
        driver.quit()
        return None