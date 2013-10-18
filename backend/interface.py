from helpers import FormHelpers
from helpers import NumberHelpers
from helpers import GeneralHelpers
from calendar_log import CalendarLog

def do_index():
    cal = CalendarLog("")
    #will returns a list of row_id's/None
    rows =  cal.index()
    return_str = "{\"entries\": ["
    for row in rows:
        return_str += "{"+GeneralHelpers.createJSONEntry("logID",str(row[0]))+","
        return_str += GeneralHelpers.createJSONEntry("logDate",str(row[1]))+"},"

    #if there was content parse off the last ,
    if rows:
         return_str = return_str[:-1]
    return return_str+"]}"

def do_select(cal):
    #returns note/Log
    log = cal.select_log()
    if log:
        return "{"+GeneralHelpers.createJSONEntry("logID",cal.logID)+", "+GeneralHelpers.createJSONEntry("logDate",log[1])+", "+GeneralHelpers.createJSONEntry("log",log[0])+"}"
    return "<no_log>"

def do_select_range(start,end,limit):
    cal = CalendarLog("")
    logs = cal.select_logs_range(start,end,limit)
    return_str = "{\"entries\": ["
    for row in logs or []:
        return_str += "{"+GeneralHelpers.createJSONEntry("logID",str(row[0]))+","
        return_str += GeneralHelpers.createJSONEntry("logDate",str(row[1]))+","
        return_str += GeneralHelpers.createJSONEntry("log",str(row[2]))+"},"

    #if there was content parse off the last ,
    if logs:
         return_str = return_str[:-1]
    return return_str+"]}"

def do_update(cal, text):
    #returns boolean
    if cal.update_log(text):
        return "<success>"
    else:
        return "<error>"

def do_update_date(cal,date):
    #returns boolean
    if cal.update_log_date(date):
        return "<success>"
    else:
        return "<error>"

def do_delete(cal):
    #returns boolean
    if cal.remove_log():
        #return the note id
        return "{"+GeneralHelpers.createJSONEntry("logID",cal.logID)+"}"
    else:
        return "<error>"

def do_add_log(data,date):
    cal = CalendarLog(None)
    log_id = cal.add_log(data,date)
    #Why return date?
    return "{"+GeneralHelpers.createJSONEntry("logID",log_id)+", "+GeneralHelpers.createJSONEntry("logDate",date)+"}"

def do_lock(n,new_pass):
    setpw =  n.set_password(new_pass)
    locked = "false"
    if setpw:
        locked = "true"
    return "{"+GeneralHelpers.createJSONEntry("logID",n.logID)+", "+GeneralHelpers.createJSONEntry("isLocked",locked)+"}"

def do_unlock(n, current_pass):
    if n.check_password(current_pass):
        setpw = n.set_password("")
        locked = "true"
        if setpw:
            locked = "false"
        return "{"+GeneralHelpers.createJSONEntry("logID",n.logID)+", "+GeneralHelpers.createJSONEntry("isLocked",locked)+"}"
    else:
        return "{"+GeneralHelpers.createJSONEntry("logID",n.logID)+", "+GeneralHelpers.createJSONEntry("isLocked","true")+"}"

def application(environ, start_response):
    is_get = False
    GET_allowed=["view_range"]
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        # When the method is POST the query string will be sent
        # in the HTTP request body which is passed by the WSGI server
        # in the file like wsgi.input environment variable.
        request_body = environ['wsgi.input'].read(request_body_size)
        d = FormHelpers.get_form(request_body)
    except (ValueError):
        #Assume its a get request
        is_get = True
        d = FormHelpers.get_form(environ['QUERY_STRING'])
    
    action = FormHelpers.get_input(d,'action')
    if action==None:
        print "ACTION IS NONE"
    else:
        print "RAY: "+action
        if(is_get):
            #Only allow certain requests as a get
            if action not in GET_allowed:
                print "ACTION not allowed"
                action=None

    response_body = "<error_interface>"
    #index,view,add,delete,update
    if action == "index":
        response_body = do_index()
    
    elif action == "add":
        data = FormHelpers.get_input(d,'data')
        date = FormHelpers.get_input(d,'date')
        if data and len(data) > 0 and date and len(date) >0:
            response_body = do_add_log(data,date)
    elif action =="view_range":
        print "view range"
        limit = FormHelpers.get_input(d,'limit')
        limit_param = None
        if limit and NumberHelpers.is_positive_integer(limit):
            limit_param = limit

        start_date = FormHelpers.get_input(d,'start')
        start_param = None
        print "start date"+str(start_date)
        if start_date and NumberHelpers.is_positive_integer(start_date):
            start_param = start_date

        end_date = FormHelpers.get_input(d,'end')
        end_param = None
        print "end date"+str(end_date)
        if end_date and NumberHelpers.is_positive_integer(end_date):
            end_param = end_date            

        print "response"
        response_body = do_select_range(start_param,end_param,limit_param)
        
    #The rest of these require the logs to be unlocked
    log_id = FormHelpers.get_input(d,'id')
    if NumberHelpers.is_positive_integer(log_id):
        log = CalendarLog(log_id)
        if log.is_locked():
            print "log "+str(log_id)+"is locked"
            if action == "unlock":
                password = str(FormHelpers.get_input(d,'password'))
                if password and len(password) > 0:
                    response_body = do_unlock(log,password)
            else:
                response_body = "{"+GeneralHelpers.createJSONEntry("logID",log_id)+", "+GeneralHelpers.createJSONEntry("isLocked","true")+"}"

        elif action =="view":
            response_body = do_select(log)

        elif action == "delete":
            response_body = do_delete(log)
            
        elif action == "update":
            data = FormHelpers.get_input(d,'data')
            if data:
                response_body = do_update(log,data)       
        
        elif action=="update_date":
            date = FormHelpers.get_input(d,'date')
            if date and len(date) > 0:
                response_body = do_update_date(log,date)

        elif action=="lock":
            password = FormHelpers.get_input(d,'password')
            if password and len(password) > 0:
                response_body = do_lock(log,password)

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]