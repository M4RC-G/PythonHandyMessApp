from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.selectioncontrol import MDSwitch
from gyro import AndroidGyroscope
from linaccel import AndroidLinearAccelerometer
from kivy.clock import Clock
from jnius import autoclass
import datetime
import os
from android.permissions import request_permissions, Permission
from kivy.garden.graph import Graph, MeshLinePlot

screen_helper = """
ScreenManager:
    MenuScreen:
    MeasureScreen:
    DataScreen:
    OffsetScreen:
        
<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["home", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:
    MDRectangleFlatButton:
        text: '       Offset & Gain       '
        icon: 'run-fast'
        pos_hint: {'center_x':0.5, 'center_y':0.25}
        on_press:
            root.manager.current = 'offset'
            root.manager.transition.direction = "left"
    MDRectangleFlatButton:
        text: '  Show logged data   '
        icon: 'run-fast'
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        on_press:
            root.manager.current = 'showdata'
            root.manager.transition.direction = "left"
    MDRectangleFlatButton:
        text: ' Start measurement '
        icon: 'run-fast'
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        on_press: 
            root.manager.current = 'measure'
            root.manager.transition.direction = "left"
            
<MeasureScreen>:
    name: 'measure'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        
        Graph:
            size_hint_y: 0.8
            id: graph_plot
            xlabel:'Time'
            ylabel:'Value'
            y_grid_label: True
            x_grid_label: True
            padding: 5
            xmin:0
            xmax:100
            ymin:-15
            ymax:20
        
        
    MDRoundFlatIconButton:
        icon: "settings"
        text: "Offset & Gain"
        on_press: root.manager.current = 'offset'
        pos_hint: {'center_x':0.5, 'center_y':0.05}

    MDRectangleFlatButton:
        text: 'Start'
        pos_hint: {'center_x':0.2, 'center_y':0.13}
        on_press: root.start_button()
    MDRectangleFlatButton:
        text: 'Stop'
        pos_hint: {'center_x':0.5, 'center_y':0.13}
        on_press: root.stop_measurement()
    MDRectangleFlatButton:
        text: 'Save'
        pos_hint: {'center_x':0.8, 'center_y':0.13}
        on_press: root.save_data()

    MDIconButton:
        icon: "keyboard-backspace"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}
    
<DataScreen>:
    name: 'showdata'

    MDRectangleFlatButton:
        text: 'Restore Track'
        pos_hint: {'center_x':0.26, 'center_y':0.13} 
    MDRectangleFlatButton:
        text: 'Restore Values'
        pos_hint: {'center_x':0.73, 'center_y':0.13} 

    MDIconButton:
        icon: "keyboard-backspace"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}


<OffsetScreen>:
    name: 'offset'

    MDSwitch:
        id: delay
        pos_hint: {'center_x': 0.1, 'center_y': 0.95}
    MDLabel:
        text: "Delay in s"
        pos_hint: {'center_x': 0.7, 'center_y': 0.95}
    MDTextFieldRect:
        id: delay_value
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.95}

    MDSwitch:
        id: duration
        pos_hint: {'center_x': 0.1, 'center_y': 0.85}
    MDLabel:
        text: "Duration in s"
        pos_hint: {'center_x': 0.7, 'center_y': 0.85}
    MDTextFieldRect:
        id: duration_value
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.85}

    MDSwitch:
        id: offset_lin
        pos_hint: {'center_x': 0.1, 'center_y': 0.75}
    MDLabel:
        text: "Offset Linear"
        pos_hint: {'center_x': 0.7, 'center_y': 0.75}
    MDLabel:
        text: "X"
        pos_hint: {'center_x': 0.9, 'center_y': 0.7}
    MDTextFieldRect:
        id: x_linoff
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.7}
    MDLabel:
        text: "Y"
        pos_hint: {'center_x': 0.9, 'center_y': 0.6}
    MDTextFieldRect:
        id: y_linoff
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.6}
    MDLabel:
        text: "Z"
        pos_hint: {'center_x': 0.9, 'center_y': 0.5}
    MDTextFieldRect:
        id: z_linoff
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.5}

    MDSwitch:
        id: offset_rot
        pos_hint: {'center_x': 0.1, 'center_y': 0.4}
    MDLabel:
        text: "Offset Rotatorisch"
        pos_hint: {'center_x': 0.7, 'center_y': 0.4}
    MDLabel:
        text: "X"
        pos_hint: {'center_x': 0.9, 'center_y': 0.35}
    MDTextFieldRect:
        id: x_rotoff
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.35}
    MDLabel:
        text: "Y"
        pos_hint: {'center_x': 0.9, 'center_y': 0.25}
    MDTextFieldRect:
        id: y_rotoff
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.25}
    MDLabel:
        text: "Z"
        pos_hint: {'center_x': 0.9, 'center_y': 0.15}
    MDTextFieldRect:
        id: z_rotoff
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.15}

    MDIconButton:
        icon: "keyboard-backspace"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}
"""



class MenuScreen(Screen):
    pass


