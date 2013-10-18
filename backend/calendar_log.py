from db import DB

class CalendarLog:
    #Database names
    database = "CALENDAR"
    entry_id = "id"
    data = "data"
    date= "date"
    password = "password"
    #Actual log ID
    logID = None

    def __init__(self,logID):
        self.DB = DB(self.database, self.entry_id)
        self.logID = logID
    
    def logID(self):
        return logID

    def index(self):
        return self.DB.select_all([self.entry_id ,self.date],None,None,None)
    
    def select_log(self):
        row = self.DB.select_one(self.logID, [self.data, self.date])
        return row

    def select_logs_range(self,start,end,limit):
        if start and end:
            return self.DB.select_all([self.entry_id ,self.date, self.data],[self.date+" >=", "AND "+self.date+" <="],[start,end],limit)
        elif start:
            return self.DB.select_all([self.entry_id ,self.date, self.data],[self.date+" >="],[start],limit)
        elif end:
            return self.DB.select_all([self.entry_id ,self.date, self.data],[self.date+" <="],[end],limit)
        else:
            return self.DB.select_all([self.entry_id ,self.date, self.data],None,None,limit)

    def update_log(self, text):
        return self.DB.update(self.logID,[self.data],[text])
    
    def update_log_date(self,date):
        return self.DB.update(self.logID,[self.date],[date])

    def add_log(self,text,date):
        return self.DB.insert([self.data,self.date,self.password],[text,date,None])

    def remove_log(self):
        return self.DB.remove(self.logID)

    def check_password(self, password):
        row = self.DB.select_one(self.logID,[self.password])
        actual_password = row[0]
        if actual_password != None:
            actual_password = str(actual_password)

        if password != None and str(password) == actual_password:
            return True
        return False

    def set_password(self,new_pass):
        return self.DB.update(self.logID,[self.password],[new_pass])

    def is_locked(self):
        row = self.DB.select_one(self.logID,[self.password])
        password = row[0]
        if password==None or len(str(password)) == 0:
            return False
        else:
            return True
