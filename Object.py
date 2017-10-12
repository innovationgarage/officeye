from datetime import datetime
import time
from math import *
import numpy as np
import math_tools as mtools

class Object(object):
    def __init__(self, line):
        self._type = line[1]
        self.w_in = float(line[2])
        self.h_in = float(line[3])
        self.x_left = float(line[4])
        self.y_left = float(line[5])
        self.x_top = float(line[6])
        self.y_top = float(line[7])
        self.w_b = float(line[8])
        self.h_b = float(line[9])
        self.prob = float(line[10])
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.properties = {
            '_type': self._type,
            'w_in': self.w_in,
            'h_in': self.h_in,
            'x_left': self.x_left,
            'y_left': self.y_left,
            'x_top': self.x_top,
            'y_top': self.y_top,
            'w_b': self.w_b,
            'h_b': self.h_b,
            'prob': self.prob
        }
                            
    def getProperties(self):
        props = {
            'w_in': self.w_in,
            'h_in': self.h_in,
            'x_left': self.x_left,
            'y_left': self.y_left,
            'x_top': self.x_top,
            'y_top': self.y_top,
            'w_b': self.w_b,
            'h_b': self.h_b,
            'prob': self.prob,
            'timestamp': self.timestamp
        }
        return props
    
    def create_object(self, conn):
        sql = ''' INSERT INTO objects(obj_type,last_event,last_x_left,last_y_left,speed)
        VALUES(:_type,:timestamp,:last_x_left,:last_y_left,:speed) '''
        cur = conn.cursor()
        cur.execute(sql, {'_type': self._type, 'timestamp': self.timestamp, 'last_x_left': self.x_left, 'last_y_left': self.y_left, 'speed': 0.0})
        return cur.lastrowid

    def calculate_speed(self, conn, object_id):
        cur = conn.cursor()
        sql_select = '''SELECT objects.last_event, objects.speed, objects.last_x_left, objects.last_y_left 
        FROM objects 
        WHERE objects.id=? '''
        cur.execute(sql_select, (object_id,))
        fetch = cur.fetchall()
        if len(fetch):
            res = fetch[0]
        else:
            res = [self.timestamp, self.x_left, self.y_left]
        last_sight = datetime.strptime(res[0], "%Y-%m-%d %H:%M:%S")
        last_speed = float(res[1])
        dt = (datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S") - last_sight).total_seconds()
#        dt = 1. #test
        d = sqrt((self.x_left-float(res[2]))**2+(self.y_left-float(res[3]))**2)
        if dt == 0:
            speed = 0.0
        else:
            speed = d/dt
        return last_speed, speed
    
    def create_event(self, conn, obj_id, model):
        sql = ''' INSERT INTO events(obj_id,model,w_in,h_in,x_left,y_left,x_top,y_top,w_b,h_b,prob,timestamp)
        VALUES(:obj_id,:model,:w_in,:h_in,:x_left,:y_left,:x_top,:y_top,:w_b,:h_b,:prob,:timestamp) '''
        cur = conn.cursor()
        event = self.getProperties()
        event['obj_id'] = obj_id
        event['model'] = model
        cur.execute(sql, event)
        return cur.lastrowid

    def update_object(self, conn, object_id):
        last_speed, speed = self.calculate_speed(conn, object_id)        
        sql = ''' UPDATE objects
        SET 
        last_event = ?,
        last_x_left = ?,
        last_y_left = ?,
        speed = ?
        WHERE id=?; 
        '''
        cur = conn.cursor()
        cur.execute(sql, (self.timestamp, self.x_left, self.y_left, speed, object_id))

    def update_speed(self, conn, object_id):
        last_speed, speed = self.calculate_speed(conn, object_id)
        sql_update = ''' UPDATE objects
        SET 
        speed = ?
        WHERE objects.id=?; 
        '''
        cur = conn.cursor()
        cur.execute(sql_update, (speed, object_id))

    def isIn(self, database, conn):
        sql = ''' SELECT DISTINCT objects.id
        FROM objects
        JOIN events ON obj_id
        WHERE 
        objects.obj_type=?
        '''
        cur = conn.cursor()
        cur.execute(sql, (self._type,))
        objects = cur.fetchall()
        if len(objects):
#            obj = (self.x_left, self.y_left, self.w_in, self.h_in, self.x_top, self.y_top, self.w_b, self.h_b)
            obj = (self.x_left, self.y_left, self.w_b, self.h_b)
            candidate_ids = objects[0]
            object_ids = []
            for oid in candidate_ids:
                last_speed, current_speed = self.calculate_speed(conn, oid)
#                candid_sql = ''' select x_left, y_left, w_in, h_in, x_top, y_top, w_b, h_b from events where obj_id=? ORDER BY events.timestamp DESC LIMIT 1 '''
                candid_sql = ''' select x_left, y_left, w_b, h_b from events where obj_id=? ORDER BY events.timestamp DESC LIMIT 1 '''
                candid_cur = conn.cursor()
                candid_cur.execute(candid_sql, (oid,))
                candid = candid_cur.fetchall()[0]
                print oid
                print obj
                print candid
                print '------'
                print self.prob, mtools.bb_intersection_over_union(candid, obj)
                if mtools.bb_intersection_over_union(candid, obj)<self.prob:
                    object_ids.append(oid)
        else:
            object_ids = []            
        return object_ids
