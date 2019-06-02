import json
import time
import requests
from appJar import gui
from threading import Thread
from src.Bridge import Bridge

class hue:

    def __init__(self):
        
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

    def setup_bridge(self):

        self.bridge = Bridge(self.ip)
        self.lights = self.bridge.list_lights()

        for light in self.lights:
            status = False

            self.app.addLabel(light['name'] + "_light", light['name'])

            if light['state']['on']:
                status = "Apagar "
            else:
                status = "Encender "
            
            self.app.addScale(light['name'] + "_brightness")
            self.app.setScaleRange(light['name'] + "_brightness", 1, 100, curr=light['state']['bri'])
            self.app.showScaleValue(light['name'] + "_brightness", show=True)
            self.app.addButton("button " + light['name'], self.turn_on_off)
            self.app.setButton("button " + light['name'], status)
        
        #Thread para los scale
        Thread(target=self.get_brightness, args=()).start()

        #Thread to set the scales
        #Thread(target=self.set_brightness, args=()).start()
        

    def turn_on_off(self, button):
        name = ' '.join(button.split(' ')[1:])
        status = self.bridge.turn_on_off(name)
        if status:
            self.app.setButton(button, "Apagar")
        else:
            self.app.setButton(button, "Encender")



    #Thread that runs every 0.5 secs
    def get_brightness(self):
        while (1):
            brightness = self.app.getAllScales()

            for light in self.lights:
                self.bridge.set_brightness(light['name'], brightness[light['name'] + '_brightness'])
                pass
            
            time.sleep(0.5) 
        
        
    def set_brightness(self):
        while (1):
    
            for light in self.lights:
                bright = self.bridge.get_brightness(light['name'])
                self.app.setScale(light['name'] + "_brightness", bright, callFunction=False)
            
            time.sleep(0.5) 

if __name__ == '__main__':
        hue = hue()