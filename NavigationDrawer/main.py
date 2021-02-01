from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from gyro import AndroidGyroscope
from linaccel import AndroidLinearAccelerometer
from kivy.clock import Clock
from jnius import autoclass
import datetime
import os
from android.permissions import request_permissions, Permission
from kivy.garden.graph import Graph, LinePlot
from kivymd.app import MDApp
from accelerometer import AndroidAccelerometer
import track
import matplot_plot
import csv
from kivy.core.window import Window


recorded_track = False     #global bool value used in update_track function to detect if a track was recorded previously
path = ""                  #global variable used to get the path of the on the DataScreen Selected File to the TrackScreen
selected_track = False     #global bool value used in update_track function to detect if a track was selected previously
sdpath = ""                #global variable for default path

class MenuScreen(Screen):
    pass

class MeasureScreen(Screen):
    def __init__(self, **kwargs):
        """schedules init function to make sure the widget tree is loaded correctly and its ids are available. Also
        permissions to read and write from the devices storage"""
        super(MeasureScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.init)
        self.disp_plot = False
        self.started_measurement = False
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def init(self, t):
        """The actual init function for this screen. Both graph plots are instantiated from the corresponding ids in the
         kv file and three LinePlots with different colors are added to each. Also the default path to save data is saved
         and if the folders needed for saving the apps data are not existent already they are created."""
        self.acc_graph = self.ids.graph_plot
        self.rot_graph = self.ids.gyro_plot

        # For all X, Y and Z axes
        self.acc_plot = []
        self.acc_plot.append(LinePlot(color=[0, 1, 0, 1], line_width=3))  # X - Green
        self.acc_plot.append(LinePlot(color=[0, 0, 1, 1], line_width=3))  # Y - Blue
        self.acc_plot.append(LinePlot(color=[1, 0, 0, 1], line_width=3))  # Z - Red
        self.rot_plot = []
        self.rot_plot.append(LinePlot(color=[0, 1, 0, 1], line_width=3))  # X - Green
        self.rot_plot.append(LinePlot(color=[0, 0, 1, 1], line_width=3))  # Y - Blue
        self.rot_plot.append(LinePlot(color=[1, 0, 0, 1], line_width=3))  # Z - Red
        global sdpath
        try:
            Environment = autoclass("android.os.Environment")
            sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
        except:
            sdpath = MDApp.get_running_app().user_data_dir
        if not os.path.exists(os.path.join(sdpath, "Acc360Track/Data")):
            os.mkdir(os.path.join(sdpath, "Acc360Track/Data"))
        if not os.path.exists(os.path.join(sdpath, "Acc360Track/Data/without_g_compensation")):
            os.mkdir(os.path.join(sdpath, "Acc360Track/Data/without_g_compensation"))
        if not os.path.exists(os.path.join(sdpath, "Acc360Track/Data/with_g_compensation")):
            os.mkdir(os.path.join(sdpath, "Acc360Track/Data/with_g_compensation"))
        self.compensated_path = sdpath + "/Acc360Track/Data/with_g_compensation/"
        self.sdpath = sdpath + "/Acc360Track/Data/without_g_compensation/"

        self.reset_plots()
        for plot in self.acc_plot:
            self.acc_graph.add_plot(plot)
        for plot in self.rot_plot:
            self.rot_graph.add_plot(plot)

        self.counter = 1

    def reset_plots(self):
        """function used to reset the acceleration and gyration plots"""
        for plot in self.acc_plot:
            plot.points = [(0, 0)]
        for plot in self.rot_plot:
            plot.points = [(0, 0)]

    def init_measurement(self):
        """"function called at start of each measurement. If the user has specified some offset values on the SettingScreen
        those are saved in local variable for later use. Empty Lists for each sensor value are created. Depending on
        whether the g_compensation checkbox is activated the right acceleration sensor type is instantiated. Gyroscope
        is also instantiated."""
        self.linoffset = False
        self.rotoffset = False
        if self.manager.screens[3].ids["offset_lin"].active:
            self.linoffset = True
            if self.manager.screens[3].ids["x_linoff"].text:
                self.x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].text)
            else:
                self.x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].hint_text)
            if self.manager.screens[3].ids["y_linoff"].text:
                self.y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].text)
            else:
                self.y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].hint_text)
            if self.manager.screens[3].ids["z_linoff"].text:
                self.z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].text)
            else:
                self.z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].hint_text)
        if self.manager.screens[3].ids["offset_rot"].active:
            self.rotoffset = True
            if self.manager.screens[3].ids["x_rotoff"].text:
                self.x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].text)
            else:
                self.x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].hint_text)
            if self.manager.screens[3].ids["y_rotoff"].text:
                self.y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                self.y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].hint_text)
            if self.manager.screens[3].ids["y_rotoff"].text:
                self.z_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                self.z_offset_rot = float(self.manager.screens[3].ids["z_rotoff"].hint_text)
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
        """"Function called when start button is pressed. If theres already a measurement in progress nothing happens.
        If not the correct widgets for live data plots are shown and the init_measurement function is called.
        Also the start_measurement function is called. If a delay is specified and the corresponding switch is set on
        the SettingScreen the function gets called with this delay"""
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

            global recorded_track, selected_track
            recorded_track = False
            selected_track = False

    def start_measurement(self, t):
        """Function to start the actual measurement. If a value for the duration of the measurement is set on the
        SettingScreen the stop_mesaurement_duration function is scheduled to be called after this time. Both, acceleration and
        gyroscope sensors are enabled and the lists used to save the sensor values are cleared, to get rid of values from
        previous measurements. Also the reset_plots funtion is called. A Clock function is scheduled, to call the
        get_sensordata cyclically with the on the SettingScreen defined sampling rate. If none is defined the default
        value is used"""
        if self.manager.screens[3].ids["duration"].active:
            Clock.schedule_once(self.stop_measurement_duration,
                                float(self.manager.screens[3].ids["duration_value"].text))
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
        if self.manager.screens[3].ids["sampling_value"].text:
            self.samplingrate = float(self.manager.screens[3].ids["sampling_value"].text)
            Clock.schedule_interval(self.get_sensordata, 1 / self.samplingrate)
        else:
            self.samplingrate = 20
            Clock.schedule_interval(self.get_sensordata, 1 / self.samplingrate)

    def stop_measurement_duration(self, t):
        """Calls stop_measurement function after a specified time."""
        self.stop_measurement()

    def stop_measurement(self):
        """"Function called after pressing the stop button. If no measurement was done before nothing happens. Else
        The for the measurement used sensors are disabled and the get_sensordata function is unscheduled.
        If a measurement with g-compensation was performed, the acceleration and gyroscope plots are hidden and the
        track is calculated from the recorded values. To display this track a new Plot3D widget is instantiated, which
        gets added to the current screen layout."""
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
            global recorded_track
            recorded_track = True

    def save_data(self):
        """"Saves recorded sensordata to a .csv file named with date and current time. Different folders are used for
        compensated and non-compensated data."""
        if recorded_track:
            time = datetime.datetime.now()
            time = time.strftime("%Y%m%d_%H%M%S")
            if self.compensation:
                f = open(self.compensated_path + time + ".csv", "w+")
            else:
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
        """Function to read sensor data from the Android system. Therefore the current values are saved and appended
        to the corresponding list. If offset values are specified those are subtracted from the measured values before
        they are saved. To display the sensor data the values are also added to both plots. To make sure that all values
        can be displayed theres a counter which deletes the oldest value from the plot and displays the newest when 100
        values are reached."""
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

        if (not lin == (None, None, None) and (not gyro == (None, None, None))):
            if self.linoffset:
                self.x_acceleration.append(lin[0] - self.x_offset_lin)
                self.y_acceleration.append(lin[1] - self.y_offset_lin)
                self.z_acceleration.append(lin[2] - self.z_offset_lin)
                self.acc_plot[0].points.append((self.counter, lin[0] - self.x_offset_lin))
                self.acc_plot[1].points.append((self.counter, lin[1] - self.y_offset_lin))
                self.acc_plot[2].points.append((self.counter, lin[2] - self.z_offset_lin))
            else:
                self.x_acceleration.append(lin[0])
                self.y_acceleration.append(lin[1])
                self.z_acceleration.append(lin[2])
                self.acc_plot[0].points.append((self.counter, lin[0]))
                self.acc_plot[1].points.append((self.counter, lin[1]))
                self.acc_plot[2].points.append((self.counter, lin[2]))
            if self.rotoffset:
                self.x_rotation.append(gyro[0] - self.x_offset_rot)
                self.y_rotation.append(gyro[1] - self.y_offset_rot)
                self.z_rotation.append(gyro[2] - self.z_offset_rot)
                self.rot_plot[0].points.append((self.counter, gyro[0] - self.x_offset_rot))
                self.rot_plot[1].points.append((self.counter, gyro[1] - self.y_offset_rot))
                self.rot_plot[2].points.append((self.counter, gyro[2] - self.z_offset_rot))
            else:
                self.x_rotation.append(gyro[0])
                self.y_rotation.append(gyro[1])
                self.z_rotation.append(gyro[2])
                self.rot_plot[0].points.append((self.counter, gyro[0]))
                self.rot_plot[1].points.append((self.counter, gyro[1]))
                self.rot_plot[2].points.append((self.counter, gyro[2]))

        self.counter += 1

    def update_track(self):
        """This function is called when the Update track button on the SettingScreen is pressed and previously a
        track was recorded. The old widget is removed and a new track is calculated with the changed offset values
        which gets shown afterwards."""
        self.manager.screens[1].ids.measurement_layout.remove_widget(self.plot)
        if self.manager.screens[3].ids["offset_lin"].active:
            self.linoffset = True
            if self.manager.screens[3].ids["x_linoff"].text:
                x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].text)
            else:
                x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].hint_text)
            if self.manager.screens[3].ids["y_linoff"].text:
                y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].text)
            else:
                y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].hint_text)
            if self.manager.screens[3].ids["z_linoff"].text:
                z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].text)
            else:
                z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].hint_text)
        else:
            x_offset_lin = 0
            y_offset_lin = 0
            z_offset_lin = 0
        if self.manager.screens[3].ids["offset_rot"].active:
            self.rotoffset = True
            if self.manager.screens[3].ids["x_rotoff"].text:
                x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].text)
            else:
                x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].hint_text)
            if self.manager.screens[3].ids["y_rotoff"].text:
                y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].hint_text)
            if self.manager.screens[3].ids["y_rotoff"].text:
                z_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                z_offset_rot = float(self.manager.screens[3].ids["z_rotoff"].hint_text)
        else:
            x_offset_rot = 0
            y_offset_rot = 0
            z_offset_rot = 0
        pos_x, pos_y, pos_z = track.calculate_track(x_accel=self.x_acceleration, y_accel=self.y_acceleration,
                                                    z_accel=self.z_acceleration, x_rotat=self.x_rotation,
                                                    y_rotat=self.y_rotation, z_rotat=self.z_rotation,
                                                    x_acc_off=x_offset_lin, y_acc_off=y_offset_lin,
                                                    z_acc_off=z_offset_lin, x_rot_off=x_offset_rot,
                                                    y_rot_off=y_offset_rot,
                                                    z_rot_off=z_offset_rot)
        self.plot = matplot_plot.Plot3D()
        self.plot.size_hint_y = 0.8
        self.plot.pos_hint = {"center_x:": 0.5, "center_y": 0.53}
        self.manager.screens[1].ids.measurement_layout.add_widget(self.plot)
        self.plot.plot(pos_x, pos_y, pos_z)


