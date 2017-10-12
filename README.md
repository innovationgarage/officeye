# officeye

### to setup the sqlite database and tables
python init_db.py

### to start monitoring
python main.py [model name] [input]
- _model name_ options implemented in JeVois: yolo9000 [default], tiny-yolo, tiny-yolo-voc
- _input_ options are test (pretending the content of serial.test file is the output of the camera) or 0 for using /dev/ttyACM0 as the serial port and /dev/video0 as the camera input. **However**, if you get a 'No video device found' by using 0, it is because unstable USB connection could lead to your machine connecting to a "new" Jevois via /dev/ttyACM1 and /dev/video1 instead. Use 1 instead!
