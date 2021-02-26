import datetime
import sys

port = "18080"
apiPassword = "kabuステーションのAPIパスワードを入力"
password = "kabuステーションのログインパスワードを入力"
symbol = "1570"
qty = 1
margin = 200
side = "1"
side_settle = "2"
lossCutMargin = 200
intervalAfterOrder = 10
intervalOrders = 600
intervalCloseCheck = 10
intervalAfterLossCut = 600
token = ""
orderPrice = 0
orderID = ""
nowtime = datetime.datetime.now()
stopOrderTime = nowtime.replace(hour=11, minute=30)
forceCloseTime = nowtime.replace(hour=14, minute=50)
morningStartTime = nowtime.replace(hour=9, minute=00)
morningStopTime = nowtime.replace(hour=11, minute=00)
lossCutCnt = 0
isAfterLossCut = False

rsi_threshold = 60.0
sd_threshold = 100.0

if len(sys.argv) >= 2:
    if sys.argv[1] == "debug":
        port = "18081"
        apiPassword = "kabuステーションのデバッグ用APIパスワードを入力"
        #デバッグ時に変更したい設定値を以下に入力
        intervalOrders = 1

print("###stopOrderTime:" + str(stopOrderTime))
