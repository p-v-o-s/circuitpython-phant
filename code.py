import socket
import time
import machine
import onewire, ds18x20


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('InmanSquareOasis', 'portauprince')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    
def get_temps():
    # the device is on GPIO12
    dat = machine.Pin(12)

    # create the onewire object
    ds = ds18x20.DS18X20(onewire.OneWire(dat))

    # scan for devices on the bus
    roms = ds.scan()
    
    temps=[]
    
    for rom in roms:
        #print(rom)
        ds.convert_temp()
        time.sleep(1)
        temp=ds.read_temp(rom)
        temps.append(temp)
    print(temps)
    
    return temps

    
def post_values():

    do_connect()
    
    temps = get_temps()

    url='http://159.203.128.53/input/bLzgdDwgq4CgqLZmwdrYHGK68908?private_key=GmPOGBYOW6spAV328wynUBEgzeGz&temp1='+str(temps[0])+'&temp2='+str(temps[1])+'&temp3='+str(temps[2])

    http_get(url)

def blink():
    led = machine.Pin(0, machine.Pin.OUT)
    led.low()
    time.sleep(1)
    led.high()
    time.sleep(1)

while True: 
    blink()
    blink()
    post_values()
    blink()
    time.sleep(20)



