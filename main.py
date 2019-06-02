import os
import json
import time
import requests
from appJar import gui
from threading import Thread
from src.Bridge import Bridge

class hue:

    def __init__(self):
        
        self.set_brightness_thread = None

        self.ip = 0

        #Creates the gui
        self.app = gui("Philips Hue", "400x400")
        self.app.setGuiPadding(10,10)

        #Looks for the bridge's LOCAL IP
        response = requests.get('https://discovery.meethue.com/')
        ip = json.loads(response.text)
        if ip:
            self.ip = ip[0]['internalipaddress']
            self.setup_bridge()
        else:
            self.app.addLabel("noBridgeFound", "There are not any Hue Bridges available")
            self.app.addLabel("noBridgeFoundHelp", "Check you are online and on the same network")

        self.app.go()
        self.app.setStopFunction(self.exit())

    def setup_bridge(self):

        self.bridge = Bridge(self.ip)
        self.lights = self.bridge.list_lights()

        for light in self.lights:

            status = False
        
            if light['state']['on']:
                status = "Apagar "
            else:
                status = "Encender "
            
            self.app.addLabel(light['name'] + "_light", light['name'])

            row = self.app.getRow()

            if light['state']['reachable']:
                self.app.addButton("button " + light['name'], self.turn_on_off, row, 0)
                self.app.setButton("button " + light['name'], status)
            else:
                self.app.addFlashLabel("unreachable_" + light['name'], "Out of range", row, 0)

            self.app.addScale(light['name'] + "_brightness", row, 1)
            self.app.setScaleRange(light['name'] + "_brightness", 1, 100, curr=light['state']['bri'])
            self.app.setScaleChangeFunction(light['name'] + "_brightness", self.set_brightness)
            

        #Thread to set the scales
        self.set_brightness_thread = Thread(target=self.get_brightness, args=())
        self.set_brightness_thread.start()
        

    def turn_on_off(self, button):
        name = ' '.join(button.split(' ')[1:])
        status = self.bridge.turn_on_off(name)
        if status:
            self.app.setButton(button, "Apagar")
        else:
            self.app.setButton(button, "Encender")



    # Thread that runs every 0.5 secs and updates the brightness scale
    def get_brightness(self):
        while (1):
            for light in self.lights:
                brightness = self.bridge.get_brightness(light['name'])
                self.app.setScale(light['name'] + "_brightness", brightness, callFunction=False)
                
            time.sleep(0.5) 
        
    def set_brightness(self, scale):
        brightness = self.app.getScale(scale)
        name = ' '.join(scale.split('_')[:-1])
        self.bridge.set_brightness(name, brightness)

    def exit(self):
        os.system('kill %d' % os.getpid())

if __name__ == '__main__':
        hue = hue()