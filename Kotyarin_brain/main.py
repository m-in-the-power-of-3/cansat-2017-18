from control_functions import *
from settings import *
import log
import time
#nmcli dev wifi connect Belochka password Acetican3 ifname wlan0
if __name__ == '__main__':
    start_time = time.time()
    board_state = BOARD_SATAE_INIT
    tic = 0

    while True:
        print(board_state)
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

            rc_hardware = Send_manager()
            rc_hardware.init()
            rc_hardware.start()

            buzzer_hardware = Buzzer_interface(BUZZER_PIN)
            buzzer_hardware.init()

            i2c_rc_hardware = Inav_rc_interface(i2c)
            i2c_rc_hardware.init()

            all_hardware = data_hardware + [buzzer_hardware] + [flight_hardware]

            observer = Observer()
            observer.init_lux_observer(LUX_LEVEL_K)
            observer.init_gps_observer(LAT_MIN, LON_MIN, LAT_MAX, LON_MAX)
            observer.init_height_observer(None)

            board_state = BOARD_SATAE_BEFORE_START

        elif board_state == BOARD_SATAE_BEFORE_START:
            if observer.pressure_at_start is not None:
                if trigger_hardware.get_data():
                    observer.find_lux_min(data_buf[TSL2561_NUM])
                    if (observer.lux_min is not None) and (observer.lux_max is not None):
                        board_state = BOARD_SATAE_IN_THE_ROCKET
                else:
                    observer.find_lux_max(data_buf[TSL2561_NUM])
            else:
                observer.init_height_observer(data_buf[TSL2561_NUM])

        elif board_state == BOARD_SATAE_IN_THE_ROCKET:
            if observer.compare_lux(data_buf[TSL2561_NUM]):
                timeout_end = time.time() + MOTOR_TIMEOUT
                motor_hardware.control(True)
                board_state = BOARD_SATAE_OPEN_BEAMS
            else:
                observer.find_lux_min(data_buf[TSL2561_NUM])

        elif board_state == BOARD_SATAE_OPEN_BEAMS:
            if time.time() > timeout_end:
                timeout_end = time.time() + FUSE_TIMEOUT
                motor_hardware.control(False)
                fuse_hardware[0].control(True)
                board_state = BOARD_SATAE_DROP_PARACHUTE

        elif board_state == BOARD_SATAE_DROP_PARACHUTE:
            if time.time() > timeout_end:
                fuse_hardware[0].control(False)
                board_state = BOARD_SATAE_LENDING

        elif board_state == BOARD_SATAE_LENDING:
            if observer.compare_height(data_buf[BMP180_NUM], HEIGHT_WP):
                board_state = BOARD_SATAE_WP
            else:
                i2c_rc_hardware.send_message(MESSAGE_LENDING)

        elif board_state == BOARD_SATAE_WP:
            if observer.compare_gps(data_buf[INAV_GPS_DATA_NUM]):
                board_state = BOARD_SATAE_DROP
                timeout_end = time.time() + FUSE_TIMEOUT
                fuse_hardware[1].control(True)
            else:
                i2c_rc_hardware.send_message(MESSAGE_WP)

        elif board_state == BOARD_SATAE_DROP:
            if time.time() > timeout_end:
                fuse_hardware[1].control(False)
                board_state = BOARD_SATAE_RTH

        elif board_state == BOARD_SATAE_RTH:
            pass


        elif board_state == BOARD_SATAE_FILESAFE:
            pass
        else:
            pass

        data_buf = []
        for hardware in data_hardware:
            hardware.update()
            data_buf = data_buf + hardware.get_data()
        flight_hardware.update()
        data_buf = data_buf + flight_hardware.get_data()
        data_buf = data_buf + flight_hardware.get_gps_data()
        data_buf = data_buf + flight_hardware.get_attitude()

        data_buf = [time.time() - start_time] + data_buf

        data_buf = hide_none(data_buf)
        data = pack_data(data_buf)

        data_log.write_data(data_buf)
        print(data_buf)

        rc_hardware.add_data(data)

        if tic == 20:
            for hardware in all_hardware:
                if hardware.control_client is None:
                    hardware.init()
            tic = 0
        else:
            tic += 1
