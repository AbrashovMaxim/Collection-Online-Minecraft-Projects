from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetPentaCraft(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [PentaCraft]')
        driver.get("https://pentacraft.ru/")
        find_all = []

        while len(find_all) < 9:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="server-block")
            if len(find_all) < 9 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 9 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [PentaCraft]')
            result = {}
            for i in find_all:
                get_Online = i.find(class_="sb-counter").text
                get_Name = i.find("h3").text
                get_Type = i.find("span").text
                get_type_Version = get_Type.split()
                if not("недоступен" in get_Type): result[get_type_Version[0][:-1] + ' ' + get_type_Version[1]] = [[get_Name + " " + get_type_Version[len(get_type_Version)-1], get_Online, 'Неизвестно']]
                        
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [PentaCraft]')
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [PentaCraft]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [PentaCraft]')
                try: driver.quit()
                except: pass
                return GetPentaCraft(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [PentaCraft]')
        try: driver.quit()
        except: pass
        return None