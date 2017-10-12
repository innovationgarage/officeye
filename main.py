import serial
import os
import time
import sys
from subprocess import Popen
import Object as _
import db_tools as db
import tracker_function as tracker

model = str(sys.argv[1])
mode = str(sys.argv[2])
database = 'db/pyolo.db'    

if mode=='test':
    with open('serial.test') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].split()
            if line[0]=='D2':
                found_object = _.Object(line)
                with db.create_connection(database) as conn:
                    obj_id = found_object.isIn(database, conn)
                    if not len(obj_id):
                        print 'new %s found!'%found_object._type
                        obj_id = found_object.create_object(conn)
                        found_object.create_event(conn, obj_id, model)                    
                        found_object.update_object(conn, obj_id)
                    else:
                        for oid in obj_id:
                            print 'known %s with obj_id: %s seen again'%(found_object._type, oid)
                            found_object.create_event(conn, oid, model)
                            found_object.update_object(conn, oid)                        
else:
    with serial.Serial('/dev/ttyACM%d'%int(sys.argv[2]), timeout=1) as ser:
        ser.write('setpar cfgfile cfg/%s.cfg\n'%model)
        ser.write('setpar weightfile weights/%s.weights\n'%model)
        process = Popen(['guvcview', '--device=/dev/video%d'%int(sys.argv[2]), '-ao', 'none', '-f', 'YUYV', '-x', '1280x480'])
#        process = Popen(['cvlc', '-vvv', 'v4l2:///dev/video%d'%int(sys.argv[2])])
        time.sleep(20)
        ser.write('setpar serout USB\n')
        ser.write('setpar serstyle Detail\n')
        ser.write('setpar thresh 35\n')
        ser.write('setpar nms 10\n')
        ser.write('help\n')
        while ser.isOpen():
            line = ser.readline().split()
            if line:
                if line[0]=='D2':
                    found_object = _.Object(line)
                    with db.create_connection(database) as conn:
                        obj_id = found_object.isIn(database, conn)
                        if not len(obj_id):
                            print 'new %s found!'%found_object._type
                            obj_id = found_object.create_object(conn)
                            found_object.create_event(conn, obj_id, model)                    
                            found_object.update_object(conn, obj_id)
                        else:
                            for oid in obj_id:
                                print 'known %s with obj_id: %s seen again'%(found_object._type, oid)
                                found_object.create_event(conn, oid, model)
                                found_object.update_object(conn, oid)                        

                        
