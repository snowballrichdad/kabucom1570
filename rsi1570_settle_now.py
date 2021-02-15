import urllib.request
import json
import pprint
import rsi1570_settings
import sys

#損切り決済注文
def settle_now():
    obj = { 'Password': rsi1570_settings.password,
            'Symbol': rsi1570_settings.symbol,
            'Exchange': 1,
            'SecurityType': 1,
            'Side': rsi1570_settings.side_settle,
            'CashMargin': 3,
            'MarginTradeType': 1,
            'DelivType': 2,
            'AccountType': 4,
            'Qty': rsi1570_settings.qty,
            'ClosePositionOrder': 0,
            'Price': 0,
            'ExpireDay': 0,
            'FrontOrderType': 10}
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:' + rsi1570_settings.port + '/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', rsi1570_settings.token)

    try:
        print('###sendorderA4')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)
    finally:
        sys.exit()

if __name__ == "__main__":
    import sys
    
    settle_now()