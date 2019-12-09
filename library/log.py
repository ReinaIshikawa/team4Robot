from datetime import datetime
f = open('log', 'a')

def info(message):
    save_log('INFO', message)

def error(message):
    save_log('ERROR', message)

def communication(message):
    save_log('COMMUNICATION', message)

def save_log(level, message):
    log = '[' + level + ']'
    log = log + '[' + get_time() + ']'
    log = log + ' ' + message + '\n'
    # print log
    f.write(log)

def close():
    if f:
        f.close()

def get_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
