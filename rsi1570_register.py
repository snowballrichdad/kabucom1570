import urllib.request
import json
import pprint
import rsi1570_settings
import rsi1570_board

def register():
    obj = { 'Symbols':
            [ 
                {'Symbol': rsi1570_settings.symbol, 'Exchange': 1}
            ] }
    json_data = json.dumps(obj).encode('utf8')

    url = 'http://localhost:' + rsi1570_settings.port + '/kabusapi/register'
    req = urllib.request.Request(url, json_data, method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', rsi1570_settings.token)

#    settings.stoptime = settings.stoptime + settings.interval

    try:
        print('###register')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            # 値情報取得 & 買いエントリ
            rsi1570_board.board()

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import sys
    register()