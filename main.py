import serial
import os
import time
import sys
from subprocess import Popen
import Object as _
import db_tools as db

if __name__ == "__main__":
    model = str(sys.argv[1])
else:
    model = 'yolo9000'

database = 'db/pyolo.db'    

''' Uncomment this block to use the USB serial to interact with the JeVois camera'''
# with serial.Serial('/dev/ttyACM0', timeout=1) as ser:
#     ser.write('setpar cfgfile cfg/%s.cfg\n'%model)
#     ser.write('setpar weightfile weights/%s.weights\n'%model)
#     process = Popen(['guvcview', '-ao', 'none', '-f', 'YUYV', '-x', '1280x480'])
#     time.sleep(20)
#     ser.write('setpar serout USB\n')
#     ser.write('setpar serstyle Detail\n')
#     ser.write('setpar thresh 35\n')
#     ser.write('setpar nms 10\n')
#     ser.write('help\n')
#     while ser.isOpen():
#         line = ser.readline().split()
#         if line:
#             if line[0]=='D2':
#                 found_object = _.Object(line)
#                 with db.create_connection(database) as conn:
#                     obj_id = found_object.isIn(database, conn)
#                     if not len(obj_id):
#                         print 'new %s found!'%found_object._type
#                         obj_id = found_object.create_object(conn)
#                         found_object.create_event(conn, obj_id, model)                    
#                         found_object.update_object(conn, obj_id)
#                     else:
#                         for oid in obj_id:
#                             print 'known %s with obj_id: %s seen again'%(found_object._type, oid)
#                             found_object.create_event(conn, oid, model)
#                             found_object.update_object(conn, oid)                        


#test
''' Comment out if using the actual camera output '''
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
                        
