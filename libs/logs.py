def CreateLogs():
    with open('logs.txt', 'w', encoding='utf-8') as f:
        f.write('')

def AppendLogs(current_time, text):
    hour = f'0{current_time.hour}' if current_time.hour < 10 else current_time.hour
    minute = f'0{current_time.minute}' if current_time.minute < 10 else current_time.minute
    seconds = f'0{current_time.second}' if current_time.second < 10 else current_time.second

    result = f'[{hour}:{minute}:{seconds}] - {text}'
    print(result)

    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.writelines(result+"\n")