import time

from settings import *
from errors import *
from functions_for_main import *

STATE = {"error": -1,
         "init": 0,
         "before start": 1,
         "in the rocket": 2,
         "free fall": 3,
         "descent by parachute": 4}

SMS_ERROR = {"none": "Error: none",
             "npna io": "Error: Init io npna error",
             "uavtalk init": "Error: Init uavtalk error.",
             "revolution init": "Error: Init revolution error",
             "tsl2561 init": "Error: Init tsl2561 error",
             "ads1115 init": "Error: Init ads1115 error",
             "trigger init": "Error: Init trigger error",
             "gsm init": "Error: Init gsm error",
             "buzzer init": "Error: Init buzzer error",
             "fuse init": "Error: Init fuse error",
             "pressure": "Error: Pressure value error",
             "trigger": "Error: Trigger error",
             "gsm sms": "Error: Gsm error",
             "tsl2561": "Error: Tsl2561 value error",
             "battery": "Error: Battary error",
             "bmp180 init": "Error: Init BMP180 error",
             "bmp180": "Error: BMP180 error"}

SMS_MESSAGE = {"error": "Fatal error",
               "init": "Init OK",
               "rocket": "I am in the rocket",
               "separated": "I was separated from rocket",
               "parachute": "I was opened parachute"}


