import time

from settings import *
from errors import *
from functions_for_main import *

STATE = {"error": -1, "init": 0, "before start": 1}

SMS_ERROR = {"none": "Error: none",
             "npna io": "Error: Init io npna error",
             "uavtalk init": "Error: Init uavtalk error.",
             "revolution init": "Error: Init revolution error",
             "tsl2561 init": "Error: Init tsl2561 error",
             "ads1115 init": "Error: Init ads1115 error",
             "trigger init": "Error: Init trigger error",
             "gsm init": "Error: Init gsm error",
             "buzzer init": "Error: Init buzzer error",
             "pressure": "Error: Pressure value error",
             "trigger": "Error: Trigger error",
             "gsm sms": "Error: Gsm error"}

SMS_MESSAGE = {"error": "Fatal error",
               "init": "Init OK",
               "rocket": "We are in the rocket"}


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
            except TriggerError:
                deb_print("Init trigger error (init block)")
                sms_error = SMS_ERROR["trigger init"]
                State = STATE["error"]
            except GsmError:
                deb_print("Init gsm error (init block)")
                sms_error = SMS_ERROR["gsm init"]
                State = STATE["error"]
            except BuzzerError:
                deb_print("Init buzzer error (init block)")
                sms_error = SMS_ERROR["buzzer init"]
                State = STATE["error"]
            else:
                try:
                    deb_print("pressure")
                    # Pressure_at_the_start = get_pressure()
                except RevolutionError:
                    deb_print("Error with pressure value")
                    sms_error = SMS_ERROR["pressure"]
                    State = STATE["error"]
                else:
                    deb_print("Finish init block")
                    sms([SMS_MESSAGE["init"], sms_error])
                    State = STATE["before start"]

            continue

        elif (State == STATE["before start"]):
            try:
                if (check_trigger()):
                    sms([SMS_MESSAGE["rocket"], sms_error])
                    State = STATE["before start"]
            except TriggerError:
                deb_print("Trigger error")
                sms_error = SMS_ERROR["trigger"]
                State = STATE["error"]
            except GsmError:
                deb_print("Gsm sms error")
                sms_error = SMS_ERROR["gsm sms"]
                State = STATE["error"]

            continue

        elif (State == STATE["error"]):
            try:
                sms([SMS_MESSAGE["error"], sms_error])
                if not (sms_error == SMS_ERROR["buzzer init"]):
                    buzzer_control(True)
                    time.sleep(7)
            finally:
                deinit_all()

        break
