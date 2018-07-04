import socket
import time
import threading

GYRO_LOG = "/home/developer/Kotyarin/Kotyarin_brain/telemetry_log/gyro.txt"
ACCEL_LOG = "/home/developer/Kotyarin/Kotyarin_brain/telemetry_log/accel.txt"
VOL_LOG = "/home/developer/Kotyarin/Kotyarin_brain/telemetry_log/vol.txt"
LUX_LOG = "/home/developer/Kotyarin/Kotyarin_brain/telemetry_log/lux.txt"

DATA_LOG = "/home/developer/git/cansat-2017-2018/H_CGS/telemetry_log/data.txt"

IP = "0.0.0.0"
PORT = 1917

data_now = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class H_log():
    def __init__(self):
        self.gyro_log = open(GYRO_LOG, 'r')
        self.accel_log = open(ACCEL_LOG, 'r')
        self.vol_log = open(VOL_LOG, 'r')
        self.lux_log = open(LUX_LOG, 'r')

        self.gyro_log.readline()
        self.accel_log.readline()
        self.vol_log.readline()
        self.lux_log.readline()
        self.lux_log.readline()

    def read_log(self):
        gyro_log = self.gyro_log.readline()
        accel_log = self.accel_log.readline()
        vol_log = self.vol_log.readline()
        lux_log = self.lux_log.readline()

        gyro = self.str_analysis(gyro_log, 3)
        accel = self.str_analysis(accel_log, 3)
        vol = self.str_analysis(vol_log, 4)
        lux = self.str_analysis(lux_log, 1)

        time = [(self.take_time(gyro_log) + self.take_time(accel_log)) / 2]

        return time + accel + gyro + lux + vol

    def take_time(self, string):
        num = string.find(",")
        if (num == -1):
            raise ValueError('Uncorrect string')
        return float(string[:num])


    def str_analysis(self, string, size):
        ret = []
        num = []
        print(string)

        num.append(string.find(","))
        if (num[0] == -1):
            raise ValueError('Uncorrect string')

        if not (size == 1):
            for i in range(size - 1):
                num.append(string.find(",", (num[i] + 1)))
                if (num[i + 1] == -1):
                    raise ValueError('Uncorrect string')
                ret.append(float(string[(num[i] + 1):num[i + 1]]))

        ret.append(float(string[num[size-1] + 1:]))
        return ret


class H_telemetry():
    def __init__(self):
        self.data_log = open(DATA_LOG, 'a')

    def setup_socket(self):
        print ("init socket")
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)

        self.sock.bind((IP, PORT))

    def setup(self):
        print("init")
        self.data_log.write("Time, Accel_x, Accel_y, Accel_z," +
                            "Gyro_x, Gyro_y, Gyro_z, Lux," +
                            "Voltage_1, Voltage_1, Voltage_1, Voltage_1\n")
        self.data_threat = threading.Thread(target=self.get_telemetry)
        self.data_threat.daemon = False
        self.data_lock = threading.Lock()
        self.stop_lock = threading.Lock()
        self.data_threat.start()
        self.stop = False

    def get_data(self):
        print ("getting data")
        data, addr = self.sock.recvfrom(1024)
        data = data.decode('ascii')
        print (data)
        ret = []

        old_num = 0
        num = data.find(",")

        while not (num == -1):
            ret.append(data[old_num:num])
            old_num = num + 1
            num = data.find(",", old_num)
        ret.append(data[(num + 1):])

        return data

    def get_telemetry(self):
        global data_now

        while True:
            print("thread")
            data = self.get_data()
            if (len(data) == 14):
                self.data_log.write(str(data[0] + "," +
                                        data[1] + "," +
                                        data[2] + "," +
                                        data[3] + "," +
                                        data[4] + "," +
                                        data[5] + "," +
                                        data[6] + "," +
                                        data[7] + "," +
                                        data[8] + "," +
                                        data[9] + "," +
                                        data[10] + "," +
                                        data[11] + "\n"))

                self.data_lock.acquire()
                data_now = data
                self.data_lock.release()

            self.stop_lock.acquire()
            if (self.stop):
                break
            self.stop_lock.release()

    def read_telemetry(self):
        global data_now

        self.data_lock.acquire()
        ret = data_now
        self.data_lock.release()
        return ret

    def close(self):
        self.data_log.close()
        self.stop_lock.acquire()
        self.stop = True
        self.stop_lock.release()

        self.data_threat.join()



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)

    sock.bind((IP, PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        print(data)