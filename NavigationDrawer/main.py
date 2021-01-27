from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.text import markup
from gyro import AndroidGyroscope
from linaccel import AndroidLinearAccelerometer
from kivy.clock import Clock
from jnius import autoclass
import datetime
import os
from android.permissions import request_permissions, Permission
from kivy.garden.graph import Graph, MeshLinePlot
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from accelerometer import AndroidAccelerometer
import track
import matplotlib
matplotlib.use('module://garden_matplotlib.backend_kivy')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplot_plot
from kivy.properties import ObjectProperty


class MenuScreen(Screen):
    pass


class MeasureScreen(Screen):
    def __init__(self, **kwargs):
        super(MeasureScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.init)
        self.disp_plot = False
        self.started_measurement = False

    def init(self, t):
        self.acc_graph = self.ids.graph_plot
        self.rot_graph = self.ids.gyro_plot

        # For all X, Y and Z axes
        self.acc_plot = []
        self.acc_plot.append(MeshLinePlot(color=[1, 0, 0, 1]))  # X - Red
        self.acc_plot.append(MeshLinePlot(color=[0, 1, 0, 1]))  # Y - Green
        self.acc_plot.append(MeshLinePlot(color=[0, 0, 1, 1]))  # Z - Blue
        self.rot_plot = []
        self.rot_plot.append(MeshLinePlot(color=[1, 0, 0, 1]))  # X - Red
        self.rot_plot.append(MeshLinePlot(color=[0, 1, 0, 1]))  # Y - Green
        self.rot_plot.append(MeshLinePlot(color=[0, 0, 1, 1]))  # Z - Blue

        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        try:
            Environment = autoclass("android.os.Environment")
            self.sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
        except:
            self.sdpath = MDApp.get_running_app().user_data_dir
        if not os.path.exists(os.path.join(self.sdpath, "Acc360Track")):
            os.mkdir(os.path.join(self.sdpath, "Acc360Track"))
        self.sdpath += "/Acc360Track/"
        self.reset_plots()
        for plot in self.acc_plot:
            self.acc_graph.add_plot(plot)
        for plot in self.rot_plot:
            self.rot_graph.add_plot(plot)

        self.counter = 1

    def reset_plots(self):
        for plot in self.acc_plot:
            plot.points = [(0, 0)]
        for plot in self.rot_plot:
            plot.points = [(0, 0)]


    def init_measurement(self):
        """"Request Permissions to write, set path to save files, instantiate sensors and
            create empty lists to save sensor values"""
        self.linoffset = False
        self.rotoffset = False
        if self.manager.screens[3].ids["offset_lin"].active:
            self.linoffset = True
            if self.manager.screens[3].ids["x_linoff"].text:
                self.x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].text)
            else:
                self.x_offset_lin = 0
            if self.manager.screens[3].ids["y_linoff"].text:
                self.y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].text)
            else:
                self.y_offset_lin = 0
            if self.manager.screens[3].ids["z_linoff"].text:
                self.z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].text)
            else:
                self.z_offset_lin = 0
        if self.manager.screens[3].ids["offset_rot"].active:
            self.rotoffset = True
            if self.manager.screens[3].ids["x_rotoff"].text:
                self.x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].text)
            else:
                self.x_offset_rot = 0
            if self.manager.screens[3].ids["y_rotoff"].text:
                self.y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                self.y_offset_rot = 0
            if self.manager.screens[3].ids["y_rotoff"].text:
                self.z_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                self.z_offset_rot = 0
        self.x_rotation = []
        self.y_rotation = []
        self.z_rotation = []
        self.x_acceleration = []
        self.y_acceleration = []
        self.z_acceleration = []
        if self.manager.screens[1].ids["g_compensation"].active:
            self.accelerometer = AndroidLinearAccelerometer()
            self.compensation = True
        else:
            self.accelerometer = AndroidAccelerometer()
            self.compensation = False
        self.gyroscope = AndroidGyroscope()

    def start_button(self):
        """"Start measurement. Calls init_measurement function and enables the sensors.
            Lists to save values are being cleared and a timer to read the sensor data gets started"""
        if not self.started_measurement:
            if self.disp_plot:
                self.manager.screens[1].ids.measurement_layout.remove_widget(self.plot)
                self.manager.screens[1].ids["graph_plot"].size_hint = (1, 0.4)
                self.manager.screens[1].ids["graph_plot"].ylabel = "value"
                self.manager.screens[1].ids["gyro_plot"].size_hint = (1, 0.4)
                self.manager.screens[1].ids["gyro_plot"].ylabel = "value"
                self.manager.screens[1].ids["rot_label"].color = (0, 0, 0, 0.15)
                self.manager.screens[1].ids["acc_label"].color = (0, 0, 0, 0.15)
                self.manager.screens[1].ids["legend"].color = (0, 0, 0, 0.8)
            self.init_measurement()
            if self.manager.screens[3].ids["delay"].active:
                Clock.schedule_once(self.start_measurement,
                                    float(self.manager.screens[3].ids["delay_value"].text))
            else:
                self.start_measurement(t=0)
            self.started_measurement = True

    def start_measurement(self, t):
        if self.manager.screens[3].ids["duration"].active:
            Clock.schedule_once(self.stop_measurement_duration,
                                float(self.manager.screens[3].ids["duration_value"].text))
        self.gyroscope.enable()
        self.accelerometer.enable()
        self.gyroscope.enable()
        self.accelerometer.enable()
        self.x_acceleration.clear()
        self.y_acceleration.clear()
        self.z_acceleration.clear()
        self.x_rotation.clear()
        self.y_rotation.clear()
        self.z_rotation.clear()
        self.counter = 1
        self.reset_plots()
        if self.manager.screens[3].ids["samplingrate"].active:
            self.samplingrate = float(self.manager.screens[3].ids["sampling_value"].text)
            Clock.schedule_interval(self.get_sensordata, 1 / self.samplingrate)
        else:
            self.samplingrate = 20
            Clock.schedule_interval(self.get_sensordata, 1 / self.samplingrate)

    def stop_measurement_duration(self, t):
        self.gyroscope.disable()
        self.accelerometer.disable()
        Clock.unschedule(self.get_sensordata)

    def stop_measurement(self):
        """"Disable Sensors and unschedule get_sensordata function"""
        if self.started_measurement:
            self.gyroscope.disable()
            self.accelerometer.disable()
            Clock.unschedule(self.get_sensordata)
            if self.compensation:
                self.manager.screens[1].ids["graph_plot"].size_hint = (0, 0)
                self.manager.screens[1].ids["graph_plot"].ylabel = " "
                self.manager.screens[1].ids["gyro_plot"].size_hint = (0, 0)
                self.manager.screens[1].ids["gyro_plot"].ylabel = " "
                self.manager.screens[1].ids["rot_label"].color = (0, 0, 0, 0)
                self.manager.screens[1].ids["acc_label"].color = (0, 0, 0, 0)
                self.manager.screens[1].ids["legend"].color = (0, 0, 0, 0)
                x_pos, y_pos, z_pos = track.calculate_track(x_accel=self.x_acceleration, y_accel=self.y_acceleration,
                                                            z_accel=self.z_acceleration, x_rotat=self.x_rotation,
                                                            y_rotat=self.y_rotation, z_rotat=self.z_rotation)

                self.plot = matplot_plot.Plot3D()
                self.plot.pos_hint = {"center_x:": 0.5, "center_y": 0.53}
                self.plot.size_hint_y = 0.8
                self.manager.screens[1].ids.measurement_layout.add_widget(self.plot)
                self.plot.plot(x_pos, y_pos, z_pos)
                self.disp_plot = True
            else:
                self.disp_plot = False
            self.started_measurement = False

    def save_data(self):
        """"Saves recorded sensordata to a .csv file named with date and current time"""
        time = datetime.datetime.now()
        time = time.strftime("%Y%m%d_%H%M%S")
        f = open(self.sdpath + time + ".csv", "w+")
        f.write("t[s],ax[m/s2],ay[m/s2],az[m/s2],\u03C9x[rad/s],\u03C9y[rad/s],\u03C9z[rad/s]\n")
        t = 0
        for i in range(len(self.x_acceleration)):
            f.write(str(t) + "," + str(self.x_acceleration[i]) + "," + str(self.y_acceleration[i]) + "," + str(
                self.z_acceleration[i]) + "," + str(self.x_rotation[i])
                    + "," + str(self.y_rotation[i]) + "," + str(self.z_rotation[i]))
            f.write("\n")
            t += 1 / self.samplingrate

        f.close()

    def get_sensordata(self, t):
        """Reads sensordata and appends them to the corresponding list every time the function gets called"""
        if (self.counter == 100):
            for plot in self.acc_plot:
                del (plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]
            for plot in self.rot_plot:
                del (plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]
            self.counter = 99

        gyro = self.gyroscope.get_rotation()
        lin = self.accelerometer.get_acceleration()


        if (not lin == (None, None, None) and (not gyro ==(None, None, None))):
            if self.linoffset:
                self.x_acceleration.append(lin[0] + self.x_offset_lin)
                self.y_acceleration.append(lin[1] + self.y_offset_lin)
                self.z_acceleration.append(lin[2] + self.z_offset_lin)
                self.acc_plot[0].points.append((self.counter, lin[0] + self.x_offset_lin))
                self.acc_plot[1].points.append((self.counter, lin[1] + self.y_offset_lin))
                self.acc_plot[2].points.append((self.counter, lin[2] + self.z_offset_lin))
            else:
                self.x_acceleration.append(lin[0])
                self.y_acceleration.append(lin[1])
                self.z_acceleration.append(lin[2])
                self.acc_plot[0].points.append((self.counter, lin[0]))
                self.acc_plot[1].points.append((self.counter, lin[1]))
                self.acc_plot[2].points.append((self.counter, lin[2]))
            if self.rotoffset:
                self.x_rotation.append(gyro[0] + self.x_offset_rot)
                self.y_rotation.append(gyro[1] + self.y_offset_rot)
                self.z_rotation.append(gyro[2] + self.z_offset_rot)
                self.rot_plot[0].points.append((self.counter, gyro[0] + self.x_offset_rot))
                self.rot_plot[1].points.append((self.counter, gyro[1] + self.y_offset_rot))
                self.rot_plot[2].points.append((self.counter, gyro[2] + self.z_offset_rot))
            else:
                self.x_rotation.append(gyro[0])
                self.y_rotation.append(gyro[1])
                self.z_rotation.append(gyro[2])
                self.rot_plot[0].points.append((self.counter, gyro[0]))
                self.rot_plot[1].points.append((self.counter, gyro[1]))
                self.rot_plot[2].points.append((self.counter, gyro[2]))

        self.counter += 1


