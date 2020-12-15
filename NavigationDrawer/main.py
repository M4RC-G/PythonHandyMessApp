from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (320, 520)

navigation_helper = """
Screen:
    NavigationLayout:
        ScreenManager:
        
            Screen:

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
                MDRectangleFlatButton:
                    text: '  Show logged data   '
                    icon: 'run-fast'
                    pos_hint: {'center_x':0.5, 'center_y':0.45}
                MDRectangleFlatButton:
                    text: ' Start measurement '
                    icon: 'run-fast'
                    pos_hint: {'center_x':0.5, 'center_y':0.65}
            
                    
        MDNavigationDrawer:
            id: nav_drawer
            
            BoxLayout:
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
                        text: 'Start measurement'
                        IconLeftWidget:
                            icon: 'run-fast'
                    OneLineIconListItem:
                        text: 'Show logged data'
                        IconLeftWidget:
                            icon: 'database-search'
                    OneLineIconListItem:
                        text: 'Offset & Gain'
                        IconLeftWidget:
                            icon: 'map-marker-distance'
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
               
                    
"""




class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(navigation_helper)
        return screen


DemoApp().run()











