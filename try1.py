import requests
import json


try:
    response = requests.get("http://192.168.43.10:8080/smartduskbin/calcitem.php")
    todos = json.loads(response.text)
    print (todos)
    if "rue" in response.text:
        ReadOrWrite = 1
        print("same")
    else:
        ReadOrWrite = 0
        print("not same")
except:
    print ("Failed to connect to server")
