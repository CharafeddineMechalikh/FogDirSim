from APIWrapper import FogDirector
import time, random, math
from infrastructure import ciscorouters_310pz_5b5m300s as infrastructure
import requests
import simplejson, signal, os

infrastructure.create()

port = os.environ.get('SERVER_PORT', "5000")
fd = FogDirector("127.0.0.1:"+port)
code = fd.authenticate("admin", "admin_123")


def simulation_counter():
    r = requests.get('http://localhost:'+port+'/result/simulationcounter')
    return int(r.text)

def bestFit(cpu, mem):
    _, devices = fd.get_devices()
    devices = [ dev for dev in devices["data"] if dev["capabilities"]["nodes"][0]["cpu"]["available"] >= cpu 
                            and dev["capabilities"]["nodes"][0]["memory"]["available"] >= mem]
    devices.sort(reverse=True, key=(lambda dev: (dev["capabilities"]["nodes"][0]["cpu"]["available"], 
                                                dev["capabilities"]["nodes"][0]["memory"]["available"]) ))
    trial = 0
    while len(devices) == 0:
        trial += 1
        if trial == 100:
            return None, None
        _, devices = fd.get_devices()
        devices = [ dev for dev in devices["data"] if dev["capabilities"]["nodes"][0]["cpu"]["available"] >= cpu 
                                    and dev["capabilities"]["nodes"][0]["memory"]["available"] >= mem]
        devices.sort(reverse=True, key=(lambda dev: (dev["capabilities"]["nodes"][0]["cpu"]["available"], 
                                                        dev["capabilities"]["nodes"][0]["memory"]["available"]) ))
    best_fit = devices[0]
    return best_fit["ipAddress"], best_fit["deviceId"]

def reset_simulation():
    url = "http://%s/simulationreset" % ("127.0.0.1:"+port)
    r = requests.get(url)
    output = r.json()
    try:
        file  = open("simulation_results_150devices_300apps.txt", "a")
        file.write("# corrected dev and myapps number - Devices: "+str(DEVICE_NUMBER)+" - # Deployments: "+str(DEPLOYMENT_NUMBER)+"\n")
        file.write("\""+str(DEVICE_NUMBER)+"\"{")
        out = simplejson.dumps(output, indent=4, sort_keys=True)
        file.write(out)
        file.write("},\n\n")
        file.close()
    except NameError:
        pass

def add_devices():
    for i in range(1, DEVICE_NUMBER+1):
        deviceId = i+1      
        _, device1 = fd.add_device("10.10.20."+str(deviceId), "cisco", "cisco")

def install_apps():
    for i in range(0, DEPLOYMENT_NUMBER):
        try:
            dep = "dep"+str(i)
            _, myappId = fd.create_myapp(localapp["localAppId"], dep)

            deviceIp, deviceId = bestFit(100, 32)
            if deviceIp == None:
                return i
            code, res = fd.fast_install_app(myappId, [deviceId])
            trial = 0
            while code == 400:
                trial += 1
                if trial == 100:
                    return i
                deviceIp, deviceId = bestFit(100, 32)
                code, res = fd.fast_install_app(myappId, [deviceId])
            fd.fast_start_app(myappId)
        except KeyboardInterrupt:
            print(i)
            return i
    return DEPLOYMENT_NUMBER

def install_apps_ft():
    for myapp_index in range(0, DEPLOYMENT_NUMBER):
        dev_list = dev_list_sort(dev_list)
            
        dep = "dep"+str(myapp_index)
        _, myappId = fd.create_myapp(localapp["localAppId"], dep)
        
        deviceId = dev_list[0][0]
        code, res = fd.fast_install_app(myappId, [deviceId])
        if code != 400:
            dev_list[0][1] -= 100
            dev_list[0][2] -= 32
        while code == 400:
            fallimento += 1
            deviceId = dev_list[0][0]
            code, res = fd.fast_install_app(myappId, [deviceId])
            if code != 400:
                dev_list[0][1] -= 100
                dev_list[0][2] -= 32
        fd.fast_start_app(myappId)

reset_simulation()
for DEVICE_NUMBER in range(20, 151, 10):
    DEPLOYMENT_NUMBER = 300
    print("STARTING ", DEVICE_NUMBER, DEPLOYMENT_NUMBER)
    add_devices()
    code, localapp = fd.add_app("./NettestApp2V1_lxc.tar.gz", publish_on_upload=True)
    installed_apps = install_apps()
    while simulation_counter() < 3000:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break
    reset_simulation()

reset_simulation()