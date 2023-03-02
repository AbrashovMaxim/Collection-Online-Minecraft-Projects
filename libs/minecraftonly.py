from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetMinecraftOnly(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [MinecraftOnly]')
        driver.get("https://minecraftonly.ru/")
        find_all = []

        while len(find_all) < 4:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_mon = soup.find(class_='monitoring')
            if find_mon != None: find_all = find_mon.find_all(class_="row")
            if len(find_all) < 4 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 19 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [MinecraftOnly]')
            result = {}

            for i in find_all:
                for j in i.find_all('div', recursive=False):
                    try:
                        get_name = j.find('span').text
                        get_online = int(j.find('font').text)
                        get_Max_Online_per = float(j.find(class_='circular-bar-chart')['data-percent'][:-1])
                        get_Max_Online = int((get_online*100)/get_Max_Online_per)
                        get_verion = j.find(class_='add_info').text

                        arr = []
                        arr.append([get_name + ' ' + get_verion, get_online, get_Max_Online])
                        result[get_name + ' ' + get_verion] = arr
                    except:
                        pass
    
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [MinecraftOnly]')  
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [MinecraftOnly]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [MinecraftOnly]')
                try: driver.quit()
                except: pass
                return GetMinecraftOnly(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [MinecraftOnly]')
        try: driver.quit()
        except: pass
        return None