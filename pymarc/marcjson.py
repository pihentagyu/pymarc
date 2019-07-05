"pymarc marcjson file."

from pymarc import Field, Record, JSONReader
import json, re

class JsonHandler:
    def __init__(self):
        self.records = []
        self._record = None
        self._field = None
        self._text = []

    def element(self,element_dict,name=None):
        if not name:
            self._record = Record()
            self.element(element_dict,'leader')
        elif name == 'leader':
            self._record.leader = element_dict[name]
            self.element(element_dict,'fields')
        elif name == 'fields':
            fields = iter(element_dict[name])
            for field in fields:
                tag, remaining = field.popitem()
                self._field = Field(tag)
                if self._field.is_control_field():
                    self._field.data = remaining
                else:
                    self.element(remaining,'subfields')
                    self._field.indicators.extend([
                        remaining['ind1'],
                        remaining['ind2']
                    ])
                self._record.add_field(self._field)
            self.process_record(self._record)
        elif name == 'subfields':
            subfields = iter(element_dict[name])
            for subfield in subfields:
                code, text = subfield.popitem()
                self._field.add_subfield(code,text)
    def elements(self,dict_list):
        if type(dict_list) is not list:
            dict_list = [dict_list]
        for rec in dict_list:
            self.element(rec)
        return self.records
    def process_record(self, record):
        self.records.append(record)

def parse_json_to_array(json_file):
    json_reader = JSONReader(json_file)
    handler = JsonHandler()
    return handler.elements(json_reader.records)