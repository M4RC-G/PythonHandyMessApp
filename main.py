'''
Read linear acceleration and rotation and save both as .csv
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from jnius import autoclass
from linaccel import AndroidLinearAccelerometer
from android.permissions import request_permissions, Permission
from plyer import gyroscope


class AccelerometerTest(BoxLayout):
    x_ro = []
    y_ro = []
    z_ro = []
    linx = []
    liny = []
    linz = []
    acc = AndroidLinearAccelerometer()

    def __init__(self):
        super().__init__()
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                gyroscope.enable()
                self.acc.enable()
                self.linx.clear()
                self.liny.clear()
                self.linz.clear()
                self.x_ro.clear()
                self.y_ro.clear()
                self.z_ro.clear()
                Clock.schedule_interval(self.get_acceleration, 1 / 5.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Accelerometer"
            else:
                gyroscope.disable()
                self.acc.disable()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Accelerometer"

                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
                try:
                    Environment = autoclass("android.os.Environment")
                    sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
                except:
                    sdpath = App.get_running_app().user_data_dir

                f = open(sdpath + "/data.csv", "w+")
                for i in range(len(self.linx)):
                   f.write(str(self.linx[i]) + " " + str(self.liny[i]) + " " + str(self.linz[i]) + " " + str(self.x_ro[i])
                           + " " + str(self.y_ro[i]) + " " + str(self.z_ro[i]))
                   f.write("\n")

                f.close()


        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_acceleration(self, dt):
        gyro = gyroscope.rotation
        lin = self.acc.get_linearacceleration()

        if not lin == (None, None, None):
            self.ids.x_label.text = "X: " + str(lin[0])
            self.x_ro.append(gyro[0])
            self.linx.append(lin[0])
            self.ids.y_label.text = "Y: " + str(lin[1])
            self.y_ro.append(gyro[1])
            self.liny.append(lin[1])
            self.ids.z_label.text = "Z: " + str(lin[2])
            self.z_ro.append(gyro[2])
            self.linz.append(lin[2])


class AccelerometerTestApp(App):
    def build(self):
        return AccelerometerTest()

    def on_pause(self):
        return True


if __name__ == '__main__':
    AccelerometerTestApp().run()
