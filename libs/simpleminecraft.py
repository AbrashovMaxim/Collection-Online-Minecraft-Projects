from bs4 import BeautifulSoup

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def ClearString(s): return ' '.join(s.split())

def GetSimpleMinecraft(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [SimpleMinecraft]')
        driver.get("https://simpleminecraft.ru/")

        find_all = []

        while len(find_all) < 23:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_common = soup.find(class_="monitoring_block")
            if find_common != None: find_all = find_common.find_all("div", recursive=False)
            if len(find_all) < 23 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 23 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [SimpleMinecraft]')
            result = {}
            getVersion = ''
            kolvo = 0
            type_server = ''
            arr = []
            for i in range(len(find_all)):
                j = find_all[i]
                if 'version_block' in j['class']:
                    getVersion = j.find('span').text.split()
                    getVersion = getVersion[len(getVersion)-1][:-1]
                elif 'servers_block' in j['class']:
                    type_server = ClearString(j.find('h4').text)
                    Max_Slots = j.find(class_='online_text').text.split()
                    Max_Slots = Max_Slots[len(Max_Slots)-1]
                    kolvo = int(j.find('b').text)
                elif 'servers_list' in j['class']:
                    for k in j.find_all(class_='server'):
                        title_server = k.find(class_='title').text
                        online_server = ClearString(k.find(class_='online').text)
                        arr.append([title_server + ' ' + getVersion, online_server, int(Max_Slots)//kolvo])
                    result[type_server + ' ' + getVersion] = arr
                    arr = []
    
            try: driver.quit()
            except: pass   
            AppendLogs(current_time, 'Get successful - [SimpleMinecraft]')    
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [SimpleMinecraft]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [SimpleMinecraft]')
                try: driver.quit()
                except: pass
                return GetSimpleMinecraft(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [SimpleMinecraft]')
        try: driver.quit()
        except: pass
        return None