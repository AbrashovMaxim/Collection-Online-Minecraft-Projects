from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def ClearString(s): return ' '.join(s.split())

def GetLoliLand(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [LoliLand]')
        driver.get("https://loliland.ru/")
        find_all = []

        while len(find_all) < 15:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="server")
            if len(find_all) < 15 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 15 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [LoliLand]')
            result = {}
            for i in find_all:
                get_Name = i.find(class_="server_name").text
                get_Version = i.find(class_="server_version").text
                arr = []
                for j in i.find_all(class_="server_mini"):
                    get_server_Name = j.find(class_="server_mini_name").text
                    get_Online_split = ClearString(j.find(class_="tooltip").text).split()
                    get_Online = get_Online_split[0]
                    arr.append([get_server_Name + ' ' + get_Version, get_Online, 100])
                result[get_Name + ' ' + get_Version] = arr
                    
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [LoliLand]')  
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [LoliLand]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [LoliLand]')
                try: driver.quit()
                except: pass
                return GetLoliLand(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [LoliLand]')
        try: driver.quit()
        except: pass
        return None