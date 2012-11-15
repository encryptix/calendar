#http://webpython.codepoint.net/wsgi_tutorial
from cgi import parse_qs, escape

class FormHelpers:
    @staticmethod
    def get_form(request_body):
        return parse_qs(request_body)
        
    @staticmethod
    def get_input(data,identifier):
        if data and identifier:
            try:
                return escape(data.get(identifier)[0])
            except:
                print "exception"
                return None
        return None

    @staticmethod
    def get_input_list(data,identifier):
        if data and identifier:
            try:
                d = data.get(identifier, []) # Makes a list
                return [escape(a) for a in d]
            except:
                return None
        return None