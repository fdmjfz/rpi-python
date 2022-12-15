import pandas as pd
import os
import serial
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2)
counter=0

data = pd.DataFrame(columns = ["T","H","P"])
try:
    while 1:
        x=ser.readline()
        b = x.decode("utf8").split(',')
        dic = {}
        try:
            for i in b:
                dic[ i.split(':')[0] ]= i.split(':')[1]
            row = pd.DataFrame( dic, index = [0])
            data = pd.concat( [data, row], ignore_index = True)
            print(row)
            print(len(data))
            
            if len(data) > 0:
                if not os.path.exists('data.csv'):
                    data.to_csv('data.csv', index=False)
                    print(f"Guardado data.csv \n Total registros: {len(data)} \n ================")

                else:
                    saved = pd.read_csv( 'data.csv')
                    pd.concat([saved, data], ignore_index = True).to_csv('data.csv', index = False)
                    print( f"Guardado data.csv. \n Total registros: {len(saved) + len(data)} \n ================")
                    
                #Reinicializamos el df data
                data = pd.DataFrame(columns = ["T","H","P"])
                    
            
        except:
            print("Sin datos")
except KeyboardInterrupt:
    print("Exiting")
