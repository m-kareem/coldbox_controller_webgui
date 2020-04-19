from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = 'petra.phys.yorku.ca'
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = ''
INFLUXDB_DATABASE = 'YorkDB'


dbClient = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
dbClient.switch_database(INFLUXDB_DATABASE)

def get_rH():
    ResultSet_rH = dbClient.query('SELECT * FROM rH GROUP BY * ORDER BY DESC LIMIT 1;')

    rH_points = list(ResultSet_rH.get_points(measurement='rH', tags={'validity': 'true'}))
    #print("rH: " + str(rH_points[0]['value']))
    return round(rH_points[0]['value'],1)



def get_Temperatur():
    ResultSet_T = dbClient.query('SELECT * FROM T GROUP BY * ORDER BY DESC LIMIT 1;')
    T_points = list(ResultSet_T.get_points(measurement='T', tags={'validity': 'true'}))
    #print("temperatur: " + str(T_points[0]['value']))
    return round(T_points[0]['value'],1)

if __name__ == '__main__':
    print('influxDB_query')
    get_rH()
    get_Temperatur()
