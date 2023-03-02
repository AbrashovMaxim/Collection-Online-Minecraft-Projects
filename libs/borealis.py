from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetBorealis(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [Borealis]')
        driver.get("https://borealis.su/")
        find_all = []

        while len(find_all) < 12:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="entry")
            if len(find_all) < 12 and check_kol == 10: break
            time.sleep(5)
        result = {}
        if not(len(find_all) < 12 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [Borealis]')
            for i in find_all:
                if not('total' in i['class']):
                    getName = i.find(class_='name').text
                    getVersion = i.find(class_='version').text
                    get_split = i.find(class_='online--text').text.split()[0].split('/')
                    get_online = get_split[0]
                    if len(get_split) > 1: get_Max_Online = get_split[1]
                    else: get_Max_Online = get_split[0]
                    arr = []
                    arr.append([getName + ' ' + getVersion, get_online, get_Max_Online])
                    result[getName + ' ' + getVersion] = arr
    
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [Borealis]')  
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [Borealis]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [Borealis]')
                try: driver.quit()
                except: pass
                return GetBorealis(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [Borealis]')
        try: driver.quit()
        except: pass
        return None