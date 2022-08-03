import datetime


def logger(data):
    with open('logs/logs.txt', 'a') as fd:
        fd.writelines(str(datetime.datetime.today()) + ': '+ str(data) + '\n')