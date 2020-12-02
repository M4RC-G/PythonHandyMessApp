'''
Read linear acceleration and rotation and save both as .csv
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from jnius import autoclass
from linaccel import AndroidLinearAccelerometer
from android.permissions import request_permissions, Permission
from gyro import AndroidGyroscope
from plyer import accelerometer
import datetime
import os
import threading

class AccelerometerTest(BoxLayout):
    def __init__(self, **kwargs):
        super(AccelerometerTest, self).__init__(**kwargs)
        self.sensorEnabled = False
        self.linaccelEnabled = False
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        try:
            Environment = autoclass("android.os.Environment")
            self.sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
        except:
            self.sdpath = App.get_running_app().user_data_dir
        if not os.path.exists(os.path.join(self.sdpath, "AccGyroData")):
            os.mkdir(os.path.join(self.sdpath, "AccGyroData"))
        self.sdpath += "/AccGyroData"
        self.x_ro = []
        self.y_ro = []
        self.z_ro = []
        self.x_accel = []
        self.y_accel = []
        self.z_accel = []
        self.acc = AndroidLinearAccelerometer()
        self.gyro = AndroidGyroscope()

    def do_toggle(self):
        if not self.sensorEnabled:
            if self.linaccelEnabled:
                self.linaccel()
            self.gyro.enable()
            accelerometer.enable()

            self.x_accel.clear()
            self.y_accel.clear()
            self.z_accel.clear()
            self.x_ro.clear()
            self.y_ro.clear()
            self.z_ro.clear()
            Clock.schedule_interval(self.get_acceleration, 1 / 20.)

            self.sensorEnabled = True
            self.ids.toggle_button.text = "Stop Accelerometer"
        else:
            self.gyro.disable()
            accelerometer.disable()
            Clock.unschedule(self.get_acceleration)
            time = datetime.datetime.now()
            time = time.strftime("%H%M%S")
            if not os.path.exists(os.path.join(self.sdpath, "acceleration")):
                os.mkdir(os.path.join(self.sdpath, "acceleration"))
            f = open(self.sdpath + "/acceleration/data" + time + ".csv", "w+")
            f.write("t[s],ax[m/s2],ay[m/s2],az[m/s2],\u03C9x[rad/s],\u03C9y[rad/s],\u03C9z[rad/s]\n")
            t = 0
            for i in range(len(self.x_accel)):
                f.write(str(t) + "," + str(self.x_accel[i]) + "," + str(self.y_accel[i]) + "," + str(self.z_accel[i]) + "," + str(self.x_ro[i])
                        + "," + str(self.y_ro[i]) + "," + str(self.z_ro[i]))
                f.write("\n")
                t += 0.05

            f.close()
            self.sensorEnabled = False
            self.ids.toggle_button.text = "Start Accelerometer"

    def linaccel(self):
        try:
            if not self.linaccelEnabled:
                if self.sensorEnabled:
                    self.do_toggle()
                self.gyro.enable()
                self.acc.enable()
                self.x_accel.clear()
                self.y_accel.clear()
                self.z_accel.clear()
                self.x_ro.clear()
                self.y_ro.clear()
                self.z_ro.clear()
                Clock.schedule_interval(self.get_linearacceleration, 1 / 20.)

                self.linaccelEnabled = True
                self.ids.toggle_button2.text = "Stop Linear Accelerometer"
            else:
                self.gyro.disable()
                self.acc.disable()
                Clock.unschedule(self.get_linearacceleration)

                self.linaccelEnabled = False
                self.ids.toggle_button2.text = "Start Linear Accelerometer"
                time = datetime.datetime.now()
                time = time.strftime("%H%M%S")
                if not os.path.exists(os.path.join(self.sdpath, "linearacceleration")):
                    os.mkdir(os.path.join(self.sdpath, "linearacceleration"))
                f = open(self.sdpath + "/linearacceleration/data" + time + ".csv", "w+")
                f.write("t[s],ax[m/s2],ay[m/s2],az[m/s2],\u03C9x[rad/s],\u03C9y[rad/s],\u03C9z[rad/s]\n")
                t = 0
                for i in range(len(self.x_accel)):
                    f.write(str(t) + "," + str(self.x_accel[i]) + "," + str(self.y_accel[i]) + "," + str(self.z_accel[i]) + "," + str(self.x_ro[i])
                            + "," + str(self.y_ro[i]) + "," + str(self.z_ro[i]))
                    f.write("\n")
                    t += 0.05


                f.close()



        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_linearacceleration(self, dt):
        gyro = self.gyro.get_rotation()
        lin = self.acc.get_linearacceleration()

        if not lin == (None, None, None):
            self.ids.x_label.text = "X: " + str(lin[0])
            self.x_ro.append(gyro[0])
            self.x_accel.append(lin[0])
            self.ids.y_label.text = "Y: " + str(lin[1])
            self.y_ro.append(gyro[1])
            self.y_accel.append(lin[1])
            self.ids.z_label.text = "Z: " + str(lin[2])
            self.z_ro.append(gyro[2])
            self.z_accel.append(lin[2])

    def get_acceleration(self, dt):
        gyro = self.gyro.get_rotation()
        accel = accelerometer.acceleration

        if not accel == (None, None, None):
            self.ids.x_label.text = "X: " + str(accel[0])
            self.x_ro.append(gyro[0])
            self.x_accel.append(accel[0])
            self.ids.y_label.text = "Y: " + str(accel[1])
            self.y_ro.append(gyro[1])
            self.y_accel.append(accel[1])
            self.ids.z_label.text = "Z: " + str(accel[2])
            self.z_ro.append(gyro[2])
            self.z_accel.append(accel[2])


class AccelerometerTestApp(App):
    def build(self):
        return AccelerometerTest()

    def on_pause(self):
        return True


if __name__ == '__main__':
    AccelerometerTestApp().run()
