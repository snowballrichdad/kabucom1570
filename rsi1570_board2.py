import urllib.request
import json
import pprint
import time
import rsi1570_kick_watch
import rsi1570_settle_now
import rsi1570_settings

def board2():
    url = 'http://localhost:' + rsi1570_settings.port + '/kabusapi/board/' + rsi1570_settings.symbol + '@1'
    req = urllib.request.Request(url, method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', rsi1570_settings.token)

    try:
        print('###rsi1570_board2')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)
            curPrice = content["CurrentPrice"]

            # 現在価格が目標価格に達していたら即決済
            if(curPrice <= rsi1570_settings.orderPrice - rsi1570_settings.margin):
                rsi1570_settle_now.settle_now()
            else:
                #利食い注文(売り発注)
                rsi1570_kick_watch.kick_watch()

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import sys
    board2()