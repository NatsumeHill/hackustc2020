import re

timeStampReg = '(20\d{2}([\.\-/|年月\s]{1,3}\d{1,2}){2}日?(\s?\d{2}:\d{2}(:\d{2})?)?)|(\d{1,2}\s?(分钟|小时|天)前)'

def getLogTime(soup):
    reportTimeLogTag = soup.find_all('span', class_ = 'text-warning')
    reportTimeString = ''
    if reportTimeLogTag is not None and reportTimeLogTag.__len__() == 1:
        reportTimeString = re.search(timeStampReg, reportTimeLogTag[0].parent.text).group()
    return reportTimeString