import schedule
import time

from datetime import datetime
from dbxintegrationlocal import *

def job():
#    path = '/Online portal/DATA'
#    check_for_change(path)
    now= datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    m=str(now)
    print("date", m)
    s= str(getupdate())
#    print("result  ",getupdate(), "\n\n")
    f = open("upadtedfiles.txt","a")
    f.write(m)
    f.write(s)
    f.close()

schedule.every(1).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("11:23").do(job)
#schedule.every(5).to(10).minutes.do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)