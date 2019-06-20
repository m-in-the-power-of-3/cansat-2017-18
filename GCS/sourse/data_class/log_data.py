#!/usr/bin/python3

from config import *
import time
from sourse.exceptions import *

class Data_source():
    def __init__(self, log_path, real_time=True, time_delay=0.01):
        self.log_path = log_path
        self.real_time = real_time
        self.time_delay = time_delay

    def start(self):
        self.log = open(self.log_path, 'r')
        self.log.readline()
        self.time_shift = None

    def change_log_path(self, log_path):
        self.log_path = log_path

    def read_data(self):
        string_data = self.log.readline()
        return_data = []

        # Ищем первую запятую.
        # Так, как строка данных состоит из времени и данных,
        # запятая должна присутствовать всегда
        comma = string_data.find(",")
        if (comma == -1):
            raise DataThreadEnd('Log end')

        return_data.append(float(string_data[:comma]))

        while True:
            value_ptr = comma + 1  # Номер первого символа значения (стоит сразу после запятой)
            comma = string_data.find(",", value_ptr)
            if (comma == -1):  # Если не найдена следующая запятая
                return_data.append(float(string_data[value_ptr:]))
                break
            return_data.append(float(string_data[value_ptr: comma]))

        if self.time_shift == None:
            self.time_shift = return_data[0]
            return_data[0] = 0
            if self.real_time:
                self.time_start = time.time()
            return return_data

        if self.real_time:
            while time.time() <= (self.time_start + return_data[0] - self.time_shift):
                pass
        else:
            if self.time_delay is not False:
                time.sleep(self.time_delay)

        return_data[0] = return_data[0] - self.time_shift
        return return_data

    def stop(self):
        self.log.close()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Only for test
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':
    print("start")
    obJ = Data_source("/home/developer/git/cansat-2017-2018/GCS/log/telemetry_log/telemetry_log.txt")
    print("start")
    obJ.start()
    while True:
        try:
            data = obJ.read_data()
            print (data)
        except ValueError:
            print ("end\n")
            obJ.close()
            break
        except KeyboardInterrupt:
            obJ.close()
            break
        except:
            raise
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
