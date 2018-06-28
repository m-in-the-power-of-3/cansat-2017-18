from librepilot.uavtalk.uavobject import *
from librepilot.uavtalk.uavtalk import *
from librepilot.uavtalk.objectManager import *
from librepilot.uavtalk.connectionManager import *

DEFINITIONS_PATH = "/home/pi/Kotyarin_brain/librepilot/uavobject-synthetics"

DATA_TYPE = {"pressure": 1, "accel": 2}


class Uavtalk():
    def __init__(self):
        self.nbUpdates = 0
        self.lastRateCalc = time.time()
        self.updateRate = 0
        self.objMan = None
        self.connMan = None

    def setup(self, port):
        serPort = port
        self.uavTalk = UavTalk(serPort, None)

        self.objMan = ObjManager(self.uavTalk)
        self.objMan.importDefinitions(DEFINITIONS_PATH)

        self.uavTalk.start()

        self.connMan = ConnectionManager(self.uavTalk, self.objMan)

        self.connMan.connect()

        self.objMan.requestAllObjUpdate()

    def stop(self):
        if self.uavTalk:
            self.uavTalk.stop()


class All_telemetry_logger():
    def __init__(self, uavt, period):
        self.ATL_uavtalk = uavt
        self.telemetry_log_acc = open('telemetry_log/accel.txt', 'a')
        self.telemetry_log_att = open('telemetry_log/attitude.txt', 'a')
        self.telemetry_log_gyr = open('telemetry_log/gyro.txt', 'a')
        self.telemetry_log_vel = open('telemetry_log/velocity.txt', 'a')
        self.telemetry_log_mag = open('telemetry_log/mag.txt', 'a')
        self.update_period = period
        self._setup_update()
        self.pressure = 0
        self.accel = 0
        self.attitude = 0
        self.gyro = 0
        self.velocity = 0
        self.mag = 0

    def setup_all(self):
        self.setup_log_head()
        self.setup_observer()

    def setup_log_head(self):
        self.telemetry_log_acc.write("Time,X,Y,Z\n")
        self.telemetry_log_att.write("Time,Roll,Yaw,Pitch\n")
        self.telemetry_log_gyr.write("Time,X,Y,Z\n")
        self.telemetry_log_vel.write("Time,North,East,Down\n")
        self.telemetry_log_mag.write("Time,X,Y,Z\n")

    def _setup_update(self):
        #Accel settings
        self.ATL_uavtalk.objMan.AccelState.metadata.telemetryUpdateMode = UAVMetaDataObject.UpdateMode.PERIODIC
        self.ATL_uavtalk.objMan.AccelState.metadata.telemetryUpdatePeriod.value = self.update_period
        self.ATL_uavtalk.objMan.AccelState.metadata.updated()

        #Attitude settings
        self.ATL_uavtalk.objMan.AttitudeState.metadata.telemetryUpdateMode = UAVMetaDataObject.UpdateMode.PERIODIC
        self.ATL_uavtalk.objMan.AttitudeState.metadata.telemetryUpdatePeriod.value = self.update_period
        self.ATL_uavtalk.objMan.AttitudeState.metadata.updated()

        #Gyro settings
        self.ATL_uavtalk.objMan.GyroState.metadata.telemetryUpdateMode = UAVMetaDataObject.UpdateMode.PERIODIC
        self.ATL_uavtalk.objMan.GyroState.metadata.telemetryUpdatePeriod.value = self.update_period
        self.ATL_uavtalk.objMan.GyroState.metadata.updated()

        #Velocity settings
        self.ATL_uavtalk.objMan.VelocityState.metadata.telemetryUpdateMode = UAVMetaDataObject.UpdateMode.PERIODIC
        self.ATL_uavtalk.objMan.VelocityState.metadata.telemetryUpdatePeriod.value = self.update_period
        self.ATL_uavtalk.objMan.VelocityState.metadata.updated()

        #Mag settings
        self.ATL_uavtalk.objMan.MagSensor.metadata.telemetryUpdateMode = UAVMetaDataObject.UpdateMode.PERIODIC
        self.ATL_uavtalk.objMan.MagSensor.metadata.telemetryUpdatePeriod.value = self.update_period
        self.ATL_uavtalk.objMan.MagSensor.metadata.updated()

    def setup_observer(self):
        self.ATL_uavtalk.objMan.regObjectObserver(self.ATL_uavtalk.objMan.AccelState, self, "method_acc")
        self.ATL_uavtalk.objMan.regObjectObserver(self.ATL_uavtalk.objMan.AttitudeState, self, "method_att")
        self.ATL_uavtalk.objMan.regObjectObserver(self.ATL_uavtalk.objMan.GyroState, self, "method_gyr")
        self.ATL_uavtalk.objMan.regObjectObserver(self.ATL_uavtalk.objMan.VelocityState, self, "method_vel")
        self.ATL_uavtalk.objMan.regObjectObserver(self.ATL_uavtalk.objMan.MagSensor, self, "method_mag")

    def method_acc(self, args):
        self.accel = [self.ATL_uavtalk.objMan.AccelState.x.value,
                      self.ATL_uavtalk.objMan.AccelState.y.value,
                      self.ATL_uavtalk.objMan.AccelState.z.value]

        self.telemetry_log_acc.write(str(time.time()) + "," +
                                     str(self.ATL_uavtalk.objMan.AccelState.x.value) + "," +
                                     str(self.ATL_uavtalk.objMan.AccelState.y.value) + "," +
                                     str(self.ATL_uavtalk.objMan.AccelState.z.value)+ "\n")

    def method_att(self, args):
        self.attitude = [self.ATL_uavtalk.objMan.AttitudeState.Roll.value,
                         self.ATL_uavtalk.objMan.AttitudeState.Pitch.value,
                         self.ATL_uavtalk.objMan.AttitudeState.Yaw.value]

        self.telemetry_log_att.write(str(time.time()) + "," +
                                     str(self.ATL_uavtalk.objMan.AttitudeState.Roll.value) + "," +
                                     str(self.ATL_uavtalk.objMan.AttitudeState.Pitch.value) + "," +
                                     str(self.ATL_uavtalk.objMan.AttitudeState.Yaw.value) + "\n")
    
    def method_gyr(self, args):
        self.gyro = [self.ATL_uavtalk.objMan.GyroState.x.value,
                     self.ATL_uavtalk.objMan.GyroState.y.value,
                     self.ATL_uavtalk.objMan.GyroState.z.value]

        self.telemetry_log_gyr.write(str(time.time()) + "," +
                                     str(self.ATL_uavtalk.objMan.GyroState.x.value) + "," +
                                     str(self.ATL_uavtalk.objMan.GyroState.y.value) + "," +
                                     str(self.ATL_uavtalk.objMan.GyroState.z.value) + "\n")

    def method_vel(self, args):
        self.velocity = [self.ATL_uavtalk.objMan.VelocityState.North.value,
                         self.ATL_uavtalk.objMan.VelocityState.East.value,
                         self.ATL_uavtalk.objMan.VelocityState.Down.value]

        self.telemetry_log_vel.write(str(time.time()) + "," +
                                     str(self.ATL_uavtalk.objMan.VelocityState.North.value) + "," +
                                     str(self.ATL_uavtalk.objMan.VelocityState.East.value) + "," +
                                     str(self.ATL_uavtalk.objMan.VelocityState.Down.value) + "\n")
    
    def method_mag(self, args):
        self.mag = [self.ATL_uavtalk.objMan.MagSensor.x.value,
                    self.ATL_uavtalk.objMan.MagSensor.y.value,
                    self.ATL_uavtalk.objMan.MagSensor.z.value]

        self.telemetry_log_mag.write(str(time.time()) + "," +
                                     str(self.ATL_uavtalk.objMan.MagSensor.x.value) + "," +
                                     str(self.ATL_uavtalk.objMan.MagSensor.y.value) + "," +
                                     str(self.ATL_uavtalk.objMan.MagSensor.z.value) + "\n")

    def get_data(self, data_type):
        if (data_type == DATA_TYPE["press"]):
            return self.pressure
        elif (data_type == DATA_TYPE["accel"]):
            return self.accel

    def close(self):
        self.telemetry_log_acc.close()
        self.telemetry_log_att.close()
        self.telemetry_log_gyr.close()
        self.telemetry_log_vel.close()
        self.telemetry_log_mag.close()


