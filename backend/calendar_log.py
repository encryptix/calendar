from db import DB

class Notes:
    #Database names
    database = "NOTES"
    note_id = "id"
    data = "data"
    name= "name"
    password = "password"
    #Actual Note ID
    noteID = None

    def __init__(self,noteID):
        self.DB = DB(self.database, self.note_id)
        self.noteID = noteID
    
    def noteID(self):
        return noteID

    def index(self):
        return self.DB.select_all([self.note_id ,self.name],None,None,None)

    def select_note(self):
        row = self.DB.select_one(self.noteID, [self.data])
        if row:
            return str(row[0])
        return None
    
    def update_note(self, text):
        return self.DB.update(self.noteID,[self.data],[text])
    
    def update_note_name(self,name):
        return self.DB.update(self.noteID,[self.name],[name])

    def add_note(self,text,name):
        return self.DB.insert([self.data,self.name,self.password],[text,name,None])

    def remove_note(self):
        return self.DB.remove(self.noteID)

    def check_password(self, password):
        row = self.DB.select_one(self.noteID,[self.password])
        actual_password = row[0]
        if actual_password != None:
            actual_password = str(actual_password)

        if password != None and str(password) == actual_password:
            return True
        return False

    def set_password(self,new_pass):
        return self.DB.update(self.noteID,[self.password],[new_pass])

    def is_locked(self):
        row = self.DB.select_one(self.noteID,[self.password])
        password = row[0]
        if password==None or len(str(password)) == 0:
            return False
        else:
            return True
