
from dynamixel.servo import Servo
from dynamixel.servo import Row, RWRow, IndirectRow
from dynamixel.channel import Protocol2

class XM430_W210_T_R(Servo):
    EEPROM = {
        'model_number': Row(name='model_number', address=0, size=2, default=1030),
        'model_information': Row(name='model_information', address=2, size=4, default=None),
        'firmware_version': Row(name='firmware_version', address=6, size=1, default=None),
        'id': RWRow(name='id', address=7, size=1, default=1),
        'baud_rate': RWRow(name='baud_rate', address=8, size=1, default=1),
        'return_delay_time': RWRow(name='return_delay_time', address=9, size=1, default=250),
        'drive_mode': RWRow(name='drive_mode', address=10, size=1, default=0),
        'operating_mode': RWRow(name='operating_mode', address=11, size=1, default=3),
        'secondary_id': RWRow(name='secondary_id', address=12, size=1, default=255),
        'protocol_type': RWRow(name='protocol_type', address=13, size=1, default=2),
        'homing_offset': RWRow(name='homing_offset', address=20, size=4, default=0),
        'moving_threshold': RWRow(name='moving_threshold', address=24, size=4, default=10),
        'temperature_limit': RWRow(name='temperature_limit', address=31, size=1, default=80),
        'max_voltage_limit': RWRow(name='max_voltage_limit', address=32, size=2, default=160),
        'min_voltage_limit': RWRow(name='min_voltage_limit', address=34, size=2, default=95),
        'pwm_limit': RWRow(name='pwm_limit', address=36, size=2, default=885),
        'current_limit': RWRow(name='current_limit', address=38, size=2, default=1193),
        'velocity_limit': RWRow(name='velocity_limit', address=44, size=4, default=330),
        'max_position_limit': RWRow(name='max_position_limit', address=48, size=4, default=4095),
        'min_position_limit': RWRow(name='min_position_limit', address=52, size=4, default=0),
        'shutdown': RWRow(name='shutdown', address=63, size=1, default=52)
    }
    RAM = {
        'torque_enable': RWRow(name='torque_enable', address=64, size=1, default=0),
        'led': RWRow(name='led', address=65, size=1, default=0),
        'status_return_level': RWRow(name='status_return_level', address=68, size=1, default=2),
        'registered_instruction': Row(name='registered_instruction', address=69, size=1, default=0),
        'hardware_error_status': Row(name='hardware_error_status', address=70, size=1, default=0),
        'velocity_i_gain': RWRow(name='velocity_i_gain', address=76, size=2, default=1920),
        'velocity_p_gain': RWRow(name='velocity_p_gain', address=78, size=2, default=100),
        'position_d_gain': RWRow(name='position_d_gain', address=80, size=2, default=0),
        'position_i_gain': RWRow(name='position_i_gain', address=82, size=2, default=0),
        'position_p_gain': RWRow(name='position_p_gain', address=84, size=2, default=800),
        'feedforward_2nd_gain': RWRow(name='feedforward_2nd_gain', address=88, size=2, default=0),
        'feedforward_1st_gain': RWRow(name='feedforward_1st_gain', address=90, size=2, default=0),
        'bus_watchdog': RWRow(name='bus_watchdog', address=98, size=1, default=0),
        'goal_pwm': RWRow(name='goal_pwm', address=100, size=2, default=None),
        'goal_current': RWRow(name='goal_current', address=102, size=2, default=None),
        'goal_velocity': RWRow(name='goal_velocity', address=104, size=4, default=None),
        'profile_acceleration': RWRow(name='profile_acceleration', address=108, size=4, default=0),
        'profile_velocity': RWRow(name='profile_velocity', address=112, size=4, default=0),
        'goal_position': RWRow(name='goal_position', address=116, size=4, default=None),
        'realtime_tick': Row(name='realtime_tick', address=120, size=2, default=None),
        'moving': Row(name='moving', address=122, size=1, default=0),
        'moving_status': Row(name='moving_status', address=123, size=1, default=0),
        'present_pwm': Row(name='present_pwm', address=124, size=2, default=None),
        'present_current': Row(name='present_current', address=126, size=2, default=None),
        'present_velocity': Row(name='present_velocity', address=128, size=4, default=None),
        'present_position': Row(name='present_position', address=132, size=4, default=None),
        'velocity_trajectory': Row(name='velocity_trajectory', address=136, size=4, default=None),
        'position_trajectory': Row(name='position_trajectory', address=140, size=4, default=None),
        'present_input_voltage': Row(name='present_input_voltage', address=144, size=2, default=None),
        'present_temperature': Row(name='present_temperature', address=146, size=1, default=None),
        'indirect_address': IndirectRow(name='indirect_address', addresses=[range(168, 224, 2), range(578, 634, 2)], size=2),
        'indirect_data': IndirectRow(name='indirect_data', addresses=[range(224, 252), range(634, 662)], size=1)
    }
    PROTOCOL = Protocol2

    def __init__(self, channel, id):
        super(XM430_W210_T_R, self).__init__(channel=channel, id=id)