class Servo_control_client():
    def __init__(self, uavt, channel, min, max, deg_ran):
        self.SCC_uavtalk = uavt
        self.channel = channel
        self._setup()
        self.setup_time_range(min, max, deg_ran)

    def _setup(self):
        self.SCC_uavtalk.objMan.ActuatorSettings.metadata.access = UAVMetaDataObject.Access.READONLY
        self.SCC_uavtalk.objMan.ActuatorSettings.metadata.updated()

    def setup_time_range(self, min, max, deg_ran):
        self.__min = min
        self.__max = max
        self.SCC_uavtalk.objMan.ActuatorSettings.ChannelMin.value[self.channel] = self.__min
        self.SCC_uavtalk.objMan.ActuatorSettings.ChannelMax.value[self.channel] = self.__max
        self.SCC_uavtalk.objMan.ActuatorSettings.metadata.updated()
        self.time_in_one_deg = (self.__max - self.__min) / deg_ran

    def conv_deg_to_time(self, deg):
        return round(deg * self.time_in_one_deg) + self.__min

    def rotation_deg(self, deg):
        self.rotation(self.conv_deg_to_time(deg))

    def rotation(self, position_time):
        if (position_time <= self.__max) and (position_time >= self.__min):
            self.SCC_uavtalk.objMan.ActuatorSettings.ChannelNeutral.value[self.channel] = position_time
            self.SCC_uavtalk.objMan.ActuatorSettings.updated()