if __name__ == '__main__':
    sms_error = SMS_ERROR["none"]

    Pressure_at_the_start = 0
    Height_now = 0
    # State at the begining
    State = STATE["init"]
    # ================================================================
    # Work cycle
    # ================================================================
    while True:
        try:
            check_data()
        except BatteryError:
            deb_print("Battery error")
            sms_error = SMS_ERROR["battery"]
            State = STATE["error"]
        except BMP180Error:
            deb_print("BMP180 error")
            sms_error = SMS_ERROR["bmp180"]
            State = STATE["error"]
        # -------------------------------------------------------------------<======
        except BaseException:
            sms_error = "Unknown error 1"
            State = STATE["error"]
        # -------------------------------------------------------------------<======

        if (State == STATE["init"]):
            # ================================================================
            # Init block
            # ================================================================
            try:
                init_all()
            except IOError:
                deb_print("Init IO error")
                sms_error = SMS_ERROR["npna io"]
                State = STATE["error"]
            except TriggerError:
                deb_print("Init trigger error (init block)")
                sms_error = SMS_ERROR["trigger init"]
                State = STATE["error"]
            except UAVTalkError:
                deb_print("Init UAVTalk error (init block)")
                sms_error = SMS_ERROR["uavtalk init"]
                State = STATE["error"]
            except RevolutionError:
                deb_print("Init revolution error (init block)")
                sms_error = SMS_ERROR["revolution init"]
                State = STATE["error"]
            except TSL2561Error:
                deb_print("Init tsl2561 error (init block)")
                sms_error = SMS_ERROR["tsl2561 init"]
                State = STATE["error"]
            except ADS1115Error:
                deb_print("Init ads1115 error (init block)")
                sms_error = SMS_ERROR["ads1115 init"]
                State = STATE["error"]
            except GsmError:
                deb_print("Init gsm error (init block)")
                sms_error = SMS_ERROR["gsm init"]
                State = STATE["error"]
            except BuzzerError:
                deb_print("Init buzzer error (init block)")
                sms_error = SMS_ERROR["buzzer init"]
                State = STATE["error"]
            except FuseError:
                deb_print("Init Fuse error (init block)")
                sms_error = SMS_ERROR["fuse init"]
                State = STATE["error"]
            except BMP180Error:
                deb_print("Init BMP180 error (init block)")
                sms_error = SMS_ERROR["bmp180 init"]
                State = STATE["error"]
            # -------------------------------------------------------------------<======
            except BaseException:
                sms_error = "Unknown error 2"
                State = STATE["error"]
            # -------------------------------------------------------------------<======
            else:
                try:
                    deb_print("pressure")
                    save_pressure_at_start()
                    deb_print("Finish init block")
                    sms([SMS_MESSAGE["init"], sms_error])
                    State = STATE["before start"]
                    count_max_lux()
                except RevolutionError:
                    deb_print("Error with pressure value")
                    sms_error = SMS_ERROR["pressure"]
                    State = STATE["error"]
                except GsmError:
                    deb_print("Gsm sms error")
                    sms_error = SMS_ERROR["gsm sms"]
                    State = STATE["error"]
                except BMP180Error:
                    deb_print("BMP180 error")
                    sms_error = SMS_ERROR["bmp180"]
                    State = STATE["error"]
                # -------------------------------------------------------------------<======
                except BaseException:
                    sms_error = "Unknown error 3"
                    State = STATE["error"]
                # -------------------------------------------------------------------<======

            continue

        elif (State == STATE["before start"]):
            # ================================================================
            # Before start block
            # ================================================================
            try:
                if (check_trigger()):
                    sms([SMS_MESSAGE["rocket"], sms_error])
                    State = STATE["in the rocket"]
                    count_min_lux()
                else:
                    print "trigger"
                    count_max_lux()
            except TriggerError:
                deb_print("Trigger error")
                sms_error = SMS_ERROR["trigger"]
                State = STATE["error"]
            except GsmError:
                deb_print("Gsm sms error")
                sms_error = SMS_ERROR["gsm sms"]
                State = STATE["error"]
            # -------------------------------------------------------------------<======
            except BaseException:
                sms_error = "Unknown error 4"
                State = STATE["error"]
            # -------------------------------------------------------------------<======

            continue

        elif (State == STATE["in the rocket"]):
            # ================================================================
            # In the rocket block
            # ================================================================
            try:
                if (check_lux()):
                    sms([SMS_MESSAGE["separated"], sms_error])
                    State = STATE["free fall"]
                else:
                    count_min_lux()
            except GsmError:
                deb_print("Gsm sms error")
                sms_error = SMS_ERROR["gsm sms"]
                State = STATE["error"]
            # -------------------------------------------------------------------<======
            except BaseException:
                sms_error = "Unknown error 5"
                State = STATE["error"]
            # -------------------------------------------------------------------<======

            continue

        elif (State == STATE["free fall"]):
            # ================================================================
            # Free fall block
            # ================================================================
            try:
                if (check_height(HEIGHT_PARACHUTE)):
                    sms([SMS_MESSAGE["parachute"], sms_error])
                    open_parachute()
                    State = STATE["descent by parachute"]
            except GsmError:
                deb_print("Gsm sms error")
                sms_error = SMS_ERROR["gsm sms"]
                State = STATE["error"]
            except BMP180Error:
                deb_print("BMP180 error")
                sms_error = SMS_ERROR["bmp180"]
                State = STATE["error"]
            except RevolutionError:
                deb_print("Revolution error")
                sms_error = SMS_ERROR["pressure"]
                State = STATE["error"]
            # -------------------------------------------------------------------<======
            except BaseException:
                sms_error = "Unknown error 6"
                State = STATE["error"]
            # -------------------------------------------------------------------<======

            continue

        elif (State == STATE["descent by parachute"]):
            # ================================================================
            # Descent by parachute block
            # ================================================================
            try:
                deb_print("We are desenting by parachute")
            except GsmError:
                deb_print("Gsm sms error")
                sms_error = SMS_ERROR["gsm sms"]
                State = STATE["error"]
            # -------------------------------------------------------------------<======
            except BaseException:
                sms_error = "Unknown error 7"
                State = STATE["error"]
            # -------------------------------------------------------------------<======

            continue

        elif (State == STATE["error"]):
            # ================================================================
            # Error block
            # ================================================================
            try:
                if not (sms_error == "gsm sms"):
                    sms([SMS_MESSAGE["error"], sms_error])
                if not (sms_error == SMS_ERROR["buzzer init"]):
                    buzzer_control(True)
                    time.sleep(7)
            finally:
                deinit_all()

            break