class DataScreen(Screen):
    def __init__(self, **kwargs):
        """init function for DataScreen. Path to g-compensated files is set and a FileChooserIconView Widget is instantiated
        and added to the layout."""
        super(DataScreen, self).__init__(**kwargs)
        self.sdpath = sdpath + "/Acc360Track/Data/with_g_compensation/"
        self.viewer = FileChooserIconView()
        self.viewer.pos_hint = {"center_x": 0.5, "center_y": 0.55}
        self.viewer.size_hint = (1, 0.8)
        self.viewer.id = "filechooser"
        self.viewer.path = self.sdpath
        if self.init_widget():
            self.add_widget(self.viewer)

    def on_enter(self):
        """Function called everytime the user switches to this screen. Files are updated to make sure all recorded tracks
        are displayed"""
        self.viewer.path = self.sdpath
        self.viewer._update_files()

    def init_widget(self, *args):
        """Function to make sure each entry in the FileChooser is displayed as wanted. Therefore update_file_list_entry
        is called for every file"""
        fc = self.viewer
        fc.bind(on_entry_added=self.update_file_list_entry)
        fc.bind(on_subentry_to_entry=self.update_file_list_entry)
        return True

    def update_file_list_entry(self, file_chooser, file_list_entry, *args):
        """function to customize the look of FileChooserIconView Widget. As the default text color is white this needs
        to be changed for each file. Also each elements size is adjusted. For customization options see
        https://github.com/kivy/kivy/blob/master/kivy/data/style.kv"""
        file_list_entry.children[0].color = (0.0, 0.0, 0.0, 1.0)  # File Names
        file_list_entry.children[1].color = (0.0, 0.0, 0.0, 1.0)  # Dir Names`
        file_list_entry.children[1].font_size = ("14sp")
        file_list_entry.children[1].shorten = False
        file_list_entry.children[1].size = ("100dp", "40sp")

    def restore_track(self):
        """Function called when the Restore track button is pressed. If a file is selected The restore_track function
        on TrackScreen is called to display the track."""
        if self.viewer.selection:
            global path
            path = self.viewer.selection[0]
            self.manager.screens[4].restore_track()
            global selected_track
            selected_track = True


