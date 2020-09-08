from influxdb import InfluxDBClient


def influx_init(config_influx):
    dbClient = InfluxDBClient(
            config_influx["influx_server"],
            config_influx["influx_port"],
            config_influx["influx_user"],
            config_influx["influx_pass"],
            None)

    dbClient.switch_database(config_influx["influx_database"])
    return dbClient



#--example of influxQL
# >> SELECT T FROM "TrH" WHERE "device" = 'esp32test' ORDER BY time DESC LIMIT 1
#------------------------------
def get_measurement(dbClient, my_device, my_measurement, my_field):
    ResultSet = dbClient.query('SELECT * FROM'+' '+my_measurement+ ' GROUP BY * ORDER BY time DESC LIMIT 1;')
    points = list(ResultSet.get_points(measurement=my_measurement, tags={'device':my_device ,'validity': 'true'}))
    try:
        #print(my_device+" "+my_field+": " + str(points[0][my_field]))
        if points[0][my_field] is not None:
            return round(points[0][my_field],1)
    except IndexError:
        print("list index out of range. Either the devise/measurement name does not exist in database, or has no value")
        return None


if __name__ == '__main__':
    print('--- influxDB_query ---')
    #-- these configs are for test, when runniing this module individually.
    config_influx = {
        "influx_server": 'petra.phys.yorku.ca',
        "influx_port": 8086,
        "influx_user": 'admin',
        "influx_pass": '',
        "influx_database": 'ESP32test',
    }
    _dbClient = influx_init(config_influx)

    print( get_measurement(_dbClient,'esp32test','TrH','rH') )
    print( get_measurement(_dbClient,'esp32test','TrH','T') )
