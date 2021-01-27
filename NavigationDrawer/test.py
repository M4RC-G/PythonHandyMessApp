from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.properties import ObjectProperty

Window.size = (370, 620)

screen_helper = """

ScreenManager:
    MenuScreen:
    MeasureScreen:
    DataScreen:
    SettingScreen:

<ContentNavigationDrawer>:

    ScrollView:

        MDList:

            OneLineListItem:
                text: "Screen 1"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "measure"

            OneLineListItem:
                text: "Screen 2"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "showdata"
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
        text: '             Settings            '
        icon: 'run-fast'
        pos_hint: {'center_x':0.5, 'center_y':0.25}
        on_press:
            root.manager.current = 'settings'
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
        pos_hint: {'center_x':0.26, 'center_y':0.13} 
    MDRectangleFlatButton:
        text: 'Restore Values'
        pos_hint: {'center_x':0.73, 'center_y':0.13} 
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
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.85}
    MDSwitch:
        id: 'duration'
        pos_hint: {'center_x': 0.1, 'center_y': 0.77}
    MDLabel:
        text: "Duration in s"
        pos_hint: {'center_x': 0.7, 'center_y': 0.77}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.77}
    MDSwitch:
        id: 'samplingrate'
        pos_hint: {'center_x': 0.1, 'center_y': 0.69}
    MDLabel:
        text: "samplingrate"
        pos_hint: {'center_x': 0.7, 'center_y': 0.69}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.69}
    MDSwitch:
        id: 'offset_lin'
        pos_hint: {'center_x': 0.1, 'center_y': 0.61}
    MDLabel:
        text: "Offset Linear"
        pos_hint: {'center_x': 0.7, 'center_y': 0.61}
    MDLabel:
        text: "X"
        pos_hint: {'center_x': 0.9, 'center_y': 0.57}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.57}
    MDLabel:
        text: "Y"
        pos_hint: {'center_x': 0.9, 'center_y': 0.49}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.49}
    MDLabel:
        text: "Z"
        pos_hint: {'center_x': 0.9, 'center_y': 0.41}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.41}
    MDSwitch:
        id: 'offset_rot'
        pos_hint: {'center_x': 0.1, 'center_y': 0.33}
    MDLabel:
        text: "Offset Rotatorisch"
        pos_hint: {'center_x': 0.7, 'center_y': 0.33}
    MDLabel:
        text: "X"
        pos_hint: {'center_x': 0.9, 'center_y': 0.29}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.29}
    MDLabel:
        text: "Y"
        pos_hint: {'center_x': 0.9, 'center_y': 0.21}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.21}
    MDLabel:
        text: "Z"
        pos_hint: {'center_x': 0.9, 'center_y': 0.13}
    MDTextFieldRect:
        size_hint: 0.3, None
        height: "30dp"
        pos_hint: {'center_x': 0.7, 'center_y': 0.13}
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
"""
class MenuScreen(Screen):
    pass


class MeasureScreen(Screen):
    pass


class DataScreen(Screen):
    pass


class SettingScreen(Screen):
    pass

sm = ScreenManager(id="screen_manager")
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(MeasureScreen(name='measure'))
sm.add_widget(DataScreen(name='showdata'))
sm.add_widget(SettingScreen(name='settings'))
class ContentNavigationDrawer(BoxLayout):
    nav_drawer = ObjectProperty()







class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen

if __name__ == "__main__":
    DemoApp().run()