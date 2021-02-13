import csv
import json
import os
import datetime


from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_path_to_export():
    _date = datetime.datetime.now().date()
    path_to_export = os.path.join(dir_path,'export',_date.strftime("%Y"),_date.strftime("%b"),_date.strftime("%d"))
    Path(path_to_export).mkdir(parents=True, exist_ok=True)

    return path_to_export

def export_json(data, fine_name):
    path_to_export = get_path_to_export()

    json_ = json.dumps(data, indent=4)
    export_to = os.path.join(path_to_export,fine_name + ".json")
    f = open(export_to,"w")
    f.write(json_)
    f.close()

    print("exported: " + export_to)

def export_csv(data, fine_name):
    path_to_export = get_path_to_export()

    export_to = os.path.join(path_to_export,fine_name + ".csv")
    with open(export_to,'w',newline="\n") as match_numbers_file:
        wr = csv.writer(match_numbers_file,quoting=csv.QUOTE_ALL)
        wr.writerows(data)

    print("exported: " + export_to)

response1_json = "response1.json"
response2_json = "response2.json"

response1_dict = {}
response2_dict = {}

with open(os.path.join(dir_path, response1_json)) as f:
    response1_dict = json.load(f)

with open(os.path.join(dir_path, response2_json)) as f:
    response2_dict = json.load(f)


"""
how this is working is..

if key in resposnse 1 doesnot exist in response 2 : add to new dict
if key in resposnse 1 exist in response 2 and value's does not match : add to new dict
"""

def getDictDif(d1, d2, _path = ""):
    for _key, _value in d1.items():
        path = _path
        if path == "":
            path = _key
        else:
            path += " -> " + _key

        if d2.get(_key):
            _type = type(_value)

            if _type == dict:
                path = getDictDif(d1[_key], d2[_key], path)
            elif _type == list:
                if len(d1[_key]) == len(d2[_key]):
                    for i, value in enumerate(d1[_key]):
                        a_path = path
                        a_path += " -> " + str(i) + " (index) "
                        getDictDif(d1[_key][i], d2[_key][i], a_path)
                else:
                    print("\n\nLIST length not matched -> " + path + " [ d1 length " + str(len(d1[_key])) + "] [ d2 length " + str(len(d2[_key])) + "] ")
            else:
                if d1[_key] != d2[_key]:
                    print("\n\nVALUE not matched -> " + path)
        else:
            print("\n\nKEY not matched -> " + path)
    return _path

response1_dict_results = response1_dict['results'][1]
response2_dict_results = response2_dict['results'][1]

getDictDif(response1_dict, response2_dict)
