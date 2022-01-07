import mysql.connector

'''
GLOBAL
'''
connection_Data = {
 'user': 'root',
 'password': '123',
 'host': '127.0.0.1',
 'database': 'GasStation'
}

connection
cursor

'''
FUNCTIONS
'''
def connect():
    global connection
    global cursor
    connection = mysql.connector.connect(**connection_Data)
    cursor = connection.cursor(buffered=True)

def insertDB(dataList):
    global cursor
    global connection
    connect()
    dataInsert = "INSERT INTO GasStation "
    "(Name_GasStation, Brand_Gas, Street_Addr,Number_Addr, Neighbor_Addr, City_Addr, State_Addr, Country_Addr, Latitude, Longitude) "
    "VALUES ("+dataList[0]+","+dataList[1]+","+dataList[2][0]+","+dataList[2][1]+","+dataList[3]+","+dataList[4]+ ","+dataList[5]+","+dataList[6]+","+dataList[9]+","+dataList[10]+")"
    cursor.execute(dataInsert)
    connection.commit()
    cursor.close()
    connection.close()

def insertGasPriceDB(dataList):
    global cursor
    global connection
    connect()
    data = queryGasStationID(dataList)
    data2 = queryFuelID(dataList[7])
    dataInsert = "INSERT INTO GasStation_has_fuel (GasStation_idGasStation, Fuel_idFuel, Cost_Fuel) "
    "VALUES ("+data[0]+","+data2[0]+dataList[8]+")"
    cursor.execute(dataInsert)
    connection.commit()
    cursor.close()
    connection.close()

def queryFuelID(gasType):
    global cursor
    gasIdQuery = "SELECT idFuel FROM Fuel WHERE Type_Fuel = "+gasType
    return cursor.execute(gasIdQuery)

def queryGasStationID(dataList):
    global cursor
    query = "SELECT idGasStation FROM GasStation WHERE Number_addr = %s AND Latitude = %s AND Longitude = %s"
    return cursor.execute(query,(dataList[2][1],dataList[9],dataList[10]))

def updateGasPriceDB():
    return 0




