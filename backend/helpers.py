#http://webpython.codepoint.net/wsgi_tutorial
from cgi import parse_qs, escape
import base64

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

class NumberHelpers:
    @staticmethod
    def is_positive_integer(number):
        if number:
            return number.isdigit()
        return False

class GeneralHelpers:
    @staticmethod
    def createJSONEntry(name,value):
        return "\""+str(name)+"\": \""+str(value)+"\""