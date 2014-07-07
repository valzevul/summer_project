import json
 
 
class SuperHandler:
    def call_up_encoding(self, *args):
        return json.dumps({"header": str(args[0]), "content": str(args[1])})
 
    def call_up_decoding(self, json_object):
        dict = json.loads(json_object)
        return dict["header"], dict["content"]

    def call_up_multiple_encoding(self, data_to_be_handled):
        list_to_be_returned = []
        dict = json.loads(data_to_be_handled)
        for i in dict.values():
            i = i.replace('\'', '\"')
            list_to_be_returned.append(self.call_up_decoding(i))
        return list_to_be_returned
 
 
"""
l = json.dumps({"id1": "{'content': 'Dfff', 'header': '\u0412\u0430\u0441\u044f'}", "id2": "{'content': 'Dfff', 'header': '\u0412\u0430\u0441\u044f'}"})
s = SuperHandler()
print s.call_up_multiple_encoding(l)
"""