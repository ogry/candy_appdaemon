# based on https://github.com/jezcooke/haier_appdaemon/blob/main/checkappliance.py
import hassapi as hass
import requests
import json
import codecs
from datetime import datetime, timedelta, timezone

appliance_entity = "sensor.candy_dishwasher_wifi" # The name of the entity to use/create in Home Assistant (value with '_stats' appended)
status_root = "statusDWash"             # The root level JSON element returned by 'http-read'
power_attribute = "StatoDWash"                  # The name of the JSON attribute that containes the power on/off state.
# stats_root = "statusCounters"               # The root level JSON element returned by 'http-getStatistics'
polling_interval = 30                       # How frequently check for the latest status.
request_timeout =  15                        # Request timeout should be less than the polling interval 




max_retry_before_unavailable = 5


class CandyDishWashing(hass.Hass):
    def initialize(self):
        self.retry = 0
        self.previous_end = None
        self.run_every(self.check_appliance, "now", polling_interval)
        self.encryption_key = self.args["encryption_key"]
        self.log(f"encryption_key: {self.encryption_key!r}")
        self.appliance_host = self.args["appliance_host"]

    def check_appliance(self, kwargs):
        try:
            status = self.get_status()
            power = int(status[status_root][power_attribute])
            if power == 1:
                state = "Idle"
            elif power == 2:
                state = "Running"
            elif power == 3:
                state = "Paused"
            elif power == 4:
                state = "Delayed start selection"
            elif power == 5:
                state = "Delayed start programmed"
            elif power == 6:
                state = "ERROR"
            elif power == 7:
                state = "Finished"
            elif power == 8:
                state = "Finished!!"
            else:
                state = "Unknow"
            
            attributes = status[status_root]
            self.set_state(appliance_entity, state=state, attributes=attributes) #{"friendly_name": "Candy DishWasher", "icon": "mdi:washing-machine" })
            self.retry = 0
            remaining_minutes = int(attributes["RemTime"]) // 60 # + int(attributes["DelVal"])
            now_rounded = datetime.now(timezone.utc).replace(second=0, microsecond=0) + timedelta(minutes=1)
            end = now_rounded + timedelta(minutes=remaining_minutes)
            if self.previous_end is not None:
                if abs(end - self.previous_end) <= timedelta(minutes=1):
                    end = max(end, self.previous_end)
            self.previous_end = end
            entity_id = appliance_entity + "_programEnd"
            self.set_state(
                entity_id,
                state=end.isoformat(),
                attributes={"friendly_name": "Candy Finish ","device_class": "timestamp","Time End": remaining_minutes, "icon": "mdi:av-timer"},
            )
        except Exception as e:
            self.log(f"error when getting status: {e}")
            self.retry += 1
            if self.retry > max_retry_before_unavailable:
                self.set_state(appliance_entity, state="OFF LINE")
                entity_id = appliance_entity + "_programEnd"
                self.set_state(
                    entity_id,
                    state="unavailable",
                    attributes={"friendly_name": "#Candy Dishwasher", "device_class": "timestamp", "icon": "mdi:timer-off-outline"},
                )
                previous_end = None
            return
        

""" 
#cicli conta
        try:
            entity_id = appliance_entity + "_stats"
            stats = self.get_stats()[stats_root]
            total = 0
            for (key, value) in stats.items():
                if key.startswith("Program"):
                    total += int(value)
            self.set_state(entity_id, state=total, 
                        attributes={ "friendly_name": "Candy Cicli totali", "icon": "mdi:washing-machine"},)
        except:
            pass
###################################### 
"""
#programma
        try:
            status = self.get_status()
            programm = status[status_root]["Program"]
            rem = int(status[status_root]["RemTime"]) // 60
            
            if programm == 'P0':
                state_program = "SPECIAL 39 MINUTI"
            elif programm == 'P1':
                state_program = "MISTI & COLORATI 59  MINUTI"
            elif programm == 'P2':
                state_program = "COTONE PERFETTO" 
            else:
                state_program = programm
            
            entity_id = appliance_entity + "_program"
            self.set_state(entity_id, state=state_program, attributes = {"friendly_name": "Program", "icon":"mdi:format-list-bulleted-type"})
            #self.retry = 0
        except:
            pass
    ###############    

