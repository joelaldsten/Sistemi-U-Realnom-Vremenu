
from dynamixel.servo import Servo
from dynamixel.servo import Row, RWRow, IndirectRow
from dynamixel.channel import Protocol2

class PH42_020_S300_R(Servo):
    EEPROM = {
        'model_number': Row(name='model_number', address=0, size=2, default=2000),
        'model_information': Row(name='model_information', address=2, size=4, default=None),
        'firmware_version': Row(name='firmware_version', address=6, size=1, default=None),
        'id': RWRow(name='id', address=7, size=1, default=1),
        'baud_rate': RWRow(name='baud_rate', address=8, size=1, default=1),
        'return_delay_time': RWRow(name='return_delay_time', address=9, size=1, default=250),
        'drive_mode': RWRow(name='drive_mode', address=10, size=1, default=0),
        'operating_mode': RWRow(name='operating_mode', address=11, size=1, default=3),
        'sencondary_id': RWRow(name='sencondary_id', address=12, size=1, default=255),
        'protocol_type': RWRow(name='protocol_type', address=13, size=1, default=2),
        'homing_offset': RWRow(name='homing_offset', address=20, size=4, default=0),
        'moving_threshold': RWRow(name='moving_threshold', address=24, size=4, default=20),
        'temperature_limit': RWRow(name='temperature_limit', address=31, size=1, default=80),
        'max_voltage_limit': RWRow(name='max_voltage_limit', address=32, size=2, default=350),
        'min_voltage_limit': RWRow(name='min_voltage_limit', address=34, size=2, default=150),
        'pwm_limit': RWRow(name='pwm_limit', address=36, size=2, default=2009),
        'current_limit': RWRow(name='current_limit', address=38, size=2, default=4500),
        'acceleration_limit': RWRow(name='acceleration_limit', address=40, size=4, default=10765),
        'velocity_limit': RWRow(name='velocity_limit', address=44, size=4, default=2920),
        'max_position_limit': RWRow(name='max_position_limit', address=48, size=4, default=303454),
        'min_position_limit': RWRow(name='min_position_limit', address=52, size=4, default=-303454),
        'external_port_mode': IndirectRow(name='external_port_mode', addresses=[range(56, 60)], size=1),
        'shutdown': RWRow(name='shutdown', address=63, size=1, default=58),
        'indirect_address': IndirectRow(name='indirect_address', addresses=[range(168, 424, 2)], size=2)
    }
    RAM = {
        'torque_enable': RWRow(name='torque_enable', address=512, size=1, default=0),
        'led_red': RWRow(name='led_red', address=513, size=1, default=0),
        'led_green': RWRow(name='led_green', address=514, size=1, default=0),
        'led_blue': RWRow(name='led_blue', address=515, size=1, default=0),
        'status_return_level': RWRow(name='status_return_level', address=516, size=1, default=2),
        'registered_instruction': Row(name='registered_instruction', address=517, size=1, default=0),
        'hardware_error_status': Row(name='hardware_error_status', address=518, size=1, default=0),
        'velocity_i_gain': RWRow(name='velocity_i_gain', address=524, size=2, default=None),
        'velocity_p_gain': RWRow(name='velocity_p_gain', address=526, size=2, default=None),
        'position_d_gain': RWRow(name='position_d_gain', address=528, size=2, default=None),
        'position_i_gain': RWRow(name='position_i_gain', address=530, size=2, default=None),
        'position_p_gain': RWRow(name='position_p_gain', address=532, size=2, default=None),
        'feedforward_2nd_gain': RWRow(name='feedforward_2nd_gain', address=536, size=2, default=None),
        'feedforward_1st_gain': RWRow(name='feedforward_1st_gain', address=538, size=2, default=None),
        'bus_watchdog': RWRow(name='bus_watchdog', address=546, size=1, default=None),
        'goal_pwm': RWRow(name='goal_pwm', address=548, size=2, default=None),
        'goal_current': RWRow(name='goal_current', address=550, size=2, default=None),
        'goal_velocity': RWRow(name='goal_velocity', address=552, size=4, default=None),
        'profile_acceleration': RWRow(name='profile_acceleration', address=556, size=4, default=None),
        'profile_velocity': RWRow(name='profile_velocity', address=560, size=4, default=None),
        'goal_position': RWRow(name='goal_position', address=564, size=4, default=None),
        'realtime_tick': Row(name='realtime_tick', address=568, size=2, default=None),
        'moving': Row(name='moving', address=570, size=1, default=None),
        'moving_status': Row(name='moving_status', address=571, size=1, default=None),
        'present_pwm': Row(name='present_pwm', address=572, size=2, default=None),
        'present_current': Row(name='present_current', address=574, size=2, default=None),
        'present_velocity': Row(name='present_velocity', address=576, size=4, default=None),
        'present_position': Row(name='present_position', address=580, size=4, default=None),
        'velocity_trajectory': Row(name='velocity_trajectory', address=584, size=4, default=None),
        'position_trajectory': Row(name='position_trajectory', address=588, size=4, default=None),
        'present_input_voltage': Row(name='present_input_voltage', address=592, size=2, default=None),
        'present_temperature': Row(name='present_temperature', address=594, size=1, default=None),
        'external_port_data': IndirectRow(name='external_port_data', addresses=[range(600, 608, 2)], size=2),
        'indirect_data': IndirectRow(name='indirect_data', addresses=[range(634, 762)], size=1)
    }
    PROTOCOL = Protocol2

    def __init__(self, channel, id):
        super(PH42_020_S300_R, self).__init__(channel=channel, id=id)
