from control_functions import *
from settings import *
import log
import time
import inav

if __name__ == '__main__':
    start_time = time.time()
    board_state = BOARD_SATAE_INIT
    tic = 0

    while True:
        if board_state == BOARD_SATAE_INIT:
            uart = init_uart()
            i2c = init_i2c()

            trigger_hardware = Trigger_interface(TRIGGER_PIN)
            trigger_hardware.init()

            fuse_hardware = []
            fuse_hardware.append(Fuse_interface(FUSE_1_PIN))
            fuse_hardware.append(Fuse_interface(FUSE_2_PIN))
            for fuse in fuse_hardware:
                fuse.init()

            motor_hardware = Motor_interface(MOTOR_PIN)
            motor_hardware.init()

            data_log = log.Log_control_client(LOG_BASE_PATH)
            data_log.setup()

            if (i2c is None) or (uart is None):
                board_state = BOARD_SATAE_ERROR
                continue

            data_hardware = []
            data_hardware.append(Ads1115_interface(i2c))
            data_hardware.append(Bmp180_interface(i2c))
            data_hardware.append(Tsl2561_interface(i2c))
            for hardware in data_hardware:
                hardware.init()

            flight_hardware = Inav_interface(uart)
            flight_hardware.init()

            rc_hardware = []
            rc_hardware.append(Socket_interface(IP, PORT))
            rc_hardware.append(Nrf24l01_interface([CE_PIN, CHANNEL, PIPES,
                                                   NRF24_FREQ, ADDRESS_WIDTH,
                                                   DATA_RATE, CRC_LEN]))
            for hardware in rc_hardware:
                hardware.init()

            buzzer_hardware = Buzzer_interface(BUZZER_PIN)
            buzzer_hardware.init()

            i2c_rc_hardware = Inav_rc_interface(i2c)
            i2c_rc_hardware.init()

            message_arm_conv = inav.cut_data(MESSAGE_ARM)
            message_lending_conv = inav.cut_data(MESSAGE_LENDING)
            message_wp_conv = inav.cut_data(MESSAGE_WP)
            message_hp_conv = inav.cut_data(MESSAGE_HP)
            message_rth_conv = inav.cut_data(MESSAGE_RTH)
            message_fs_conv = inav.cut_data(MESSAGE_FS)

            all_hardware = rc_hardware + data_hardware + [buzzer_hardware] + [flight_hardware] + [i2c_rc_hardware]

            observer = Observer()
            observer.init_lux_observer(LUX_LEVEL_K)
            observer.init_gps_observer(DROP_SQUARE)
            observer.init_voltage_observer(K, VOLTAGE_MIN)
            observer.init_height_observer(None)

            board_state = BOARD_FIRST_DATA

            timeout_end = None

        elif board_state == BOARD_FIRST_DATA:
            observer.find_lux_max(data_buf[TSL2561_NUM])
            observer.init_height_observer(data_buf[BMP180_NUM])
            if (observer.pressure_at_start is not None) and (observer.lux_max is not None):
                if timeout_end is None:
                    buzzer_hardware.control(True)
                    timeout_end = time.time() + BUZZER_TIMER
                elif time.time() > timeout_end:
                    buzzer_hardware.control(False)
                    board_state = BOARD_SATAE_BEFORE_START
                    timeout_end = None
                else:
                    time.sleep(0.02)

        elif board_state == BOARD_SATAE_BEFORE_START:
            if trigger_hardware.get_data():
                observer.find_lux_min(data_buf[TSL2561_NUM])
                if (observer.lux_min is not None):
                    if timeout_end is None:
                        buzzer_hardware.control(True)
                        timeout_end = time.time() + BUZZER_TIMER
                    elif time.time() > timeout_end:
                        buzzer_hardware.control(False)
                        board_state = BOARD_SATAE_WAIT_100
                    else:
                        time.sleep(0.02)

            else:
                observer.find_lux_max(data_buf[TSL2561_NUM])

        elif board_state == BOARD_SATAE_WAIT_100:
            if (data_buf[BMP180_NUM] is not None) and (not observer.compare_height(data_buf[BMP180_NUM], HEIGHT_START)):
                observer.max_height = 100
                board_state = BOARD_SATAE_IN_THE_ROCKET

        elif board_state == BOARD_SATAE_IN_THE_ROCKET:
            if observer.compare_lux(data_buf[TSL2561_NUM]) or observer.compare_height(data_buf[BMP180_NUM], observer.max_height * HEIGHT_PART):
                timeout_end = time.time() + SEPARATE_TIMEOUT
                board_state = BOARD_SATAE_SEPARATE_WAIT
            else:
                observer.find_lux_min(data_buf[TSL2561_NUM])

        elif board_state == BOARD_SATAE_SEPARATE_WAIT:
            if time.time() > timeout_end:
                timeout_end = [time.time() + MOTOR_TIMEOUT, time.time() + FUSE_TIMEOUT]
                end = [0, 0]
                motor_hardware.control(True)
                fuse_hardware[0].control(True)
                board_state = BOARD_SATAE_PREPARE_FOR_FLIGHT

        elif board_state == BOARD_SATAE_PREPARE_FOR_FLIGHT:
            if time.time() > timeout_end[0]:
                motor_hardware.control(False)
                end[0] = 1

            if time.time() > timeout_end[1]:
                fuse_hardware[0].control(False)
                end[1] = 1

            if ((end[0] == 1) and (end[1] == 1)):
                i2c_rc_hardware.send_message(message_arm_conv)
                board_state = BOARD_SATAE_LENDING

        elif board_state == BOARD_SATAE_LENDING:
            if observer.compare_height(data_buf[BMP180_NUM], HEIGHT_WP):
                board_state = BOARD_SATAE_WP
                observer.init_gps_observer(DROP_SQUARE)
                i2c_rc_hardware.send_message(message_wp_conv)
            else:
                i2c_rc_hardware.send_message(message_lending_conv)
        elif board_state == BOARD_SATAE_WP:
            if observer.compare_gps(data_buf[INAV_GPS_DATA_NUM + 2], data_buf[INAV_GPS_DATA_NUM + 3]):
                i2c_rc_hardware.send_message(message_hp_conv)
                board_state = BOARD_SATAE_DROP
                timeout_end = time.time() + FUSE_TIMEOUT
                fuse_hardware[1].control(True)
            else:
                i2c_rc_hardware.send_message(message_wp_conv)

        elif board_state == BOARD_SATAE_DROP:
            if time.time() > timeout_end:
                fuse_hardware[1].control(False)
                board_state = BOARD_SATAE_RTH
                observer.init_gps_observer(HOME_SQUARE)
                timeout_end = None
            i2c_rc_hardware.send_message(message_hp_conv)

        elif board_state == BOARD_SATAE_RTH:
            if observer.compare_gps(data_buf[INAV_GPS_DATA_NUM + 2], data_buf[INAV_GPS_DATA_NUM + 3]):
                i2c_rc_hardware.send_message(message_hp_conv)
                if timeout_end is None:
                    buzzer_hardware.control(True)
                    timeout_end = time.time() + BUZZER_TIMER
                elif time.time() > timeout_end:
                    buzzer_hardware.control(False)
                else:
                    time.sleep(0.02)

            else:
                i2c_rc_hardware.send_message(message_rth_conv)

        elif board_state == BOARD_SATAE_FILESAFE:
            i2c_rc_hardware.send_message(message_fs_conv)

        data_buf = []
        data_send_buf = []
        for hardware in data_hardware:
            hardware.update()
            data_buf = data_buf + hardware.get_data()
        flight_hardware.update()
        data_buf = data_buf + flight_hardware.get_data()
        data_buf = data_buf + flight_hardware.get_gps_data()
        data_buf = data_buf + flight_hardware.get_attitude()


        data_buf = [time.time() - start_time] + data_buf + [board_state]

        data_buf_log = hide_none(data_buf)
        data = pack_data(data_buf)

        data_log.write_data(data_buf)

        for hardware in rc_hardware:
            hardware.send(data)

        if observer.compare_voltage(data_buf[ADS1115_NUM:ADS1115_NUM + 3]):
            buzzer_hardware.control(True)
            board_state = BOARD_SATAE_FILESAFE

        if tic == 20:
            for hardware in all_hardware:
                if hardware.control_client is None:
                    hardware.init()
            tic = 0
        else:
            tic += 1
