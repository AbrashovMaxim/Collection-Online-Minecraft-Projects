from bs4 import BeautifulSoup
import cssutils

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetGravityCraft(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [GravityCraft]')
        driver.get("https://gravitycraft.net/")
        find_common = None

        while find_common == None:
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_common = soup.find(class_="servers")
        
        find_all = []

        while len(find_all) < 39:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_common = soup.find(class_="servers")
            find_all = find_common.find_all("div", recursive=False)
            if len(find_all) < 39 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 39 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [GravityCraft]')
            result = {}
            getVersion = ''
            type_server = ''
            arr = []
            for i in range(len(find_all)):
                j = find_all[i]
                if 'version_block' in j['class']:
                    getVersion = j.find('span').text.split()
                    getVersion = getVersion[len(getVersion)-1]
                elif 'server-info' in j['class']:
                    get_divs = j.find("div").find('div').find_all("div", recursive=False)
                    type_server = get_divs[1].find('a').text
                elif 'server-mini' in j['class']:
                    for k in j.find_all(class_='server-info'):
                        title_server = k.find('a').text
                        try: online_server = int(k.find('span').text)
                        except: online_server = 0
                        if online_server == 0: get_Max_Online = 0
                        else:
                            span_style = k.find(class_='progress-bar')['style']
                            style = float(cssutils.parseStyle(span_style).width[:-1])
                            get_Max_Online = int((online_server*100)/style)

                        arr.append([title_server + ' ' + getVersion, online_server, get_Max_Online])
                    result[type_server + ' ' + getVersion] = arr
                    arr = []
    
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [GravityCraft]')  
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [GravityCraft]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [GravityCraft]')
                try: driver.quit()
                except: pass
                return GetGravityCraft(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [GravityCraft]')
        try: driver.quit()
        except: pass
        return None