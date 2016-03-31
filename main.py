#-*- coding: utf-8 -*-

# main.py for kivy event (mainly)
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock

from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore

from kivy.config import Config

#Config.set('graphics', 'width', '640')
#Config.set('graphics', 'height', '480')

from core.decoder import Decoder
from core import logger

from core import downloadtools
from core.downloadtools import DownloadThread

class DownloaderApp(App):

    use_kivy_settings = False

    def on_pause(self):
        return True

    def paste(self):
        '''
        try:
            from kivy.core.clipboard import Clipboard
            self.main_screen.ids.page_url.text = Clipboard.paste()
        except:
            logger.error("Could not be pasted to clipboard!")
            pass
        '''
        pass

    def copy(self,text):
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
        except:
            logger.error("Could not be copied to clipboard: "+text)
            pass

    def build(self):
        self.store = JsonStore("data/store.json")
        self.download_thread = None
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.main_screen = StartScreen(name='Welcome Screen')
        self.download_screen = DownloadScreen(name="Download Screen")
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.download_screen)
        return self.screen_manager

    def target_selected(self, path, filename):
        self._popup.dismiss()
        self.main_screen.ids.target_folder.text = path
        self.store.put("target_folder",value=self.main_screen.ids.target_folder.text)

    def target_selection(self):
        content = LoadDialog(load=self.target_selected, cancel=self.dismiss_popup)
        content.ids.filechooser.path = self.main_screen.ids.target_folder.text
        self._popup = Popup(title="Choose destination", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def url_ready(self,page_url):
        if not self.main_screen.ids.page_url.text.startswith("http://") and not self.main_screen.ids.page_url.text.startswith("https://"):
            self.message("There is a problem...","URL is not accepted, needs an http/s url")
            return
        self.store.put("target_folder",value=self.main_screen.ids.target_folder.text)
        self.store.put("source_url",value=self.main_screen.ids.page_url.text)

        self.media_url = self.main_screen.ids.page_url.text
        self.video_title = self.media_url

        self.screen_manager.current = self.screen_manager.next()

        self.start_download()

    def start_download(self):
        logger.debug("start_download called")

        self.download_screen.result = "downloading "+self.media_url+"\n\n"

        self.target_file = os.path.join( self.main_screen.ids.target_folder.text , self.video_title.decode("utf-8") )
        self.target_folder = self.main_screen.ids.target_folder.text

        self.download_screen.ids.loading.opacity=1
        self.download_screen.ids.label_text_message.text="decoding:\n\n"+self.media_url
        progressDialog = self.download_screen.ids.progress_bar_download
        progressDialoglabel = self.download_screen.ids.label_text_message
        self.download_thread = DownloadThread(self.media_url,self.target_folder,self.download_screen,progressDialog,progressDialoglabel)
        self.download_thread.start()

    def abort_download(self):
        logger.debug("abort_download")
        try:
            self.download_thread.abort()
        except:
            pass
        self.screen_manager.current = self.screen_manager.previous()

    def message(self,title,body):

        content = MessageDialog()
        content.ids.message_body.text = body
        self._popup = Popup(title=title, content=content, size_hint=(0.8, 0.8))
        self._popup.open()

    def on_stop(self):
        logger.debug("on_stop event called: goodbye!")


class StartScreen(Screen):
    pass

class DownloadScreen(Screen):
    pass

class MessageDialog(BoxLayout):
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    DownloaderApp().run()