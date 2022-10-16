import requests
import json

def getJSONFiles():
    deptList = requests.get('http://luthers-list.herokuapp.com/api/deptlist/')
    deptList_json = json.loads(deptList.text)

    for i in range(len(deptList_json)):
        dept = deptList_json[i].get("subject")
        class_request = "http://luthers-list.herokuapp.com/api/dept/" + dept
        dept_classes = requests.get(class_request)
        dept_classes_json = json.dumps(dept_classes.text)

        file_name = "JSON/" + dept + '.json'
        with open(file_name, "w") as outfile:
            outfile.write(dept_classes_json)