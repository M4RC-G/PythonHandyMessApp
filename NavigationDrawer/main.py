from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer

screen_helper = """
ScreenManager:
    id: screen_manager

    MenuScreen:
    MeasureScreen:
    DataScreen:
    SettingScreen:
    CalibrationScreen:
    AboutScreen:
    HelpScreen:


<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:

    MDRectangleFlatButton:
        text: 'Settings'
        icon: 'settings'
        size_hint_x: 0.4
        pos_hint: {'center_x':0.5, 'center_y':0.25}
        on_press:
            root.manager.current = 'settings'
            root.manager.transition.direction = "left"
    MDRectangleFlatButton:
        text: 'Calibration'
        icon: 'target'
        size_hint_x: 0.4
        pos_hint: {'center_x':0.5, 'center_y':0.4}
        on_press:
            root.manager.current = 'calibration'
            root.manager.transition.direction = "left"
    MDRectangleFlatButton:
        text: 'Show logged tracks'
        icon: 'database'
        size_hint_x: 0.4
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        on_press:
            root.manager.current = 'showdata'
            root.manager.transition.direction = "left"
    MDRectangleFlatButton:
        text: 'Start tracking'
        icon: 'run-fast'
        size_hint_x: 0.4
        pos_hint: {'center_x':0.5, 'center_y':0.7}
        on_press: 
            root.manager.current = 'measure'
            root.manager.transition.direction = "left"

    MDNavigationDrawer:
        id: nav_drawer

        orientation: 'vertical'
        spacing: '8dp'
        padding: '8dp'
        Image:
            source: 'AccTrack.jpeg'
            size_hint_x: None
            size_hint_y: None
            width: 200
        MDList:
            OneLineIconListItem:
                text: 'Start tracking'
                IconLeftWidget:
                    icon: 'run-fast'
                    on_press: root.manager.current = 'measure'
            OneLineIconListItem:
                text: 'Show logged tracks'
                IconLeftWidget:
                    icon: 'database-search'
            OneLineIconListItem:
                text: 'Calibration'
                IconLeftWidget:
                    icon: 'target'
            OneLineIconListItem:
                text: 'Settings'
                IconLeftWidget:
                    icon: 'settings-outline'
            OneLineIconListItem:
                text: 'About'
                IconLeftWidget:
                    icon: 'information-outline'
            OneLineIconListItem:
                text: 'Help'
                IconLeftWidget:
                    icon: 'help-circle-outline'
        Image:
            source: 'HE_Logo.png'
            size_hint_x: 0.6
        MDLabel:
            text: 'ATB6 ETB6 MTB6 - WS 2020/21'
            font_style: 'Caption'
            size_hint_y: None
            height: self.texture_size[1] 


<MeasureScreen>:
    name: 'measure'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:

    MDRoundFlatIconButton:
        icon: "settings"
        text: "Settings"
        on_press: root.manager.current = 'settings'
        pos_hint: {'center_x':0.5, 'center_y':0.05}

    MDRectangleFlatButton:
        text: 'Start'
        pos_hint: {'center_x':0.2, 'center_y':0.13}
    MDRectangleFlatButton:
        text: 'Stop'
        pos_hint: {'center_x':0.5, 'center_y':0.13} 
    MDRectangleFlatButton:
        text: 'Save'
        pos_hint: {'center_x':0.8, 'center_y':0.13} 

    MDIconButton:
        icon: "home"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}


<DataScreen>:
    name: 'showdata'

    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:

    MDRectangleFlatButton:
        text: 'Restore Track'
        pos_hint: {'center_x':0.5, 'center_y':0.13} 

    MDIconButton:
        icon: "home"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}


<SettingScreen>:
    name: 'settings'

    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:

    MDSwitch:
        id: 'delay'
        pos_hint: {'center_x': 0.1, 'center_y': 0.85}
    MDLabel:
        text: "Delay in s"
        pos_hint: {'center_x': 0.7, 'center_y': 0.85}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.85}

    MDSwitch:
        id: 'duration'
        pos_hint: {'center_x': 0.1, 'center_y': 0.77}
    MDLabel:
        text: "Duration in s"
        pos_hint: {'center_x': 0.7, 'center_y': 0.77}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.77}

    MDSwitch:
        id: 'samplingrate'
        pos_hint: {'center_x': 0.1, 'center_y': 0.69}
    MDLabel:
        text: "Samplingrate in Hz"
        pos_hint: {'center_x': 0.7, 'center_y': 0.69}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.69}

    MDSwitch:
        id: 'offset_lin'
        pos_hint: {'center_x': 0.1, 'center_y': 0.61}
    MDLabel:
        text: "Offset accelerations"
        pos_hint: {'center_x': 0.7, 'center_y': 0.61}
    MDLabel:
        text: "ax in m/s²"
        pos_hint: {'center_x': 0.75, 'center_y': 0.57}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.57}
    MDLabel:
        text: "ay in m/s²"
        pos_hint: {'center_x': 0.75, 'center_y': 0.49}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.49}
    MDLabel:
        text: "az in m/s²"
        pos_hint: {'center_x': 0.75, 'center_y': 0.41}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.41}

    MDSwitch:
        id: 'offset_rot'
        pos_hint: {'center_x': 0.1, 'center_y': 0.33}
    MDLabel:
        text: "Offset gyration"
        pos_hint: {'center_x': 0.7, 'center_y': 0.33}
    MDLabel:
        text: "roll rate in °/s"
        pos_hint: {'center_x': 0.75, 'center_y': 0.29}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.29}
    MDLabel:
        text: "pitch rate in  °/s"
        pos_hint: {'center_x': 0.75, 'center_y': 0.21}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False
        input_type: 'number'
        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.21}
    MDLabel:
        text: "yaw rate in °/s"
        pos_hint: {'center_x': 0.75, 'center_y': 0.13}
    MDTextFieldRect:
        size_hint: 0.25, None
        multiline: False

        hint_text: '0'
        height: "30dp"
        pos_hint: {'center_x': 0.75, 'center_y': 0.13}

    MDIconButton:
        icon: "home"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}

    MDRoundFlatIconButton:
        icon: "run-fast"
        text: "START"
        on_press: root.manager.current = 'measure'
        pos_hint: {'center_x':0.5, 'center_y':0.05}


<CalibrationScreen>:
    name: 'calibration'

    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:

    MDLabel:
        text: "Place your device on a flat surface and press the Start-button to begin with the calibration!"
        halign: 'center'
        font_style: "Subtitle1"

    MDFillRoundFlatIconButton:
        icon: 'target'
        text: "Start calibration"
        pos_hint: {'center_x':0.5, 'center_y':0.4}

    MDIconButton:
        icon: "home"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}

<AboutScreen>:
    name: 'about'

    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:

    MDLabel:
        text: "Projektarbeit: Mechatronisches Projekt"
        halign: 'center'

    MDIconButton:
        icon: "home"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}

<HelpScreen>:
    name: 'help'

    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: '360° ACC Track'
            left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
            elevation:10
        Widget:

    Image:
        source: 'Flugzeug.jpeg'


    MDIconButton:
        icon: "home"
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
        pos_hint: {'center_x':0.1, 'center_y':0.05}
"""


class ContentNavigationDrawer(BoxLayout):
    pass


class MenuScreen(Screen):
    pass


class MeasureScreen(Screen):
    pass


class DataScreen(Screen):
    pass


class SettingScreen(Screen):
    pass


class CalibrationScreen(Screen):
    pass


class AboutScreen(Screen):
    pass


class HelpScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(MeasureScreen(name='measure'))
sm.add_widget(DataScreen(name='showdata'))
sm.add_widget(SettingScreen(name='settings'))
sm.add_widget(CalibrationScreen(name='calibration'))
sm.add_widget(AboutScreen(name='about'))
sm.add_widget(HelpScreen(name='help'))


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


DemoApp().run()