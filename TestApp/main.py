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
from kivy.garden.graph import MeshLinePlot
import datetime
import os
from Plot.plot import Plot3D
import threading
from queue import Queue
import time

import matplotlib
matplotlib.use('module://garden_matplotlib.backend_kivy')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class AccelerometerTest(BoxLayout):
    def __init__(self, **kwargs):
        super(AccelerometerTest, self).__init__(**kwargs)
        self.sensorEnabled = False
        self.linaccelEnabled = False
        self.graph = self.ids.graph_plot

        # For all X, Y and Z axes
        self.plot = []
        self.plot.append(MeshLinePlot(color=[1, 0, 0, 1]))  # X - Red
        self.plot.append(MeshLinePlot(color=[0, 1, 0, 1]))  # Y - Green
        self.plot.append(MeshLinePlot(color=[0, 0, 1, 1]))  # Z - Blue

        self.reset_plots()
        #self.plot3D = Plot3D()
        #self.ids.matplotlib_plot.add_widget(self.plot3D)
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection="3d")
        self.ax.plot([], [], [])
        self.mpl_canvas = self.fig.canvas
        self.ids.matplotlib_plot.add_widget(self.mpl_canvas)


        #self.q_data = Queue()
        #self.q_bool = Queue()

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

        for plot in self.plot:
            self.graph.add_plot(plot)
            
    def reset_plots(self):
        for plot in self.plot:
            plot.points = [(0, 0)]

        self.counter = 1
        
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
                self.ax.clear()
                #self.q_data.queue.clear()
                #self.q_bool.queue.clear()
                self.linaccelEnabled = True
                #self.q_bool.put(self.linaccelEnabled)
                Clock.schedule_interval(self.get_linearacceleration, 1 / 20.)
                Clock.schedule_interval(self.plotfunc, 1)
                #self.thread = threading.Thread(target=self.readsensorvalues, args=(self.q_data, self.q_bool,))
                #self.thread.start()

                self.ids.toggle_button2.text = "Stop Linear Accelerometer"
            else:
                self.gyro.disable()
                self.acc.disable()
                #self.plot3D.plot(self.x_accel, self.y_accel, self.z_accel)
                Clock.unschedule(self.get_linearacceleration)
                Clock.unschedule(self.plot)
                self.linaccelEnabled = False
                #self.q_bool.put(self.linaccelEnabled)
                self.ids.toggle_button2.text = "Start Linear Accelerometer"
                #self.thread.join()
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
        if (self.counter == 100):
            for plot in self.plot:
                del (plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]

            self.counter = 99

        gyro = self.gyro.get_rotation()
        lin = self.acc.get_linearacceleration()

        if (not lin == (None, None, None)):
            self.plot[0].points.append((self.counter, lin[0]))
            self.x_ro.append(gyro[0])
            self.x_accel.append(lin[0])
            self.plot[1].points.append((self.counter, lin[1]))
            self.y_ro.append(gyro[1])
            self.y_accel.append(lin[1])
            self.plot[2].points.append((self.counter, lin[2]))
            self.z_ro.append(gyro[2])
            self.z_accel.append(lin[2])

        self.counter += 1


    def plotfunc(self, t):
        #self.plot3D.plot(self.x_accel, self.y_accel, self.z_accel)
        self.ax.plot(self.x_accel, self.y_accel, self.z_accel)
        self.mpl_canvas.draw()

    def get_acceleration(self, dt):
        if (self.counter == 100):
            for plot in self.plot:
                del(plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]

            self.counter = 99

        accel = accelerometer.acceleration
        gyro = self.gyro.get_rotation()

        if(not accel == (None, None, None)):
            self.plot[0].points.append((self.counter, accel[0]))
            self.x_ro.append(gyro[0])
            self.x_accel.append(accel[0])
            self.plot[1].points.append((self.counter, accel[1]))
            self.y_ro.append(gyro[1])
            self.y_accel.append(accel[1])
            self.plot[2].points.append((self.counter, accel[2]))
            self.z_ro.append(gyro[2])
            self.z_accel.append(accel[2])

        self.counter += 1


    # def readsensorvalues(self, q_data, q_bool):
    #     accelerometer = AndroidLinearAccelerometer()
    #     gyroscope = AndroidGyroscope()
    #     accelerometer.enable()
    #     gyroscope.enable()
    #     x_acceleration = []
    #     x_gyro = []
    #     y_acceleration = []
    #     y_gyro = []
    #     z_acceleration = []
    #     z_gyro = []
    #     bool = True
    #     while bool:
    #         gyro = gyroscope.get_rotation()
    #         lin = accelerometer.get_linearacceleration()
    #         if (not lin == (None, None, None)):
    #             x_gyro.append(gyro[0])
    #             x_acceleration.append(lin[0])
    #             y_gyro.append(gyro[1])
    #             y_acceleration.append(lin[1])
    #             z_gyro.append(gyro[2])
    #             z_acceleration.append(lin[2])
    #             q_data.put((x_acceleration, y_acceleration, z_acceleration, x_gyro, y_gyro, z_gyro))
    #         if not q_bool.empty():
    #             bool = q_bool.get()
    #             q_bool.task_done()
    #         time.sleep(1/50)
    #     if not bool:
    #         accelerometer.disable()
    #         gyroscope.disable()



class AccelerometerTestApp(App):
    def build(self):
        return AccelerometerTest()

    def on_pause(self):
        return True


if __name__ == '__main__':
    AccelerometerTestApp().run()

