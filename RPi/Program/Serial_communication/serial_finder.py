import glob
import serial
import sys
import time

# note: Teensy will work on most or all frequencies


def find_serial_ports():
    """
    Finds serial devices connected with USB
    Checks on different frequencies (9600, 57600 and 115200)
    Expects serial device to send the device name.
    ex: arduino is sending 'SensorArduino' to serial in loop

    :return: dict with port name (key), and device name (Value)
    ex: {'/dev/ttyACM0' : 'SensorArduino'}
    """

    # list of connected usb devices
    port_names = get_available_com_ports()
    print('Available Ports: ', port_names)

    port_name_list = {}
    for search_runs in range(1): # write 3 if you want to search multible baudrates
        if search_runs == 0:
            baud_rate = 115200
        if search_runs == 1:
            baud_rate = 57600
        if search_runs == 2:
            baud_rate = 9600

        for key in port_names:
            serial_port = serial.Serial(key, baud_rate, timeout=1, write_timeout=2,
                                        stopbits=1, bytesize=8)

            print(f'\nChecking {serial_port.name} at {baud_rate} Baud:')

            try:
                # send request for the name of the device
                serial_port.write("<request_name:0>".encode('utf-8'))

                # wait for response from serial device
                # max waiting time is set to 2s
                timer = time.time()  # current time
                while time.time() - timer < 2:
                    # read response if available
                    if serial_port.in_waiting > 0:
                        message_received = serial_port.readline()
                        message_received = message_received.strip().decode('utf-8').split(":")  # convert to readable data

                        if "device_name" in message_received[0]:
                            device_name = message_received[1].replace('>', '')
                            print(f" found device : {device_name}")

                            port_name_list[key] = device_name  # add port and name to return dict

                            serial_port.reset_input_buffer()
                            serial_port.close()

                            break
                        
            except serial.SerialTimeoutException as timeout:
                print(f"{timeout}: device did not respond")
                
            except Exception as e:

                print(e, '- in serial_finder')

                try:
                    serial_port.close()
                except Exception as e:
                    print(e, '- in serial_finder')
        search_runs = search_runs + 1
    print('Device finder complete\n')
    return port_name_list


def get_available_com_ports():
    """
    find all available com port on Windows or linux systems
    :return: list with all com ports
    """

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


"""
Unit test
Run this to find devices connected to RPi USB 
"""
if __name__ == "__main__":
    dict = find_serial_ports()
    print("find_serial_ports() returns:")
    print(dict)
