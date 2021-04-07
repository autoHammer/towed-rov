import queue
from threading import Thread
from sensor import Sensor
from time import sleep


class SerialMessageRecivedHandler(Thread):
    def __init__(self, gui_command_queue, sensor_list, valid_sensor_list, message_queue):
        Thread.__init__(self)
        self.message_received_queue = gui_command_queue
        self.sensor_list = sensor_list
        self.valid_sensor_list = valid_sensor_list
        self.valid_commands = ['reset', 'IMU', 'SensorArduino', 'StepperArduino',
                               'depth_beneath_rov_offset', 'depth_rov_offset', 'pid_depth_p',
                               'pid_depth_i', 'pid_depth_d', 'pid_roll_p', 'pid_roll_i', 'pid_roll_d',
                               'auto_mode', 'manual_wing_pos', 'set_point_depth',
                               'emergency_surface'
                               ]
        self.message_queue = message_queue
        self.count = 0

    def run(self):
        while True:
            try:
                print(self.count)
                self.count = self.count + 1
                # received_message = self.message_queue.get_nowait()
                # print(received_message)
    #             message = received_message.split(':',1)
    #             if message[0] in  self.valid_commands:
    # #                 print("----------------------")
    #                 self.message_received_queue.put(received_message)
    #             else:
    #                 self.__add_sensor(message)
            except queue.Empty:
                pass
            except ValueError:
                pass
    #             print(received_message, "error: ", e)

    def __add_sensor(self, message):
        """
        checks of message is an expected on, and if, it adds the message/sensor to the list of sensors.
        If the sensor is already in the list it updates it's value.
        :param message:
        
        """
        if ('IMU' or 'sensorArduino' or 'stepperArduino') in message[0]:
            pass
        else:
            name = message[0]
            value = message[1]
            # if name == 'depth':
            #     print(message)
            if name in self.valid_sensor_list:
                if name in self.sensor_list.keys():
                    self.sensor_list[name] = float(value)
                else:
                    sensor = Sensor(name, float(value))
                    # print('------')
                    # print(sensor)
                    # print('------')
                    self.sensor_list[name] = float(value)
if __name__ == '__main__':
    q1 = queue.Queue()
    q2 = queue.Queue()
    q2.put("sdtig:2")
    test = SerialMessageRecivedHandler(q1, [], {}, q2)
    test.start()
    while True:
        pass