class SettingScreen(Screen):
    """Screen to adjust settings like samplingrate, delay, duration and offsets. Most of the settings will
        be done in the *.kv file, here we just change the calibration values at the hint text parameter of the text input."""
    def __init__(self, **kwargs):
        super(SettingScreen, self).__init__(**kwargs)

    def on_enter(self):
        """If the user enters the settings page, the actual calibration data will be loaded as hint text into the
        offset textfields. """
        self.sdpath = sdpath + "/Acc360Track/Calibration/"
        try:
            if self.manager.screens[1].ids["g_compensation"].active:
                self.sdpath += "Offset_gCompensation.csv"
            else:
                self.sdpath += "Offset.csv"
            with open(self.sdpath, "r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.manager.screens[3].ids["x_linoff"].hint_text = row[0][:10]
                    self.manager.screens[3].ids["y_linoff"].hint_text = row[1][:10]
                    self.manager.screens[3].ids["z_linoff"].hint_text = row[2][:10]
                    self.manager.screens[3].ids["x_rotoff"].hint_text = row[3][:10]
                    self.manager.screens[3].ids["y_rotoff"].hint_text = row[4][:10]
                    self.manager.screens[3].ids["z_rotoff"].hint_text = row[5][:10]
        except OSError:
            pass

    def update_track(self):
        """Depending on the user navigation, from where he wanted to upgrade the track, the screen manager navigates
        back to the right screen"""
        if selected_track:
            self.manager.screens[4].update_track()
            self.manager.current = "track"
        elif recorded_track:
            self.manager.screens[1].update_track()
            self.manager.current = "measure"


class TrackScreen(Screen):
    """The Track Screen shows the measured values plotted as an 3D plot."""
    def __init__(self, **kwargs):
        super(TrackScreen, self).__init__(**kwargs)

    def restore_track(self):
        """from the stored position values, we can calculte a matplot 3D track by adding a plot widget"""
        pos_x, pos_y, pos_z = track.calculate_track(path=path)
        self.plot = matplot_plot.Plot3D()
        self.add_widget(self.plot)
        self.plot.plot(pos_x, pos_y, pos_z)

    def update_track(self):
        """update an already stored track with customized offset values.
            If the linear offset switch of settings screen is active, it takes the text of the particular textfield
            or if the text is empty, it takes the hint text (calibration values). If the linear offset switch is inactive
            then there will be written zeros instead. Same for Gyration offset.
            After that the track will be plotted with updated values."""
        if self.manager.screens[3].ids["offset_lin"].active:
            self.linoffset = True
            if self.manager.screens[3].ids["x_linoff"].text:
                x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].text)
            else:
                x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].hint_text)
            if self.manager.screens[3].ids["y_linoff"].text:
                y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].text)
            else:
                y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].hint_text)
            if self.manager.screens[3].ids["z_linoff"].text:
                z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].text)
            else:
                z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].hint_text)
        else:
            x_offset_lin = 0
            y_offset_lin = 0
            z_offset_lin = 0
        if self.manager.screens[3].ids["offset_rot"].active:
            self.rotoffset = True
            if self.manager.screens[3].ids["x_rotoff"].text:
                x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].text)
            else:
                x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].hint_text)
            if self.manager.screens[3].ids["y_rotoff"].text:
                y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].hint_text)
            if self.manager.screens[3].ids["y_rotoff"].text:
                z_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            else:
                z_offset_rot = float(self.manager.screens[3].ids["z_rotoff"].hint_text)
        else:
            x_offset_rot = 0
            y_offset_rot = 0
            z_offset_rot = 0
        pos_x, pos_y, pos_z = track.calculate_track(path=path, x_acc_off=x_offset_lin, y_acc_off=y_offset_lin,
                                                    z_acc_off=z_offset_lin, x_rot_off=x_offset_rot,
                                                    y_rot_off=y_offset_rot,
                                                    z_rot_off=z_offset_rot)
        self.plot.plot(pos_x, pos_y, pos_z)


