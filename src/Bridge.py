from qhue import create_new_username, QhueException
from qhue import Bridge as bdg

class Bridge():

    def __init__(self, ip):
        self.ip = str(ip)
        self.lights = []
        
        try:
            uif = open('src/user.uif', 'r')
            self.username = uif.read()
            uif.close()
        except FileNotFoundError:
            self.username = None
            self.create_user()

        self.bridge = bdg(self.ip, self.username)       

    def get_index(self, name):
        i = 0
        # We need to take the index out of our lights array
        for light in self.lights:
            if light['name'] == name:
                return i
            i += 1
    
        return -1

    def create_user(self):
        try:
            self.username = create_new_username(self.ip)
            uif = open("src/user.uif", 'w')
            uif.write(self.username)
            uif.close()
            return self.username
        except QhueException as err:
            print("Error occurred while creating a new username: {}".format(err))
            return None

    def get_username(self):
        return self.username

    #Returns a list with the registered lights on the bridge
    def list_lights(self):
        lights = []
        for k in self.bridge.lights():
            lights.append(self.bridge.lights[k]())
        
        #Updates our local array
        self.lights = lights
        return self.lights
        
    #Turns on or off the light with name name
    def turn_on_off(self, name):

        index = self.get_index(name)

        #Stores the values to our local array to stay updated
        value = self.lights[index]['state']['on']
        self.lights[index]['state']['on'] = False if value else True

        # Sets the light on or off
        self.bridge.lights(index + 1, 'state', on=self.lights[index]['state']['on'])
        return not value

    def set_brightness(self, name, brightness):
        bright = int(brightness * 2.54)
        index = self.get_index(name)
        if self.lights[index]['state']['on']:
            #Stores the values to our local array to stay updated
            self.lights[index]['state']['bri'] = bright
            #Applies the changes
            self.bridge.lights(index + 1, 'state', bri=bright)

    def get_brightness(self, name):
        index = self.get_index(name)
        #print(self.bridge('lights', index + 1))
        return int(self.bridge('lights', index + 1)['state']['bri']/2.49)
        
    def set_color(self, name, hue, saturation, value):
        index = self.get_index(name)
        #Stores the values to our local array to stay updated
        self.lights[index]['state']['hue'] = hue
        self.lights[index]['state']['sat'] = 240

        #Applies the changes
        self.bridge.lights(index + 1, 'state', sat=240)
        self.bridge.lights(index + 1, 'state', hue=hue)
