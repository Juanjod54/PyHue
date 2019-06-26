import math
    
def rgb_to_hsl(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    lbda = cmax-cmin

    degree = 60

    hue = 0
    saturation = 0
    light = (cmax + cmin)/2

    if (r == cmax):
        hue = int((g-b)/lbda)
    elif (g == cmax): 
        hue = int((b-r)/lbda + 2)
    elif (b == cmax): 
        hue = int((r-g)/lbda + 4)

    if (lbda != 0):
        saturation = int(lbda/(1-abs(2*light - 1)))

    return 60*hue, saturation, int(light)
