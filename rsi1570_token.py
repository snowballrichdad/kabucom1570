import urllib.request
import json
import pprint
import sys
import rsi1570_register
import rsi1570_settings

obj = { 'APIPassword': rsi1570_settings.apiPassword }
json_data = json.dumps(obj).encode('utf8')

url = 'http://localhost:' + rsi1570_settings.port + '/kabusapi/token'

req = urllib.request.Request(url, json_data, method='POST')
req.add_header('Content-Type', 'application/json')

try:
    print('###rsi1570_token')
    with urllib.request.urlopen(req) as res:
        print(res.status, res.reason)
        for header in res.getheaders():
            print(header)
        print()
        content = json.loads(res.read())
        pprint.pprint(content)
        token = content["Token"]
        rsi1570_settings.token = token
        #PUSh配信銘柄登録
        rsi1570_register.register()
except urllib.error.HTTPError as e:
    print(e)
    content = json.loads(e.read())
    pprint.pprint(content)
except Exception as e:
    print(e)
