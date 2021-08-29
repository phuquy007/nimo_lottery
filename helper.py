from datetime import datetime

def WriteLog(error, message = ""):
    f = open("logs.txt", "a")
    f.write(f'\n{datetime.now()}: {message} - {str(error)}')
    f.close()