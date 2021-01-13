from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from gyro import AndroidGyroscope
from linaccel import AndroidLinearAccelerometer
from kivy.clock import Clock
from jnius import autoclass
import datetime
import os
from android.permissions import request_permissions, Permission



screen_helper = """
ScreenManager:
    MenuScreen:
    MeasureScreen:
    DataScreen:
    OffsetScreen:


<MenuScreen>:
    name: 'menu'
    MDBoxLayout:
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
    MDBoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10

        Widget:
    
    MDRoundFlatIconButton:
        icon: "settings"
        text: "Offset & Gain"
        on_press: root.manager.current = 'offset'
        pos_hint: {'center_x':0.5, 'center_y':0.05}
        
    MDRectangleFlatButton:
        text: 'Start'
        pos_hint: {'center_x':0.2, 'center_y':0.13}
        on_press: app.start_measurement()
    MDRectangleFlatButton:
        text: 'Stop'
        pos_hint: {'center_x':0.5, 'center_y':0.13} 
        on_press: app.stop_measurement()
    MDRectangleFlatButton:
        text: 'Save'
        pos_hint: {'center_x':0.8, 'center_y':0.13}
        on_press: app.save_data() 
    
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
        id: 'delay'
        pos_hint: {'center_x': 0.1, 'center_y': 0.95}
    MDLabel:
        text: "Delay in s"
        pos_hint: {'center_x': 0.7, 'center_y': 0.95}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.95}
        
    MDSwitch:
        id: 'duration'
        pos_hint: {'center_x': 0.1, 'center_y': 0.85}
    MDLabel:
        text: "Duration in s"
        pos_hint: {'center_x': 0.7, 'center_y': 0.85}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.85}
        
    MDSwitch:
        id: 'offset_lin'
        pos_hint: {'center_x': 0.1, 'center_y': 0.75}
    MDLabel:
        text: "Offset Linear"
        pos_hint: {'center_x': 0.7, 'center_y': 0.75}
    MDLabel:
        text: "X"
        pos_hint: {'center_x': 0.9, 'center_y': 0.7}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.7}
    MDLabel:
        text: "Y"
        pos_hint: {'center_x': 0.9, 'center_y': 0.6}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.6}
    MDLabel:
        text: "Z"
        pos_hint: {'center_x': 0.9, 'center_y': 0.5}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.5}
        
    MDSwitch:
        id: 'offset_rot'
        pos_hint: {'center_x': 0.1, 'center_y': 0.4}
    MDLabel:
        text: "Offset Rotatorisch"
        pos_hint: {'center_x': 0.7, 'center_y': 0.4}
    MDLabel:
        text: "X"
        pos_hint: {'center_x': 0.9, 'center_y': 0.35}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.35}
    MDLabel:
        text: "Y"
        pos_hint: {'center_x': 0.9, 'center_y': 0.25}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.25}
    MDLabel:
        text: "Z"
        pos_hint: {'center_x': 0.9, 'center_y': 0.15}
    MDTextFieldRect:
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
    pass


class DataScreen(Screen):
    pass


class OffsetScreen(Screen):
    pass

class MeasurementLayout(MDBoxLayout):
    pass


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen

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

        self.x_rotation = []
        self.y_rotation = []
        self.z_rotation = []
        self.x_acceleration = []
        self.y_acceleration = []
        self.z_acceleration = []
        self.accelerometer = AndroidLinearAccelerometer()
        self.gyroscope = AndroidGyroscope()

    def start_measurement(self):
        """"Start measurement. Calls init_measurement function and enables the sensors.
            Lists to save values are being cleared and a timer to read the sensor data gets started"""
        self.init_measurement()
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
        Clock.schedule_interval(self.get_sensordata, 1 / 20)

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
        gyro = self.gyroscope.get_rotation()
        lin = self.accelerometer.get_linearacceleration()

        if (not lin == (None, None, None)):
            # self.plot[0].points.append((self.counter, lin[0]))
            self.x_rotation.append(gyro[0])
            self.x_acceleration.append(lin[0])
            # self.plot[1].points.append((self.counter, lin[1]))
            self.y_rotation.append(gyro[1])
            self.y_acceleration.append(lin[1])
            # self.plot[2].points.append((self.counter, lin[2]))
            self.z_rotation.append(gyro[2])
            self.z_acceleration.append(lin[2])


if __name__ == "__main__":
    DemoApp().run()










