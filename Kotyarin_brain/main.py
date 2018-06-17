#import serial
import i2cdev

import revolution
import ads1115
import tsl2561

# UAV talk
PORT_REVOLUTION = "/dev/ttyS1"

# UART
PORT_UART = "/dev/ttyS2"

# I2C
PORT_I2C = 0
I2C_TIMEOUT = 2

# Revolution
REV_LOG_UPDATE_RATE = 50

REV_SERVO_MIN = 700
REV_SERVO_MAX = 2500
REV_SERVO_DEG = 180
REV_SERVO_CHANNEL = 0
REV_SERVO_ROT_1 = 500
REV_SERVO_ROT_2 = 1000
REV_SERVO_ROT_3 = 1500


if __name__ == '__main__':
    # ================================================================
    # Init block
    # ================================================================
    # UAV talk
    uav_talk = revolution.Uavtalk()
    uav_talk.setup(PORT_REVOLUTION)

    # Uart
    # -------------------------------------------------------------<==
    # TODO: init uart for GSM
    # -------------------------------------------------------------<==

    # I2C
    i2c_line = i2cdev.I2C(PORT_I2C)
    i2c_line.set_timeout(I2C_TIMEOUT)

    # Revolution - log
    revolution_log = revolution.All_telemetry_logger(uav_talk,
                                                     REV_LOG_UPDATE_RATE)
    revolution_log.setup_all()

    # Revolution - servo
    revolution_servo = revolution.Servo_control_client(uav_talk,
                                                       REV_SERVO_CHANNEL,
                                                       REV_SERVO_MIN,
                                                       REV_SERVO_MAX,
                                                       REV_SERVO_DEG,)

    # Revolution - buzzer
    # -------------------------------------------------------------<==
    # TODO: write module for buzzer
    # -------------------------------------------------------------<==

    # GSM
    # -------------------------------------------------------------<==
    # TODO: write module for GSM
    # -------------------------------------------------------------<==

    # TSL2561
    pi_tsl2561 = tsl2561.Tsl2561_control_client()
    pi_tsl2561.setup()

    # Pi - ADS1115
    pi_ads1115 = ads1115.Ads1115_control_client(i2c_line)
    ads1115.setup()

    # ================================================================
    # First data block
    # ================================================================