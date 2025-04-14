import dfLink
import time

#端末設定---------------------
#端末keyを指定してください。
pkey='xokRnzg2uFV1KNQQSGqs'
#-------------------------------------------

#シリアルポートを入力-------------------------
#serial_serch.pyでシリアルポートを検索してください
serial_port='/dev/tty.usbmodem101'
#-------------------------------------------
#Arduinoとのシリアル通信設定-------------------
my_arduino = dfLink.set_serial(serial_port,9600)
#-------------------------------------------


# --------------------------------------------------------------
while True:

    # IoTサーバーからデータの取得----------------------------------------------------
    data_list = dfLink.getData_From_dfLink(pkey=pkey)
    # リスト形式で取得される
    print(data_list)
    # --------------------------------------------------------------
    #最初データ（0番目)の塊の中の2番目のデータを読みたい（0から始まるので、本当は3番目)
    try:
        int_data =int(data_list[0][2])
        print(int_data)
        
        # int_dataが1だったら、'1'を送信(点灯させる）、それ以外の時は'0'を送る(消灯させる）
        if int_data==1:
            to_arduino = '1';
        else:
            to_arduino = '0';


        #Arduinoにデータを送る
        my_arduino.write(to_arduino.encode())
    except:
        print("データなし")

    time.sleep(1)#指定した秒数を待つ（msでなく秒なので、注意）　　
