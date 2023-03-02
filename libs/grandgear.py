from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetGrandGear(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [GrandGear]')
        driver.get("https://grandgear.top/")
        find_all = []

        while len(find_all) < 7:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="server-item")
            if len(find_all) < 19 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 19 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [GrandGear]')
            result = {}

            for i in find_all:
                getName = i.find('h6').text
                get_online = i.find(class_='server-item__info-online').text
                get_Max_Online = i.find('p').text
                get_Max_Online = get_Max_Online.split()[1]
                arr = []
                arr.append([getName, get_online, get_Max_Online])
                result[getName] = arr
    
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [GrandGear]')   
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [GrandGear]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [GrandGear]')
                try: driver.quit()
                except: pass
                return GetGrandGear(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [GrandGear]')
        try: driver.quit()
        except: pass
        return None