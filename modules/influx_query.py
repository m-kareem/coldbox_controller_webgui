from influxdb import InfluxDBClient
import datetime, time, statistics
import json
import GUIlogging
import GUIcoloredlogging

logging = GUIlogging.init_logger(__name__)
#logging = GUIcoloredlogging.init_logger(__name__)

def influx_init(config_influx):
    dbClient = InfluxDBClient(
            config_influx["influx_server"],
            config_influx["influx_port"],
            config_influx["influx_user"],
            config_influx["influx_pass"],
            None)

    #dbClient.switch_database(config_influx["influx_database"])
    return dbClient



#--example of influxQL
# >> SELECT T FROM "TrH" WHERE "device" = 'esp32test' ORDER BY time DESC LIMIT 1
#------------------------------
def get_measurement(dbClient, dbName, my_device, my_measurement, my_field):
    dbClient.switch_database(dbName)
    ResultSet = dbClient.query('SELECT * FROM'+' '+my_measurement+ ' GROUP BY * ORDER BY time DESC LIMIT 1;')
    points = list(ResultSet.get_points(measurement=my_measurement, tags={'device':my_device ,'validity': 'true'}))
    try:
        #logging.debug(my_device+" "+my_field+": " + str(points[0][my_field]))
        if points[0][my_field] is not None:
            return round(points[0][my_field],1)
    except IndexError:
        logging.error("list index out of range. Either the devise/measurement name does not exist in database, or has no value")
        return None

def convertStringToDatetime(time):
    if len(time) < 21:
        time = time.replace('Z', '.000Z') #add milliseconds, if missing in timestamp
    elif len(time) > 26:
        time = time[:-4] + 'Z' #strip off nanoseconds, which datetime cannot handle
    return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ') #2021-03-03T17:37:04.796Z

def get_measurement_range(dbClient, dbName, my_device, my_measurement, my_field, timeMin, timeMax, JSONOut = "measurement.json"):
    # check format of time given, it has to be in the format 2021-03-03T21:37:15.025486Z
    try:
        timeMin = datetime.datetime.strptime(timeMin, '%Y-%m-%dT%H:%M:%S.%fZ')
        timeMax = datetime.datetime.strptime(timeMax, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        print("ERROR! Time needs to given in format %Y-%m-%dT%H:%M:%S.%fZ")
        exit()
    
    # make sure the minimum time is the minimum time
    if timeMin > timeMax:
        print("ERROR! Minimum time greater than maximum time!")
        exit()

    # convert times back to timestamps
    timeMin = int(datetime.datetime.timestamp(timeMin) * 1e9)
    timeMax = int(datetime.datetime.timestamp(timeMax) * 1e9)

    print(timeMin, timeMax)

    # query datebase
    dbClient.switch_database(dbName)
    ResultSet = dbClient.query('SELECT ' + my_field + ' FROM'+' '+my_measurement+ ' WHERE time > ' + str(timeMin) + ' AND time < ' + str(timeMax) + ' GROUP BY * ORDER BY time;')
    points = list(ResultSet.get_points(measurement=my_measurement, tags={'device':my_device ,'validity': 'true'}))

    #calculate averages
    averageTimeList = []

    averageRangeSeconds = 60 #seconds
    minPoint = points[0]
    minPointTime = convertStringToDatetime(minPoint['time'])

    averageMeasurement = [minPoint[my_field]]
    for point in points: #points are time ordered
        pointTime = convertStringToDatetime(point['time'])

        if (pointTime - minPointTime).total_seconds() < averageRangeSeconds:
            averageMeasurement.append(point[my_field])
        else:
            dictOfMeasurement = {}
            dictOfMeasurement['minTime'] = minPoint['time']
            dictOfMeasurement['maxTime'] = point['time']
            dictOfMeasurement[my_field + "_average" + str(averageRangeSeconds)] = statistics.mean(averageMeasurement)
            dictOfMeasurement[my_field + "_stdev" + str(averageRangeSeconds)] = statistics.stdev(averageMeasurement)
            averageTimeList.append(dictOfMeasurement)

            minPoint = point
            minPointTime = convertStringToDatetime(minPoint['time'])
            averageMeasurement = [minPoint[my_field]]
            pointCounter = 0

    dictOfMeasurement = {}
    dictOfMeasurement['minTime'] = minPoint['time']
    dictOfMeasurement['maxTime'] = point['time']
    if len(averageMeasurement) > 1:
        dictOfMeasurement[my_field + "_average" + str(averageRangeSeconds)] = statistics.mean(averageMeasurement)
        dictOfMeasurement[my_field + "_stdev" + str(averageRangeSeconds)] = statistics.stdev(averageMeasurement)
    else:
        dictOfMeasurement[my_field + "_average" + str(averageRangeSeconds)] = point[my_field]
        dictOfMeasurement[my_field + "_stdev" + str(averageRangeSeconds)] = 0
    averageTimeList.append(dictOfMeasurement)

    # print(averageTimeList)

    # store to file
    if JSONOut:
        with open(JSONOut, 'w') as fp:
            json.dump(points, fp, indent=4)    
        with open(JSONOut.replace('.json', '_average' + str(averageRangeSeconds) + '.json'), 'w') as fpA:
            json.dump(averageTimeList, fpA, indent=4)    

    return averageTimeList

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
    _dbName = config_influx["influx_database"]

    print( get_measurement(_dbClient,_dbName,'esp32test','TrH','rH') )
    print( get_measurement(_dbClient,_dbName,'esp32test','TrH','T') )

    print( get_measurement_range(_dbClient,_dbName,'esp32test','TrH','T', '2021-03-03T15:00:00.000Z', '2021-03-03T17:37:00.000Z') )
