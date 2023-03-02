from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def ClearString(s): return ' '.join(s.split())


def GetCubixWorld(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [CubixWorld]')
        driver.get("https://cubixworld.net/")
        find_all = []
        while len(find_all) < 19:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="server")
            if len(find_all) < 19 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 19 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [CubixWorld]')
            pol_result = {}
            for i in find_all:
                get_version = ClearString(i.find(class_="version").text)
                get_name = ClearString(i.find("a", {"class": "serverName"}).text)
                if get_version.split()[0] == 'MOBILE': get_name += "-Mobile"
                pol_result[get_name] = get_version
            result = {}
            for i in driver.find_elements(By.CSS_SELECTOR, 'span.quantityServers'):
                try: i.click()
                except: continue
                miniServers = []
                while len(miniServers) != 1:
                    html = driver.page_source
                    soup = BeautifulSoup(html, "lxml")
                    miniServers = soup.find_all(class_="miniServers")
                mini_Servers = []
                while len(mini_Servers) == 0:
                    html = driver.page_source
                    soup = BeautifulSoup(html, "lxml")
                    mini_Servers = soup.find_all(class_="miniServer")
                nameServer = ''
                arr = []
                for j in mini_Servers:
                    getName = j.find(class_="serverName").text
                    getNameSplit = getName.split()
                    getOnline = j.find(class_="quantityServers").text
                    getOnineSplit = getOnline.split()
                    nameServer = getNameSplit[0]
                    temp_arr = []
                    getVers = pol_result[nameServer].split()
                    temp_arr.append(getName + " " + getVers[len(getVers)-1])
                    temp_arr.append(getOnineSplit[0])
                    temp_arr.append(getOnineSplit[len(getOnineSplit)-1])
                    arr.append(temp_arr)
                getVers = pol_result[nameServer].split()
                result[nameServer + " " + getVers[len(getVers)-1]] = arr
            try: driver.quit()
            except: pass
            AppendLogs(current_time, 'Get successful - [CubixWorld]')   
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [CubixWorld]')
                try: driver.quit()
                except: pass
                return None
            else:
                AppendLogs(current_time, 'Repeating - [CubixWorld]')
                try: driver.quit()
                except: pass
                return GetCubixWorld(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [CubixWorld]')
        try: driver.quit()
        except: pass
        return None
        