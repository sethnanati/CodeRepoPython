import json


def keyConfig():
    with open('prodPrivateConfig.ini', 'r') as f:
        contents = f.read()
        # f.close()
        conjson = json.loads(contents)
        #print(conjson)
    return conjson


keyConfig()