class CalibrationScreen(Screen):
    """Calibration screen: calibrate the sensors of the smartphone and automatically adjust the offset settings"""
    def __init__(self, **kwargs):
        super(CalibrationScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.onBackBtn)

    def calibrate(self):
        """If the g_compensation checkbox ist active (default: active), the AndroidLinearAccelerometer fct. is called,
        otherwise the AndroidAccelerometer fct. is called. After presssing start calibration, the 10 sec calibration
        starts after a delay of 2 sec. The label text also changes dynamically."""
        self.gyroscope = AndroidGyroscope()
        if self.manager.screens[5].ids["g_compensation_calibration"].active:
            self.linear = True
            self.accelerometer = AndroidLinearAccelerometer()
        else:
            self.accelerometer = AndroidAccelerometer()
            self.linear = False
        Clock.schedule_once(self.start_calibration, 2)
        Clock.schedule_once(self.stop_calibration, 12)
        self.time = 10
        Clock.schedule_interval(self.disp_time, 1)
        self.manager.screens[5].ids["calibration_text"].text = "Calibration started.\nPlease dont move the device!"
        self.manager.screens[5].ids["calibration_button"].disabled = True
        self.x_rotation = []
        self.y_rotation = []
        self.z_rotation = []
        self.x_acceleration = []
        self.y_acceleration = []
        self.z_acceleration = []
        self.gyroscope.enable()
        self.accelerometer.enable()

    def start_calibration(self, t):
        """default samplingrate of calibration"""
        Clock.schedule_interval(self.start_measurement, 1 / 20)

    def start_measurement(self, t):
        """start the calibration
        record the measured values of gyroscop and linear Accelerometer"""
        gyro = self.gyroscope.get_rotation()
        lin = self.accelerometer.get_acceleration()

        if (not lin == (None, None, None) and (not gyro == (None, None, None))):
            self.x_acceleration.append(lin[0])
            self.y_acceleration.append(lin[1])
            self.z_acceleration.append(lin[2])
            self.x_rotation.append(gyro[0])
            self.y_rotation.append(gyro[1])
            self.z_rotation.append(gyro[2])

    def stop_calibration(self, t):
        """if the the calibration Counter = 0, stop recording values and unschedule the display countdown
        Without g Compensation, substract 9.81 in z direction
        Safe the calibrated values in the right folder (create them at the first start of the app)
        return back to the menu
        """
        Clock.unschedule(self.disp_time)
        Clock.unschedule(self.start_measurement)
        x_acc_off = sum(self.x_acceleration) / len(self.x_acceleration)
        y_acc_off = sum(self.y_acceleration) / len(self.y_acceleration)
        z_acc_off = sum(self.z_acceleration) / len(self.z_acceleration)
        x_rot_off = sum(self.x_rotation) / len(self.x_rotation)
        y_rot_off = sum(self.y_rotation) / len(self.y_rotation)
        z_rot_off = sum(self.z_rotation) / len(self.z_rotation)

        if not self.linear:
            z_acc_off -= 9.81
        if not os.path.exists(os.path.join(sdpath, "Acc360Track/Calibration")):
            os.mkdir(os.path.join(sdpath, "Acc360Track/Calibration"))
        self.sdpath = sdpath + "/Acc360Track/Calibration/"
        if self.linear:
            f = open(self.sdpath + "Offset_gCompensation.csv", "w+")
        else:
            f = open(self.sdpath + "Offset.csv", "w+")
        f.write("x_acc_offset,y_acc_offset,z_acc_offset,x_rot_offset,y_rot_offset,z_rot_offset\n")
        f.write(str(x_acc_off) + "," + str(y_acc_off) + "," + str(z_acc_off) + "," + str(x_rot_off)
                + "," + str(y_rot_off) + "," + str(z_rot_off))
        f.close()
        self.manager.current = "menu"
        self.manager.screens[5].ids["calibration_button"].disabled = False
        self.manager.screens[5].ids["calibration_button"].text = "Start Calibration"
        self.manager.screens[5].ids[
            "calibration_text"].text = "Place your device on a flat surface and press the Start-button to begin with the calibration!"

    def disp_time(self, t):
        """Countdown for Calibration Mode"""
        self.manager.screens[5].ids["calibration_button"].text = str(self.time)
        self.time -= 1

    def onBackBtn(self, window, keycode1, *largs):
        """back key on smartphone, reserved with "ESC", we use it as a back key"""
        if keycode1 == 27:
            self.manager.direction = "right"
            self.manager.current = "menu"
            return True
        return False


class AboutScreen(Screen):
    pass


class HelpScreen(Screen):
    pass


class ContentNavigationDrawer(BoxLayout):
    pass


class Screenmanagement(ScreenManager):
    pass


class AccTrack(MDApp):
    """Builds the App, returns the root widget Screenmanagment with the different screens"""
    def build(self):
        return Screenmanagement()


if __name__ == "__main__":
    AccTrack().run()