#errori
        try:
            status = self.get_status()
            error_code = status[status_root]["CodiceErrore"]

            entity_id = appliance_entity + "_error"
            self.set_state(entity_id, state=error_code, attributes = {"friendly_name": "error", "icon":"mdi:alert-circle-outline"})
        #    self.retry = 0
        except:
            pass
    ###############    

    
#MetaCarico
        try:
            status = self.get_status()
            MetaCarico = status[status_root]["MetaCarico"]

            entity_id = appliance_entity + "_metaCarico"
            self.set_state(entity_id, state=MetaCarico, attributes = {"friendly_name": "metacarico"})
        #    self.retry = 0
        except:
            pass
    ###############    
    

    
#StartStop
        try:
            status = self.get_status()
            StartStop = status[status_root]["StartStop"]

            entity_id = appliance_entity + "_startSsop"
            self.set_state(entity_id, state=StartStop, attributes = {"friendly_name": "startstop"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#TreinUno
        try:
            status = self.get_status()
            TreinUno = status[status_root]["TreinUno"]

            entity_id = appliance_entity + "_treinuno"
            self.set_state(entity_id, state=TreinUno, attributes = {"friendly_name": "treinuno"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#Eco
        try:
            status = self.get_status()
            Eco = status[status_root]["Eco"]

            entity_id = appliance_entity + "_eco"
            self.set_state(entity_id, state=Eco, attributes = {"friendly_name": "eco"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#Program
        try:
            status = self.get_status()
            Program = status[status_root]["Program"]

            entity_id = appliance_entity + "_program"
            self.set_state(entity_id, state=Program, attributes = {"friendly_name": "program"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#ExtraDry
        try:
            status = self.get_status()
            ExtraDry = status[status_root]["ExtraDry"]

            entity_id = appliance_entity + "_extradry"
            self.set_state(entity_id, state=ExtraDry, attributes = {"friendly_name": "extradry"})
        #    self.retry = 0
        except:
            pass
    ###############    
    





#OpenDoorOpt
        try:
            status = self.get_status()
            OpenDoorOpt = status[status_root]["OpenDoorOpt"]

            entity_id = appliance_entity + "_opendooropt"
            self.set_state(entity_id, state=OpenDoorOpt, attributes = {"friendly_name": "opendooropt"})
        #    self.retry = 0
        except:
            pass
    ###############    

#DelayStart
        try:
            status = self.get_status()
            DelayStart = status[status_root]["DelayStart"]

            entity_id = appliance_entity + "_delaystart"
            self.set_state(entity_id, state=DelayStart, attributes = {"friendly_name": "delaystart"})
        #    self.retry = 0
        except:
            pass
    ###############    


#RemTime
        try:
            status = self.get_status()
            RemTime = status[status_root]["RemTime"]

            entity_id = appliance_entity + "_remtime"
            self.set_state(entity_id, state=RemTime, attributes = {"friendly_name": "remtime", "unit_of_measurement": "Minutes"})
        #    self.retry = 0
        except:
            pass
    ###############           
    ###############  
#MissSalt
        try:
            status = self.get_stats()
            MissSalt = status[stats_root]["MissSalt"]

            entity_id = appliance_entity + "_misssalt"
            self.set_state(entity_id, state=MissSalt, attributes = {"friendly_name": "misssalt", "icon":"mdi:vibrate"})
        #    self.retry = 0
        except:
            pass
    ##############

# MissRinse           
        try:
            status = self.get_status()
            MissRinse = status[status_root]["MissRinse"]

            entity_id = appliance_entity + "_missrinse"
            self.set_state(entity_id, state=MissRinse, attributes = {"friendly_name": "missrinse", "icon":"mdi:vibrate"}) 
        #    self.retry = 0
        except:
            pass
    ###############    


#OpenDoor
        try:
            statusrpm = self.get_status()
            OpenDoor = status[status_root]["OpenDoor"]

            entity_id = appliance_entity + "_opendoor"
            self.set_state(entity_id, state=OpenDoor, attributes = {"friendly_name": "opendoor"})
            # self.retry = 0
        except:
            pass
    ###############  
    ###############     

#StatoWiFi
        try:
            status = self.get_status()
            StatoWiFi = status[status_root]["StatoWiFi"]
            
 
            entity_id = appliance_entity + "_wifi"
            self.set_state( entity_id, state=StatoWiFi, attributes = {"friendly_name": "WiFi"})
            # self.retry = 0
        except:
            pass


# R1           
        try:
            status = self.get_status()
            R1 = status[status_root]["R1"]

            entity_id = appliance_entity + "_r1"
            self.set_state(entity_id, state=R1, attributes = {"friendly_name": "R1"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R2           
        try:
            status = self.get_status()
            R2 = status[status_root]["R2"]

            entity_id = appliance_entity + "_r2"
            self.set_state(entity_id, state=R2, attributes = {"friendly_name": "R2"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R3           
        try:
            status = self.get_status()
            R3 = status[status_root]["R3"]

            entity_id = appliance_entity + "_r3"
            self.set_state(entity_id, state=R3, attributes = {"friendly_name": "R3"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R4           
        try:
            status = self.get_status()
            R4 = status[status_root]["R4"]

            entity_id = appliance_entity + "_r4"
            self.set_state(entity_id, state=R4, attributes = {"friendly_name": "R4"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R4           
        try:
            status = self.get_status()
            R4 = status[status_root]["R4"]

            entity_id = appliance_entity + "_r4"
            self.set_state(entity_id, state=R4, attributes = {"friendly_name": "R4"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R5           
        try:
            status = self.get_status()
            R5 = status[status_root]["R5"]

            entity_id = appliance_entity + "_r5"
            self.set_state(entity_id, state=R5, attributes = {"friendly_name": "R5"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R6           
        try:
            status = self.get_status()
            R6 = status[status_root]["R6"]

            entity_id = appliance_entity + "_r6"
            self.set_state(entity_id, state=R6, attributes = {"friendly_name": "R6"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R7           
        try:
            status = self.get_status()
            R7 = status[status_root]["R7"]

            entity_id = appliance_entity + "_r7"
            self.set_state(entity_id, state=R7, attributes = {"friendly_name": "R7"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R8           
        try:
            status = self.get_status()
            R8 = status[status_root]["R8"]

            entity_id = appliance_entity + "_r8"
            self.set_state(entity_id, state=R8, attributes = {"friendly_name": "R8"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R9           
        try:
            status = self.get_status()
            R9 = status[status_root]["R9"]

            entity_id = appliance_entity + "_r9"
            self.set_state(entity_id, state=R9, attributes = {"friendly_name": "R9"}) 
        #    self.retry = 0
        except:
            pass
    ###############    

# R15
        try:
            status = self.get_status()
            R15 = status[status_root]["R15"]

            entity_id = appliance_entity + "_r15"
            self.set_state(entity_id, state=R15, attributes = {"friendly_name": "R15"}) 
        #    self.retry = 0
        except:
            pass
    ###############    


####################################
#diagnosi
        try:
            status = self.get_status()
            diaa = int(status[status_root]["DisTestOn"])
            diab = int(status[status_root]["DisTestRes"])
            #macchine = 0
            if diaa == 1:
                state_risc = "In Corso"
            elif diab == 1:
                state_risc = "OK"
            elif diab == 2:
                state_risc = "ERRORE"
            else:
                state_risc = "---"

            entity_id = appliance_entity + "_diagnosi"
            self.set_state( entity_id, state=state_risc, attributes = {"friendly_name": "Diagnosi", "icon":"mdi:medical-bag"})
            self.retry = 0
        except:
            pass
##################################
##################################
    def get_status(self):
        return self.get_data("read")

    def get_stats(self):
        self.get_data("prepareStatistics")
        return self.get_data("getStatistics")

    def get_data(self, command):
        res = requests.get(
            "http://" + self.appliance_host + "/http-" + command + ".json?encrypted=1",
            timeout=request_timeout,
        )
        return json.loads(self.decrypt(codecs.decode(res.text, "hex"), self.encryption_key))

    def decrypt(self, cipher_text, key):
        decrypted = ""

        for i in range(len(cipher_text)):
            decrypted += chr(cipher_text[i] ^ ord(key[i % len(key)]))

        return decrypted
