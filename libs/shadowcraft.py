from bs4 import BeautifulSoup
import cssutils

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetShadowCraft(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [ShadowCraft]')
        driver.get("https://shadowcraft.ru/")
        find_all = []

        while len(find_all) < 7:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="block-monitor")
            if len(find_all) < 7 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 7 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [ShadowCraft]')
            result = {}

            for i in find_all:
                get_name = i.find('a').text
                get_split = get_name.split()
                if len(get_split) == 1: version = '1.7.10'
                else: version = get_split[1]
                get_online = int(i.find(class_='block-monitor-prs').text)
                if get_online == 0: get_Max_Online = 0
                else:
                    span_style =  i.find(class_='block-monitor-fix').find('span')['style']
                    style = float(cssutils.parseStyle(span_style).width[:-1])
                    get_Max_Online = int((get_online*100)/style)

                arr = []
                arr.append([get_name + ' ' + version, get_online, get_Max_Online])
                result[get_name + ' ' + version] = arr
    
            driver.quit()
            AppendLogs(current_time, 'Get successful - [ShadowCraft]')
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [ShadowCraft]')
                driver.quit()
                return None
            else:
                AppendLogs(current_time, 'Repeating - [ShadowCraft]')
                driver.quit()
                return GetShadowCraft(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [ShadowCraft]')
        driver.quit()
        return None