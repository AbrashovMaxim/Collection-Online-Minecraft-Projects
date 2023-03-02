from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetExcaliburCraft(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [ExcaliburCraft]')
        driver.get("https://excalibur-craft.ru/")

        find_all = []
        while len(find_all) < 13:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="complex")
            if len(find_all) < 13 and check_kol == 10: break
            time.sleep(5)
        if not(len(find_all) < 13 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [ExcaliburCraft]')
            result = {}
            for i in find_all:
                get_name = i.find(class_="complex-name")
                get_name_vers = get_name.find("span").find("img").get("alt")
                get_name_vers = get_name_vers.split(" ") # Type 0 | Vers 1
                get_servers = i.find_all(class_="server")
                servers = []
                for j in get_servers:
                    get_name_and_online = j.find_all("span")
                    servers.append([get_name_and_online[0].text+" "+get_name_vers[1][:-1], get_name_and_online[1].text, get_name_and_online[2].text]) # 0 - Название | 1 - Онлайн | 2 - Кол-во слотов
                if len(servers) > 0:
                    result[get_name_vers[0] + " " + get_name_vers[1][:-1]] = servers

            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [ExcaliburCraft]')
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [ExcaliburCraft]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [ExcaliburCraft]')
                try: driver.quit()
                except: pass
                return GetExcaliburCraft(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [ExcaliburCraft]')
        try: driver.quit()
        except: pass
        return None