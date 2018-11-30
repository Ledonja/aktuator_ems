from pyModbusTCP.client import ModbusClient
import mysql.connector
from mysql.connector import errorcode
import requests
import time


def modbus_devices(register, value):
    c = ModbusClient(host="164.8.11.147", port=502, auto_open=True)
    # regs=c.read_holding_registers(33)
    # print(regs)
    regs = c.write_single_register(register, value)
    regs1 = c.read_holding_registers(register)
    print(regs1)


def klima(id, value):
    url = "http://164.8.11.12" + id + "/" + value
    response = requests.post(url)
    print(response)


def bojler(value):
    url = "http://164.8.11.128/" + value
    response = requests.post(url)
    print(response)


def sql_read():

    config = {
        'user': 'emspowerlab',
        'password': 'powerlab2017',
        'host': '164.8.11.146',
        'port': '3306',
        'database': 'ems',
        'raise_on_warnings': False
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)

    # Reading data from SQL database
    query = "SELECT activity, value FROM ems_history WHERE datetime > " \
            "NOW() - INTERVAL 60 MINUTE AND idsender = 1 AND idreceiver = 2 AND flag = 0"
    cursor.execute(query)
    frame = cursor.fetchall()
    print(frame)

    # Update flag to 1 in read frame
    # query = "UPDATE ems_history SET flag = 1 WHERE id = "

    # Writing data to SQL database
    query = "INSERT INTO ems_history (idsender, idreceiver, activity, value, datetime) VALUES (2, 1, 'b', 80, NOW())"
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    cnx.close()

def sql_write(self):
    return()

if __name__ == "__main__":
    sql_read()

    # while True:
    #     x = sql_read()
    #
    #     if x[0] == 1:
    #         if x[1] == 'Q':
    #             modbus_devices()
    #         elif x[1] == 'C':
    #             klima()
    #         elif x[1] == 'B':
    #             bojler()
    #         else:
    #             sql_write('Ni šlo blabla ')
    #     else:
    #         continue

    # klima(3,'ON')
    # bojler('ON')
    # modbus_devices(33,3)
