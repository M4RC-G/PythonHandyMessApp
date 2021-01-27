from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.properties import ObjectProperty

screen_helper = """
ScreenManager:
    MenuScreen:
    MeasureScreen:
    DataScreen:
    SettingScreen:
    CalibrationScreen:
    AboutScreen:
    HelpScreen:


<ContentNavigationDrawer>:
    orientation: 'vertical'

    Image:
        source: 'AccTrack.jpeg'
        size_hint_x: None
        size_hint_y: None
        width: 200

    ScrollView:
        MDList:
            OneLineAvatarIconListItem:
                text: 'Start tracking'
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "measure"
                IconLeftWidget:
                    icon: 'run-fast' 
            OneLineAvatarIconListItem:
                text: 'Show logged tracks'
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "showdata"
                IconLeftWidget:
                    icon: 'database-search'
            OneLineAvatarIconListItem:
                text: 'Calibration'
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "calibration"
                IconLeftWidget:
                    icon: 'target'
            OneLineAvatarIconListItem:
                text: 'Settings'
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "settings"
                IconLeftWidget:
                    icon: 'settings-outline'
            OneLineAvatarIconListItem:
                text: 'About'
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "about"
                IconLeftWidget:
                    icon: 'information-outline'
            OneLineAvatarIconListItem:
                text: 'Help'
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "help"
                IconLeftWidget:
                    icon: 'help-circle-outline'

    Image:
        source: 'HE_Logo.png'
        size_hint_x: None
        size_hint_y: None
        width: 200
    MDLabel:
        text: 'ATB6 ETB6 MTB6 - WS 2020/21'
        font_style: 'Caption'
        size_hint_y: None
        height: self.texture_size[1]



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

        ContentNavigationDrawer:
            screen_manager: root.manager
            nav_drawer: nav_drawer


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

    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
            screen_manager: root.manager
            nav_drawer: nav_drawer


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

    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
            screen_manager: root.manager
            nav_drawer: nav_drawer


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

    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
            screen_manager: root.manager
            nav_drawer: nav_drawer


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

    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
            screen_manager: root.manager
            nav_drawer: nav_drawer


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

    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
            screen_manager: root.manager
            nav_drawer: nav_drawer


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

    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
            screen_manager: root.manager
            nav_drawer: nav_drawer
"""


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


sm = ScreenManager(id="screen_manager")
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(MeasureScreen(name='measure'))
sm.add_widget(DataScreen(name='showdata'))
sm.add_widget(SettingScreen(name='settings'))
sm.add_widget(CalibrationScreen(name='calibration'))
sm.add_widget(AboutScreen(name='about'))
sm.add_widget(HelpScreen(name='help'))


class ContentNavigationDrawer(BoxLayout):
    nav_drawer = ObjectProperty()


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


DemoApp().run()