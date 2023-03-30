
from dynamixel.servo import Servo
from dynamixel.servo import Row, RWRow, IndirectRow
from dynamixel.channel import Protocol1

class AX_12A(Servo):
    EEPROM = {
        'model_number': Row(name='model_number', address=0, size=2, default=12),
        'firmware_version': Row(name='firmware_version', address=2, size=1, default=None),
        'id': RWRow(name='id', address=3, size=1, default=1),
        'baud_rate': RWRow(name='baud_rate', address=4, size=1, default=1),
        'return_delay_time': RWRow(name='return_delay_time', address=5, size=1, default=250),
        'cw_angle_limit': RWRow(name='cw_angle_limit', address=6, size=2, default=0),
        'ccw_angle_limit': RWRow(name='ccw_angle_limit', address=8, size=2, default=1023),
        'temperature_limit': RWRow(name='temperature_limit', address=11, size=1, default=70),
        'min_voltage_limit': RWRow(name='min_voltage_limit', address=12, size=1, default=60),
        'max_voltage_limit': RWRow(name='max_voltage_limit', address=13, size=1, default=140),
        'max_torque': RWRow(name='max_torque', address=14, size=2, default=1023),
        'status_return_level': RWRow(name='status_return_level', address=16, size=1, default=2),
        'alarm_led': RWRow(name='alarm_led', address=17, size=1, default=36),
        'shutdown': RWRow(name='shutdown', address=18, size=1, default=36)
    }
    RAM = {
        'torque_enable': RWRow(name='torque_enable', address=24, size=1, default=0),
        'led': RWRow(name='led', address=25, size=1, default=0),
        'cw_compliance_margin': RWRow(name='cw_compliance_margin', address=26, size=1, default=1),
        'ccw_compliance_margin': RWRow(name='ccw_compliance_margin', address=27, size=1, default=1),
        'cw_compliance_slope': RWRow(name='cw_compliance_slope', address=28, size=1, default=32),
        'ccw_compliance_slope': RWRow(name='ccw_compliance_slope', address=29, size=1, default=32),
        'goal_position': RWRow(name='goal_position', address=30, size=2, default=None),
        'moving_speed': RWRow(name='moving_speed', address=32, size=2, default=None),
        'torque_limit': RWRow(name='torque_limit', address=34, size=2, default=None),
        'present_position': Row(name='present_position', address=36, size=2, default=None),
        'present_speed': Row(name='present_speed', address=38, size=2, default=None),
        'present_load': Row(name='present_load', address=40, size=2, default=None),
        'present_voltage': Row(name='present_voltage', address=42, size=1, default=None),
        'present_temperature': Row(name='present_temperature', address=43, size=1, default=None),
        'registered': Row(name='registered', address=44, size=1, default=0),
        'moving': Row(name='moving', address=46, size=1, default=0),
        'lock': RWRow(name='lock', address=47, size=1, default=0),
        'punch': RWRow(name='punch', address=48, size=2, default=32)
    }
    PROTOCOL = Protocol1

    def __init__(self, channel, id):
        super(AX_12A, self).__init__(channel=channel, id=id)
