from bs4 import BeautifulSoup
import cssutils

import time

from libs.driverlib import DriverOptions
from libs.logs import AppendLogs

def GetMCSkill(kol, current_time):
    check_kol = 0
    try:
        driver = DriverOptions()
        AppendLogs(current_time, 'Driver loaded - [MCSkill]')
        driver.get("https://mcskill.net/")
        find_all = []

        while len(find_all) < 6:
            check_kol += 1
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            find_all = soup.find_all(class_="server-list")
            if len(find_all) < 6 and check_kol == 10: break
            time.sleep(5)
        
        if not(len(find_all) < 6 and check_kol == 10):
            AppendLogs(current_time, 'Get information - [MCSkill]')
            result = {}
            for i in find_all:
                getVers = i.find('center').text
                a = getVers.split()
                Version = []
                for j in range(1, len(a)): Version.append(a[j])
                Version = ' '.join(Version)
                for j in i.find_all(class_="server_item"):
                    getName = j.find(class_="collapsible-header").find("h3").text
                    arr = []
                    for k in j.find_all(class_="server_information"):
                        get_Name = k.find("h3").text
                        get_text_Online = k.find("span").text
                        get_text_Online_split = get_text_Online.split()
                        if len(get_text_Online_split) > 1: 
                            get_Online = int(get_text_Online_split[len(get_text_Online_split)-1])
                            span_style = i.find(class_='support_online_line')['style']
                            style = float(cssutils.parseStyle(span_style).width[:-1])
                            get_Max_Online = int((get_Online*100)/style)
                        else: 
                            get_Online = get_text_Online
                            get_Max_Online = 0
                        temp_arr = []
                        temp_arr.append(get_Name + ' ' + Version)
                        temp_arr.append(get_Online)
                        temp_arr.append(get_Max_Online)
                        arr.append(temp_arr)
                    
                    result[getName + ' ' + Version] = arr
                        
            driver.quit()
            AppendLogs(current_time, 'Get successful - [MCSkill]')  
            return result
        else:
            if kol == 3:
                AppendLogs(current_time, 'Warning - [MCSkill]')
                driver.quit()
                return None
            else:
                AppendLogs(current_time, 'Repeating - [MCSkill]')
                driver.quit()
                return GetMCSkill(kol+1, current_time)
    except Exception as e:
        AppendLogs(current_time, str(e) + ' - [MCSkill]')
        driver.quit()
        return None