class MeasureScreen(Screen):
    def __init__(self, **kwargs):
        super(MeasureScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.init)

    def init(self, t):
        self.acc_graph = self.ids.graph_plot

        # For all X, Y and Z axes
        self.acc_plot = []
        self.acc_plot.append(MeshLinePlot(color=[1, 0, 0, 1]))  # X - Red
        self.acc_plot.append(MeshLinePlot(color=[0, 1, 0, 1]))  # Y - Green
        self.acc_plot.append(MeshLinePlot(color=[0, 0, 1, 1]))  # Z - Blue

        self.reset_plots()
        for plot in self.acc_plot:
            self.acc_graph.add_plot(plot)

        self.counter = 1

    def reset_plots(self):
        for plot in self.acc_plot:
            plot.points = [(0, 0)]


    def init_measurement(self):
        """"Request Permissions to write, set path to save files, instantiate sensors and
            create empty lists to save sensor values"""
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        try:
            Environment = autoclass("android.os.Environment")
            self.sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
        except:
            self.sdpath = MDApp.get_running_app().user_data_dir
        if not os.path.exists(os.path.join(self.sdpath, "AccGyroData")):
            os.mkdir(os.path.join(self.sdpath, "AccGyroData"))
        self.sdpath += "/AccGyroData"

        self.linoffset = False
        self.rotoffset = False
        if self.manager.screens[3].ids["offset_lin"].active:
            self.linoffset = True
            self.x_offset_lin = float(self.manager.screens[3].ids["x_linoff"].text)
            self.y_offset_lin = float(self.manager.screens[3].ids["y_linoff"].text)
            self.z_offset_lin = float(self.manager.screens[3].ids["z_linoff"].text)
        if self.manager.screens[3].ids["offset_rot"].active:
            self.rotoffset = True
            self.x_offset_rot = float(self.manager.screens[3].ids["x_rotoff"].text)
            self.y_offset_rot = float(self.manager.screens[3].ids["y_rotoff"].text)
            self.z_offset_rot = float(self.manager.screens[3].ids["z_rotoff"].text)

        self.x_rotation = []
        self.y_rotation = []
        self.z_rotation = []
        self.x_acceleration = []
        self.y_acceleration = []
        self.z_acceleration = []
        self.accelerometer = AndroidLinearAccelerometer()
        self.gyroscope = AndroidGyroscope()

    def start_button(self):
        """"Start measurement. Calls init_measurement function and enables the sensors.
            Lists to save values are being cleared and a timer to read the sensor data gets started"""
        self.init_measurement()
        if self.manager.screens[3].ids["delay"].active:
            Clock.schedule_once(self.start_measurement, float(self.manager.screens[3].ids["delay_value"].text))
        else:
            self.start_measurement(t=0)

    def start_measurement(self, t):
        if self.manager.screens[3].ids["duration"].active:
            Clock.schedule_once(self.stop_measurement_duration, float(self.manager.screens[3].ids["duration_value"].text))
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
        Clock.schedule_interval(self.get_sensordata, 1 / 20)

    def stop_measurement_duration(self, t):
        self.gyroscope.disable()
        self.accelerometer.disable()
        Clock.unschedule(self.get_sensordata)

    def stop_measurement(self):
        """"Disable Sensors and unschedule get_sensordata function"""
        self.gyroscope.disable()
        self.accelerometer.disable()
        Clock.unschedule(self.get_sensordata)

    def save_data(self):
        """"Saves recorded sensordata to a .csv file named with date and current time"""
        time = datetime.datetime.now()
        time = time.strftime("%Y%m%d_%H%M%S")
        if not os.path.exists(os.path.join(self.sdpath, "acceleration")):
            os.mkdir(os.path.join(self.sdpath, "acceleration"))
        f = open(self.sdpath + "/acceleration/" + time + ".csv", "w+")
        f.write("t[s],ax[m/s2],ay[m/s2],az[m/s2],\u03C9x[rad/s],\u03C9y[rad/s],\u03C9z[rad/s]\n")
        t = 0
        for i in range(len(self.x_acceleration)):
            f.write(str(t) + "," + str(self.x_acceleration[i]) + "," + str(self.y_acceleration[i]) + "," + str(
                self.z_acceleration[i]) + "," + str(self.x_rotation[i])
                    + "," + str(self.y_rotation[i]) + "," + str(self.z_rotation[i]))
            f.write("\n")
            t += 0.05

        f.close()

    def get_sensordata(self, t):
        """Reads sensordata and appends them to the corresponding list every time the function gets called"""
        if (self.counter == 100):
            for plot in self.acc_plot:
                del (plot.points[0])
                plot.points[:] = [(i[0] - 1, i[1]) for i in plot.points[:]]

            self.counter = 99

        gyro = self.gyroscope.get_rotation()
        lin = self.accelerometer.get_linearacceleration()

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
            else:
                self.x_rotation.append(gyro[0])
                self.y_rotation.append(gyro[1])
                self.z_rotation.append(gyro[2])

        self.counter += 1



class DataScreen(Screen):
    pass


class OffsetScreen(Screen):
    pass

class MeasurementLayout(MDBoxLayout):
    pass


class DemoApp(MDApp):
    def build(self):
        screen = Builder.load_string(screen_helper)
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MeasureScreen(name='measure'))
        sm.add_widget(DataScreen(name='showdata'))
        sm.add_widget(OffsetScreen(name='offset'))
        return screen




if __name__ == "__main__":
    DemoApp().run()










