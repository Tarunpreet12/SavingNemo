import MySQLdb

class DbConnect(object):
    """ Db Class"""
    
    def __init__(self, config):
        self.connection = MySQLdb.connect(
                            host=config['MYSQL_HOST'], \
                            port=config['MYSQL_PORT'], \
                            user=config['MYSQL_USER'], \
                            passwd=config['MYSQL_PASSWORD'], \
                            db=config['MYSQL_DB'])
        
    def getLoggerTypes(self):
        """Fetches Distinct Logger Types"""
        cursor = self.connection.cursor()
        query = '''select lt.type from cnx_logger_type lt'''
        cursor.execute(query)
        result = cursor.fetchall()
        result = list(result)
        final_result = [[row[0], row[0]] for row in result]
        cursor.close()
        return final_result

    def getCountry(self, logger_type):
        """Fetches Distinct countries given logger type"""
        cursor = self.connection.cursor()
        query = '''
            select distinct lg.country from cnx_logger_type lt 
            inner join cnx_logger l 
            on l.biomimic_id=lt.bioid 
            inner join cnx_logger_geographics lg 
            on l.geo_id=lg.gid 
            where lt.type=\'''' + logger_type + "\'"
        cursor.execute(query)
        result = cursor.fetchall()
        result = set(result)
        final_result = [[row[0], row[0]] for row in result]
        cursor.close()
        return final_result

    def getState(self, logger_country):
        """Fetches Distinct states given logger type and logger country"""
        cursor = self.connection.cursor()
        query = '''
            select distinct (lg.state) from cnx_logger_type lt
            inner join cnx_logger l on l.biomimic_id=lt.bioid
            inner join cnx_logger_geographics lg on l.geo_id=lg.gid
            where lg.country=\'''' + logger_country + "\'"
        cursor.execute(query)
        result = cursor.fetchall()
        result = set(result)
        final_result = [[row[0], row[0]] for row in result]
        cursor.close()
        return final_result

    def getLocation(self, logger_state):
        """Fetches Distinct locations given logger type and logger country"""
        cursor = self.connection.cursor()
        query = '''
            select distinct (lg.location) from cnx_logger_type lt
            inner join cnx_logger l on l.biomimic_id=lt.bioid
            inner join cnx_logger_geographics lg on l.geo_id=lg.gid
            where lg.state=\'''' + logger_state + "\'"
        cursor.execute(query)
        result = cursor.fetchall()
        result = set(result)
        final_result = [[row[0], row[0]] for row in result]
        cursor.close()
        return final_result

    def getZone(self, logger_type):
        """Fetches Distinct Zones given logger type"""
        cursor = self.connection.cursor()
        query = '''
            select distinct (p.zone) 
            from cnx_logger_type lt
            inner join cnx_logger l on l.biomimic_id=lt.bioid
            inner join cnx_logger_properties p on p.lpropId = l.prop_id
            where lt.type=\''''+logger_type + "\'"
        cursor.execute(query)
        result = cursor.fetchall()
        result = set(result)
        final_result = [[row[0], row[0]] for row in result]
        cursor.close()
        return final_result

    def getSubZone(self, logger_type):
        """Fetches Distinct Subzones given logger type"""
        cursor = self.connection.cursor()
        query = '''
            select distinct (p.subzone) 
            from cnx_logger_type lt
            inner join cnx_logger l on l.biomimic_id=lt.bioid
            inner join cnx_logger_properties p on p.lpropId = l.prop_id
            where lt.type=\''''+logger_type + "\'"
        cursor.execute(query)
        result = cursor.fetchall()
        result = set(result)
        final_result = [[row[0], row[0]] for row in result]
        cursor.close()
        return final_result

    def getWaveExp(self, logger_type):
        """Fetches Distinct Wave Exp given logger type"""
        cursor = self.connection.cursor()
        query = '''
            select distinct (p.wave_exp) 
            from cnx_logger_type lt
            inner join cnx_logger l on l.biomimic_id=lt.bioid
            inner join cnx_logger_properties p on p.lpropId = l.prop_id
            where lt.type=\''''+logger_type + "\'"
        cursor.execute(query)
        result = cursor.fetchall()
        result = list(result)
        final_result = set()
        for row in result:
            if row[0] is None:
                final_result.add(("None", "None"))
            else:
                final_result.add((row[0], row[0]))        
        cursor.close()
        return final_result

    def getQueryResults(self, queryDict):
        """Fetches records form tables based on user query"""
        cursor = self.connection.cursor()
        where_condition = " where lt.type=\'"+queryDict.get('logger_type')+\
                          "\' and lg.country=\'"+queryDict.get('country_name')+"\'"# and t.date_time BETWEEN \'"+queryDict.get('start_date')+"\' AND \'"+queryDict.get('end_date')+"\'"
        if queryDict.get('state_name') != 'None':
            where_condition += " and lg.state=\'"+queryDict.get('state_name')+"\'"
        if queryDict.get('location_name') != 'None':
            where_condition += " and lg.location=\'"+queryDict.get('location_name')+"\'"
        if queryDict.get('zone_name') != 'None':
            where_condition += " and p.zone=\'"+queryDict.get('zone_name')+"\'"
        if queryDict.get('sub_zone_name') != 'None':
            where_condition += " and p.subzone=\'"+queryDict.get('sub_zone_name')+"\'"
        if (queryDict.get('wave_exp') is not None):
            if (queryDict.get('wave_exp') == 'None'): 
                where_condition += " and p.wave_exp is Null"
            else:
                where_condition += " and p.wave_exp=\'"+queryDict.get('wave_exp')+"\'"
        query = '''select t.date_time,t.temperature 
                from cnx_logger_type lt
                inner join cnx_logger l 
                on l.biomimic_id=lt.bioid
                inner join cnx_logger_geographics lg 
                on l.geo_id=lg.gid
                inner join cnx_logger_properties p 
                on p.lpropId = l.prop_id
                inner join cnx_logger_temp t on t.logger_id = l.lid''' + where_condition

        cursor.execute(query)
        results = cursor.fetchall()
        results = list(results)
        final_result = [[result[0].strftime("%m/%d/%Y %H:%M"), result[1]] for result in results]
        cursor.close()
        return final_result

    def getQueryRawResults(self, queryDict):
        """Fetches records form tables based on user query"""
        cursor = self.connection.cursor()
        where_condition = " where lt.type=\'"+queryDict.get('logger_type')+\
                          "\' and lg.country=\'"+queryDict.get('country_name')+"\'"# and t.date_time BETWEEN \'"+queryDict.get('start_date')+"\' AND \'"+queryDict.get('end_date')+"\'"
        if queryDict.get('state_name') != 'None':
            where_condition += " and lg.state=\'"+queryDict.get('state_name')+"\'"
        if queryDict.get('location_name') != 'None':
            where_condition += " and lg.location=\'"+queryDict.get('location_name')+"\'"
        if queryDict.get('zone_name') != 'None':
            where_condition += " and p.zone=\'"+queryDict.get('zone_name')+"\'"
        if queryDict.get('sub_zone_name') != 'None':
            where_condition += " and p.subzone=\'"+queryDict.get('sub_zone_name')+"\'"
        if (queryDict.get('wave_exp') is not None):
            if (queryDict.get('wave_exp') == 'None'): 
                where_condition += " and p.wave_exp is Null"
            else:
                where_condition += " and p.wave_exp=\'"+queryDict.get('wave_exp')+"\'"
        query = '''select t.date_time,t.temperature 
                from cnx_logger_type lt
                inner join cnx_logger l 
                on l.biomimic_id=lt.bioid
                inner join cnx_logger_geographics lg 
                on l.geo_id=lg.gid
                inner join cnx_logger_properties p 
                on p.lpropId = l.prop_id
                inner join cnx_logger_temp t on t.logger_id = l.lid''' + where_condition

        cursor.execute(query)
        results = cursor.fetchall()
        results = list(results)
        header = [("logger_type:"+queryDict.get('logger_type')[0],"country_name:"+queryDict.get('country_name')[0],"state_name:"+queryDict.get('state_name')[0],"location_name:"+queryDict.get('location_name')[0],"zone_name:"+queryDict.get('zone_name')[0],"sub_zone_name:"+queryDict.get('sub_zone_name')[0],"wave_exp:"+queryDict.get('wave_exp')[0]),("Timestamp","Temperature")]
        final_result = header + [[result[0].strftime("%m/%d/%Y %H:%M"), result[1]] for result in results]
        cursor.close()
        return final_result



    def close(self):
        self.connection.close()




