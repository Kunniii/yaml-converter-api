import logging as log
import os

# Create ./logs/app.log
try:
    os.mkdir('./logs')
    os.system('touch ./logs/api.log')
# If folder exsits, do nothing
except:
    pass

logFormatter = log.Formatter("%(asctime)s [ %(name)s ]  [ %(threadName)s ]  [ %(levelname)s ]  %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
rootLogger = log.getLogger()

rootLogger.setLevel(log.DEBUG)

fileHandler = log.FileHandler("./logs/api.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = log.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

def write_log(level:int, mesage:str):
    # 1 is debug
    if level == 1:
        rootLogger.debug(mesage)
    # 2 is info
    elif level == 2:
        rootLogger.info(mesage)
    # 3 is warning
    elif level == 3:
        rootLogger.warning(mesage)
    # 4 is error
    elif level == 4:
        rootLogger.error(mesage)
    # 5 is crtitical
    elif level == 5:
        rootLogger.critical(mesage)

# for testing
if __name__ == '__main__':
    write_log(1, "Write debug")
    write_log(2, "Write info")
    write_log(3, "Write warning")
    write_log(4, "Write error")
    write_log(5, "Write critical")