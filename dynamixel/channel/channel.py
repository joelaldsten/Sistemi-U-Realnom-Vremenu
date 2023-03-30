#!/usr/bin/python3

import dynamixel_sdk as sdk
import serial.tools
import serial.tools.list_ports

class Channel:

    def __init__(self, speed, serial_number=None, device=None):
        if serial_number != None and device != None:
            raise Exception('Either serial_number or port should be specified')

        # Hackish way to check baud-rate
        if sdk.PortHandler.getCFlagBaud(None, speed) < 0:
            raise Exception('Baud rate error "%d"' % speed)

        # Scan available USB devices
        devices = {}
        for v,p,s,d in [ (p.vid, p.pid, p.serial_number, p.device)
                         for p
                         in serial.tools.list_ports.comports() ]:
            devices[s] = d
            pass
        if serial_number and serial_number in devices:
            port = devices[serial_number]
            pass
        elif device and device in devices.values():
            port = device
            pass
        elif len(devices) == 1:
            port = list(devices.values())[0]
            print("Warning, defaulting to: ", devices)
        else:
            raise Exception(f'Select one of: {devices}')

        self.port_handler = sdk.PortHandler(port)
        if not self.port_handler.openPort():
            raise Exception("self.port_handler.openPort()")
        if not self.port_handler.setBaudRate(speed):
            raise Exception(f"self.port_handler.setBaudRate({speed})")
        try:
            self.port_handler.ser.set_low_latency_mode(True)
        except:
            raise Exception("self.port_handler.ser-set_low_latency_mode(True)")

        # Check id (i.e. FT2H2W9I)...

        self._protocol = {}
        pass

    def protocol(self, protocol):
        if  protocol in self._protocol:
            return self._protocol[protocol]
        else:
            self._protocol[protocol] = protocol(self.port_handler)
            return self._protocol[protocol]
        
    def add(self, device):
        print('Add', device)
        pass
    
    
    pass


class Protocol:

    def __init__(self, port_handler, packet_handler):
        self.port_handler = port_handler
        self.packet_handler = packet_handler
        pass

    def read(self, servo, row):
        if row.size == 1:
            value, comm_result, error = self.packet_handler.read1ByteTxRx(
                self.port_handler, servo._id, row.address)
            pass
        elif row.size == 2:
            value, comm_result, error = self.packet_handler.read2ByteTxRx(
                self.port_handler, servo._id, row.address)
            pass
        elif row.size == 4:
            value, comm_result, error = self.packet_handler.read4ByteTxRx(
                self.port_handler, servo._id, row.address)
            pass
        else:
            raise Exception('Invalid size', row)
        if comm_result != 0:
            raise Exception("Comunication error", comm_result)
        if error != 0:
            raise Exception("Servo error", error)
        return value
        
    def write(self, servo, row, value):
        if row.size == 1:
            comm_result, error = self.packet_handler.write1ByteTxRx(
                self.port_handler, servo._id, row.address, value)
            pass
        elif row.size == 2:
            comm_result, error = self.packet_handler.write2ByteTxRx(
                self.port_handler, servo._id, row.address, value)
            pass
        elif row.size == 4:
            comm_result, error = self.packet_handler.write4ByteTxRx(
                self.port_handler, servo._id, row.address, value)
            pass
        else:
            raise Exception('Invalid size', row)
        if comm_result != 0:
            raise Exception("Comunication error", comm_result)
        if error != 0:
            raise Exception("Servo error", error)
        pass
        
    pass


class Protocol1(Protocol):

    def __init__(self, port_handler):
        super(Protocol1, self).__init__(port_handler, sdk.PacketHandler(1.0))
        pass

    pass

class Protocol2(Protocol):

    def __init__(self, port_handler):
        super(Protocol2, self).__init__(port_handler, sdk.PacketHandler(2.0))
        pass

    pass
