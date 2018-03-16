                                                                                    #Copyright (c) 2005, Essien Ita Essien
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
#Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 
#Neither the name of pysystray nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission. 
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import bases
import menu
import utils

__all__ = ['App', 'Menu', 'MenuItem', 'DEFAULT_HANDLER', 'threaded']


DEFAULT_HANDLER = utils.DEFAULT_HANDLER
Menu = menu.Menu
MenuItem = menu.MenuItem

threaded = utils.threaded

        
class App(bases.AppBase):
    def __init__(self, title, icon=None):
        bases.AppBase.__init__(self, title, icon)
        
    def start(self):
        self._start()
    
    def stop(self):
        self._stop()

class Control(bases.AppBase):
    def __init__(self, title, icon=None):
        bases.AppBase.__init__(self, title, icon)
        self.enabled = False
        
    def __get_enabled(self):
        try:
            return self.systray.alive
        except AttributeError:
            return False
            
    def __set_enabled(self, e):
        try:
            self.systray.alive = e
        except AttributeError:
            pass #_start hasn't been called yet
            
    enabled = property(__get_enabled, __set_enabled, None, "Gets/Sets Enabled status")

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self._start_control()
            return
    
    def disable(self):
        if self.enabled:
            self._stop()
            self.enabled = False
            
    def show_message(self, message):
        if self.enabled:
            self.systray.show_message(message)
            
    def show_info(self, message):
        if self.enabled:
            self.systray.show_info(message)
            
    def show_warning(self, message):
        if self.enabled:
            self.systray.show_warning(message)
            
    def show_error(self, message):
        if self.enabled:
            self.systray.show_error(message)
        
    def hide(self):
        if self.enabled and self.visible:
            self.systray.hide()
        
    def show(self):
        if self.enabled and not self.visible:
            self.systray.show()
    
    
