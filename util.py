import re
import secret

def removeEmotes(text):
    return re.sub(r'<.*:[0-9]*>', '', text)

def removeLeadSpaces(text):
    return re.sub(r'^ *', '', text)

def removeURLs(text):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', text)

def removeNonAscii(text):
    return re.sub(r'[^\x00-\x7F]', '', text)

def checkBot(text):
    return re.match(r'bot', text)

def formatBytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 2**10 

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit

token = secret.token