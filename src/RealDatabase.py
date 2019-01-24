"""
    RealDatabase describes the infrastructure analyzed and passed to the simulator.
    It is not the database modified by the simulator
"""

import pymongo as pm 
import time, json
import SECRETS as config
from bson.objectid import ObjectId
import Database

client = pm.MongoClient("mongodb://%s:%s@%s:%d" % (config.db_username, 
                                                   config.db_password, 
                                                   config.db_host, 
                                                   config.db_port))
client.drop_database("realDatabase")
db = client.realDatabase
# Building RealDatabase
db.Rdevices.insert_one({
            "ipAddress": "10.10.20.51",
            "port": 8443,
            "deviceId": 1,
            "totalCPU": 2000,
            "totalMEM": 128,
            "totalVCPU": 2,
            "maxVCPUPerApp": 2,
            "chaos_down_prob": 0.4,
            "chaos_revive_prob": 0.2,
            "distributions": { 
                "CPU": [
                    {
                        "timeStart": 0,
                        "timeEnd": 24,
                        "mean": 180,
                        "deviation": 39
                    }
                ],
                "MEM": [
                    {
                        "timeStart": 0,
                        "timeEnd": 24,
                        "mean": 55,
                        "deviation": 16
                    }
                ]
            }
        })

db.Rdevices.insert_one({
            "ipAddress": "10.10.20.52",
            "port": 8443,
            "deviceId": 2,
            "totalCPU": 1000,
            "totalVCPU": 2,
            "maxVCPUPerApp": 2,
            "totalMEM": 128,
            "chaos_down_prob": 0.4,
            "chaos_revive_prob": 0.2,
            "distributions": { 
                "CPU": [
                    {
                        "timeStart": 0,
                        "timeEnd": 24,
                        "mean": 189,
                        "deviation": 30
                    }
                ],
                "MEM": [
                    {
                        "timeStart": 0,
                        "timeEnd": 24,
                        "mean": 105,
                        "deviation": 32
                    }
                ]
            }
        })
        
db.Rdevices.insert_one({
            "ipAddress": "10.10.20.53",
            "port": 8443,
            "deviceId": 3,
            "totalCPU": 1000,
            "totalVCPU": 2,
            "maxVCPUPerApp": 2,
            "totalMEM": 128,
            "chaos_down_prob": 0.4,
            "chaos_revive_prob": 0.2,
            "distributions": { 
                "CPU": [
                    {
                        "timeStart": 0,
                        "timeEnd": 24,
                        "mean": 330,
                        "deviation": 78
                    }
                ],
                "MEM": [
                    {
                        "timeStart": 0,
                        "timeEnd": 24,
                        "mean": 118,
                        "deviation": 20
                    }
                ]
            }
        })


def getDevice(ip = None, port = None, deviceId = None):
    if ip == None and port == None and deviceId == None:
        return None
    if ip != None and port != None:
        return  db.Rdevices.find_one({"ipAddress": ip, "port": port})
    if deviceId != None:
        return Database.getDevice(deviceId)

    
