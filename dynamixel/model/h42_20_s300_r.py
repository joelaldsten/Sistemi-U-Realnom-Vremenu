
from dynamixel.servo import Servo
from dynamixel.servo import Row, RWRow, IndirectRow
from dynamixel.channel import Protocol2

class H42_20_S300_R(Servo):
    EEPROM = {
        'model_number': Row(name='model_number', address=0, size=2, default=51200),
        'model_information': Row(name='model_information', address=2, size=4, default=None),
        'firmware_version': Row(name='firmware_version', address=6, size=1, default=None),
        'id': RWRow(name='id', address=7, size=1, default=1),
        'baud_rate': RWRow(name='baud_rate', address=8, size=1, default=1),
        'return_delay_time': RWRow(name='return_delay_time', address=9, size=1, default=250),
        'operating_mode': RWRow(name='operating_mode', address=11, size=1, default=3),
        'homing_offset': RWRow(name='homing_offset', address=13, size=4, default=0),
        'moving_threshold': RWRow(name='moving_threshold', address=17, size=4, default=50),
        'temperature_limit': RWRow(name='temperature_limit', address=21, size=1, default=80),
        'max_voltage_limit': RWRow(name='max_voltage_limit', address=22, size=2, default=400),
        'min_voltage_limit': RWRow(name='min_voltage_limit', address=24, size=2, default=150),
        'acceleration_limit': RWRow(name='acceleration_limit', address=26, size=4, default=255),
        'torque_limit': RWRow(name='torque_limit', address=30, size=2, default=465),
        'velocity_limit': RWRow(name='velocity_limit', address=32, size=4, default=10300),
        'max_position_limit': RWRow(name='max_position_limit', address=36, size=4, default=151875),
        'min_position_limit': RWRow(name='min_position_limit', address=40, size=4, default=-151875),
        'external_port_mode': IndirectRow(name='external_port_mode', addresses=[range(44, 48)], size=1),
        'shutdown': RWRow(name='shutdown', address=48, size=1, default=58),
        'indirect_address': IndirectRow(name='indirect_address', addresses=[range(49, 561, 2)], size=2)
    }
    RAM = {
        'torque_enable': RWRow(name='torque_enable', address=562, size=1, default=0),
        'led_red': RWRow(name='led_red', address=563, size=1, default=0),
        'led_green': RWRow(name='led_green', address=564, size=1, default=0),
        'led_blue': RWRow(name='led_blue', address=565, size=1, default=0),
        'velocity_i_gain': RWRow(name='velocity_i_gain', address=586, size=2, default=40),
        'velocity_p_gain': RWRow(name='velocity_p_gain', address=588, size=2, default=440),
        'position_p_gain': RWRow(name='position_p_gain', address=594, size=2, default=32),
        'goal_position': RWRow(name='goal_position', address=596, size=4, default=None),
        'goal_velocity': RWRow(name='goal_velocity', address=600, size=4, default=0),
        'goal_torque': RWRow(name='goal_torque', address=604, size=2, default=0),
        'goal_acceleration': RWRow(name='goal_acceleration', address=606, size=4, default=0),
        'moving': Row(name='moving', address=610, size=1, default=None),
        'present_position': Row(name='present_position', address=611, size=4, default=None),
        'present_velocity': Row(name='present_velocity', address=615, size=4, default=None),
        'present_current': Row(name='present_current', address=621, size=2, default=None),
        'present_input_voltage': Row(name='present_input_voltage', address=623, size=2, default=None),
        'present_temperature': Row(name='present_temperature', address=625, size=1, default=None),
        'external_port_data': IndirectRow(name='external_port_data', addresses=[range(626, 634, 2)], size=2),
        'indirect_data': IndirectRow(name='indirect_data', addresses=[range(634, 890)], size=1),
        'registered_instruction': Row(name='registered_instruction', address=890, size=1, default=0),
        'status_return_level': RWRow(name='status_return_level', address=891, size=1, default=2),
        'hardware_error_status': Row(name='hardware_error_status', address=892, size=1, default=0)
    }
    PROTOCOL = Protocol2

    def __init__(self, channel, id):
        super(H42_20_S300_R, self).__init__(channel=channel, id=id)
