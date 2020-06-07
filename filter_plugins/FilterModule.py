#!/usr/bin/env/ python

import json
import yaml

class FilterModule:

    ##    with open ('/home/elil/Yml/ansible/hub_output.json', 'r') as f:
    ##        data = json.load(f)

    @staticmethod
    def filters():              # define custom filters derived froclass methods ata functions
        return {'check_for_qos': FilterModule.check_for_qos,
                'create_class_map': FilterModule.create_class_map,
                'get_variable': FilterModule.get_variable,
                'cfg_to_erase': FilterModule.cfg_to_erase,
                'check_wanted_class': FilterModule.check_wanted_class
                } 

    @staticmethod
    def check_for_qos(data):  # constructs list of policy maps from output
        global policy_map
        for line in data['Qos_Config']:
            if 'parent-10m' in line:
                policy_map = line
            else:
                for line in data['Qos_Config']:
                    if 'parent-' in line:
                        policy_map = line
        return policy_map

    @staticmethod                   # constructs list of class maps from output 
    def check_wanted_class(data):
        global class_list
        class_list = []
        for line in data['Qos_Config']:
            if 'class' in line:
                if line.split()[1] != 'class-default':
                    class_list.append(line.split()[1])
        return class_list

    @staticmethod                  # CHECK???  constructs list of  class maps from output  
    def create_class_map(data):
        global wanted_clist
        wanted_clist = []
        for line in data['Class_Config']:
            if line.startswith('class'):
                FilterModule.check_wanted_class(data)
                if line.split()[2] in class_list:
                    wanted_clist.append(line)
        return wanted_clist

    @staticmethod
    def cfg_to_erase(data):       # Collects names of policy-maps and class-maps from the output
        qos_list = []
        class_map_list = []
        global_qos_list = [qos_list, class_map_list]
        _data = []
        for line in data:
            _data.append(line.strip())
        for _line in _data:
            if _line == '':
                _data.remove(_line)
        for _line in _data:
            if "output" in _line:
                qos_list.append(_line.split()[2])
            elif ("Service-policy" in _line) and ("output" not in _line):
                qos_list.append(_line.split()[2])
            elif (_line.startswith("Class-map")) and ("class-default" not in _line):
                class_map_list.append(_line.split()[1])
        return global_qos_list

    @staticmethod
    def get_variable(variable):
        var = variable
        return int(var)



