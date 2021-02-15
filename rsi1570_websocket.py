import sys
import websocket
import _thread
import pprint
import json
import rsi1570_settings
import rsi1570i_cancelorder
import datetime
import urllib.request
import rsi1570_board
import time
import printNikkei

def on_message(ws, message):
    printNikkei.printWithTime('--- RECV MSG. --- ')
    #print(message)
    content = json.loads(message)
    pprint.pprint(content)
    curPrice = content["CurrentPrice"]
    pprint.pprint(curPrice)

    if(curPrice >= rsi1570_settings.orderPrice + rsi1570_settings.lossCutMargin):
        # キャンセルからの損切り注文
        rsi1570_settings.lossCutCnt += 1
        rsi1570i_cancelorder.cancelorder()
        rsi1570_settings.isAfterLossCut = True
        ws.close()

def on_error(ws, error):
    if len(error) != 0:
        printNikkei.printWithTime('--- ERROR --- ')
        print(error)

def on_close(ws):
    printNikkei.printWithTime('--- DISCONNECTED --- ')


def on_open(ws):
    printNikkei.printWithTime('--- CONNECTED --- ')
    def run():
        while(True):

            # 指定時間sleep
            time.sleep(rsi1570_settings.intervalCloseCheck)

            url = 'http://localhost:' + rsi1570_settings.port + '/kabusapi/orders'
            params = { 'product': 0, }
            req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method='GET')
            req.add_header('Content-Type', 'application/json')
            req.add_header('X-API-KEY', rsi1570_settings.token)

            try:
                with urllib.request.urlopen(req) as res:
                    print(res.status, res.reason)
                    for header in res.getheaders():
                        print(header)
                    print()
                    content = json.loads(res.read())
                    pprint.pprint(content)

                    # 注文情報を取得
                    lastOrder = content[len(content)-1]
                    print(lastOrder['State'])
                            
                    # 全約定の場合(売りが完了している場合)
                    if lastOrder['State'] == 5:

                        # まずはwebsoketを停止
                        printNikkei.printWithTime('closing...')
                        ws.close()
                        break
                    
                    # 手仕舞い時刻
                    nowtime = datetime.datetime.now()
                    if nowtime > rsi1570_settings.forceCloseTime:
                        # キャンセルからの損切り注文
                        rsi1570i_cancelorder.cancelorder()
                        ws.close()
                        break

            except urllib.error.HTTPError as e:
                print(e)
                content = json.loads(e.read())
                pprint.pprint(content)
            except Exception as e:
                print(e)



    _thread.start_new_thread(run, ())

def websocketA1():
    printNikkei.printWithTime('--- websocketA1 Start--- ')
    url = 'ws://localhost:' + rsi1570_settings.port + '/kabusapi/websocket'
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

    printNikkei.printWithTime('--- websocketA1 --- ')

    #再エントリチェック
    nowtime = datetime.datetime.now()
    
    if nowtime < rsi1570_settings.stopOrderTime:
        # ロスカットは2回したら終了
        if rsi1570_settings.lossCutCnt < 1:
            # 指定時間sleep後再び買い発注
            if rsi1570_settings.isAfterLossCut:
                rsi1570_settings.isAfterLossCut = False
                time.sleep(rsi1570_settings.intervalAfterLossCut)
            else:
                time.sleep(rsi1570_settings.intervalOrders)

            #念のためもろもろ変数初期化
            rsi1570_settings.orderPrice = 0
            rsi1570_settings.orderID = ""

            #再エントリ            
            rsi1570_board.board()


if __name__ == "__main__":
    import sys
    websocketA1()
