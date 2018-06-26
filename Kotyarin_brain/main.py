from settings import *
from errors import *
from func import *

STATE = {"error": -1, "init": 0, "before start": 1}

SMS_ERROR = {"none": "Error: none",
             "npna io": "Error: Init io npna error",
             "uavtalk init": "Error: Init uavtalk error.",
             "revolution init": "Error: Init revolution error",
             "tsl2561 init": "Error: Init tsl2561 error",
             "ads1115 init": "Error: Init ads1115 error",
             "pressure": "Error: Pressure value error"}

if __name__ == '__main__':
    sms_error = SMS_ERROR["none"]

    Pressure_at_the_start = 0
    Height_now
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
                obj = init_all_deb()
            except UAVTalkError:
                deb_print("Init UAVTalk error (init block)")
                sms_error = SMS_ERROR["uavtalk init"]
                State = STATE["error"]
                continue
            except RevolutionError:
                deb_print("Init revolution error (init block)")
                sms_error = SMS_ERROR["revolution init"]
                State = STATE["error"]
                continue
            except TSL2561Error:
                deb_print("Init tsl2561 error (init block)")
                sms_error = SMS_ERROR["tsl2561 init"]
                State = STATE["error"]
                continue
            except ADS1115Error:
                deb_print("Init ads1115 error (init block)")
                sms_error = SMS_ERROR["ads1115 init"]
                State = STATE["error"]
                continue
            except IOError:
                deb_print("Init IO error")
                sms_error = SMS_ERROR["npna io"]
                State = STATE["error"]
                continue
            else:
                revolution_log = obj["log"]
                revolution_servo = obj["servo"]
                pi_tsl2561 = obj["tsl2561"]
                pi_ads1115 = obj["ads1115"]
                State = STATE["first data"]

        elif (State == STATE["first data"]):
            try:
                first_data(revolution_log, ads1115, tsl2561)
            except Exception:
                deb_print("First data error")
                # ------------------------------------------------------<===
                State = STATE["error"]
                continue

        elif (State == STATE["before start"]):
            try:
                Pressure_at_the_start = pressure_now(revolution_log)
            except RevolutionError:
                deb_print("Error with pressure value")
                sms_error = SMS_ERROR["pressure"]
                State = STATE["error"]
                continue




    #    elif (State == STATE["init"]):