path = ""
class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)
        try:
            Environment = autoclass("android.os.Environment")
            self.sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
        except:
            self.sdpath = MDApp.get_running_app().user_data_dir
        self.sdpath += "/Acc360Track/"
        self.viewer = FileChooserIconView(id="filechooser")
        self.viewer.path = self.sdpath
        if self.init_widget():
            self.add_widget(self.viewer)



    def init_widget(self, *args):
        fc = self.viewer
        fc.bind(on_entry_added=self.update_file_list_entry)
        fc.bind(on_subentry_to_entry=self.update_file_list_entry)
        return True

    def update_file_list_entry(self, file_chooser, file_list_entry, *args):
        file_list_entry.children[0].color = (0.0, 0.0, 0.0, 1.0)  # File Names
        file_list_entry.children[1].color = (0.0, 0.0, 0.0, 1.0)  # Dir Names`
        file_list_entry.children[1].font_size = ("14sp")
        file_list_entry.children[1].shorten = False
        file_list_entry.children[1].size = ("100dp", "50sp")
        # https://github.com/kivy/kivy/blob/master/kivy/data/style.kv

    def restore_track(self):
        if self.viewer.selection:
            global path
            path = self.viewer.selection[0]



class SettingScreen(Screen):
    pass

class TrackScreen(Screen):
    def __init__(self, **kwargs):
        super(TrackScreen, self).__init__(**kwargs)

    def on_enter(self):
        pos_x, pos_y, pos_z = track.calculate_track(path=path)
        plot = matplot_plot.Plot3D()
        self.add_widget(plot)
        plot.plot(pos_x, pos_y, pos_z)
class CalibrationScreen(Screen):
    pass


class AboutScreen(Screen):
    pass


class HelpScreen(Screen):
    pass


class ContentNavigationDrawer(BoxLayout):
    nav_drawer = ObjectProperty()


class MeasurementLayout(MDBoxLayout):
    pass


class AccTrack(MDApp):
    def build(self):
        screen = Builder.load_file("acctrack.kv")
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MeasureScreen(name='measure'))
        sm.add_widget(DataScreen(name='showdata'))
        sm.add_widget(SettingScreen(name='settings'))
        sm.add_widget(TrackScreen(name='track'))
        sm.add_widget(CalibrationScreen(name='calibration'))
        sm.add_widget(AboutScreen(name='about'))
        sm.add_widget(HelpScreen(name='help'))
        return screen




if __name__ == "__main__":
    AccTrack().run()

