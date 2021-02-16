import urllib.request
import json
import pprint
import rsi1570_websocket
import time
import rsi1570_settings

def kick_watch():
    # まずは利食い注文
    obj = { 'Password': rsi1570_settings.password,
            'Symbol': rsi1570_settings.symbol,
            'Exchange': 1,
            'SecurityType': 1,
            'Side': '2',
            'CashMargin': 3,
            'MarginTradeType': 1,
            'DelivType': 2,
            'AccountType': 4,
            'Qty': rsi1570_settings.qty,
            'ClosePositionOrder': 0,
            'Price': rsi1570_settings.orderPrice - rsi1570_settings.margin,
            'ExpireDay': 0,
            'FrontOrderType': 20}
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:' + rsi1570_settings.port + '/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', rsi1570_settings.token)

    try:
        print('###rsi1570_kick_watch:' + rsi1570_settings.port + ':' + str(rsi1570_settings.orderPrice))
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            #損切り監視用の注文IDを保存
            rsi1570_settings.orderID = content['OrderId']
            pprint.pprint(rsi1570_settings.orderID)

            #損切り用値監視
            rsi1570_websocket.websocketA1()
            
    except urllib.error.HTTPError as e:
        print('###kabusapi_sendorder2:HTTPError')
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print('###kabusapi_sendorder2:Exception')
        print(e)
        
if __name__ == "__main__":
    import sys
    kick_watch()