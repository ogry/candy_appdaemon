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
            programm = int(status[status_root]["Program"])
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
            error_code = int(status[status_root]["CodiceErrore"])
            if error_code == 'E0':
                state_error = "---"
            else:
                state_error = error_code

            entity_id = appliance_entity + "_error"
            self.set_state(entity_id, state=state_error, attributes = {"friendly_name": "error", "icon":"mdi:alert-circle-outline"})
        #    self.retry = 0
        except:
            pass
    ###############    

    
#MetaCarico
        try:
            status = self.get_status()
            MetaCarico = int(status[status_root]["MetaCarico"])

            entity_id = appliance_entity + "_metaCarico"
            self.set_state(entity_id, state=temp, attributes = {"friendly_name": "metacarico"})
        #    self.retry = 0
        except:
            pass
    ###############    
    

    
#StartStop
        try:
            status = self.get_status()
            StartStop = int(status[status_root]["StartStop"])

            entity_id = appliance_entity + "_startSsop"
            self.set_state(entity_id, state=temp, attributes = {"friendly_name": "startstop"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#TreinUno
        try:
            status = self.get_status()
            TreinUno = int(status[status_root]["TreinUno"])

            entity_id = appliance_entity + "_treinuno"
            self.set_state(entity_id, state=temp, attributes = {"friendly_name": "treinuno"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#Eco
        try:
            status = self.get_status()
            Eco = int(status[status_root]["Eco"])

            entity_id = appliance_entity + "_eco"
            self.set_state(entity_id, state=eco, attributes = {"friendly_name": "eco"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#Program
        try:
            status = self.get_status()
            Program = int(status[status_root]["Program"])

            entity_id = appliance_entity + "_program"
            self.set_state(entity_id, state=temp, attributes = {"friendly_name": "program"})
        #    self.retry = 0
        except:
            pass
    ###############    
    
    
#ExtraDry
        try:
            status = self.get_status()
            ExtraDry = int(status[status_root]["ExtraDry"])

            entity_id = appliance_entity + "_extradry"
            self.set_state(entity_id, state=extradry, attributes = {"friendly_name": "extradry"})
        #    self.retry = 0
        except:
            pass
    ###############    
    





#OpenDoorOpt
        try:
            status = self.get_status()
            OpenDoorOpt = int(status[status_root]["OpenDoorOpt"])

            entity_id = appliance_entity + "_opendooropt"
            self.set_state(entity_id, state=opendooropt, attributes = {"friendly_name": "opendooropt"})
        #    self.retry = 0
        except:
            pass
    ###############    

#DelayStart
        try:
            status = self.get_status()
            DelayStart = int(status[status_root]["DelayStart"])

            entity_id = appliance_entity + "_delaystart"
            self.set_state(entity_id, state=delaystart, attributes = {"friendly_name": "delaystart"})
        #    self.retry = 0
        except:
            pass
    ###############    


#RemTime
        try:
            status = self.get_status()
            RemTime = int(status[status_root]["RemTime"])

            entity_id = appliance_entity + "_remtime"
            self.set_state(entity_id, state=remtime, attributes = {"friendly_name": "remtime", "unit_of_measurement": "Minutes"})
        #    self.retry = 0
        except:
            pass
    ###############           
    ###############  
#MissSalt
        try:
            status = self.get_stats()
            MissSalt = int(status[stats_root]["MissSalt"])

            entity_id = appliance_entity + "_misssalt"
            self.set_state(entity_id, state=misssalt, attributes = {"friendly_name": "misssalt", "icon":"mdi:vibrate"})
        #    self.retry = 0
        except:
            pass
    ##############

# MissRinse           
        try:
            status = self.get_status()
            MissRinse = int(status[status_root]["MissRinse"])

            entity_id = appliance_entity + "_missrinse"
            self.set_state(entity_id, state=missrinse, attributes = {"friendly_name": "missrinse", "icon":"mdi:vibrate"}) 
        #    self.retry = 0
        except:
            pass
    ###############    


#OpenDoor
        try:
            statusrpm = self.get_status()
            OpenDoor = int(status[status_root]["OpenDoor"]) * 100

            entity_id = appliance_entity + "_opendoor"
            self.set_state(entity_id, state=opendoor, attributes = {"friendly_name": "Giri Centrifuga", "unit_of_measurement": "rpm", "icon":"mdi:sync"})
            self.retry = 0
        except:
            pass
    ###############  
    ###############     
#motore
        try:
            status = self.get_status()
            value = int(status[status_root]["motS"]) / 10 

            entity_id = appliance_entity + "_motore"
            self.set_state(entity_id, state=value, 
                        attributes = {"friendly_name": "Giri Motore", "unit_of_measurement": "rpm", "icon": "mdi:engine"})
        #    self.retry = 0
        except:
            pass
#prelavaggio
        try:
            status = self.get_status()
            prelavax = int(status[status_root]["Opt1"])
            if prelavax == 1:
                state = "ON"
            else:
                state = "OFF"

            entity_id = appliance_entity + "_opt1"
            self.set_state(entity_id, state=state, attributes = {"friendly_name": "Prelavaggio", "icon":"mdi:hand-wash"})
        #    self.retry = 0
        except:
            pass
    ###############     
#igiene 
        try:
            status = self.get_status()
            igieneplus = int(status[status_root]["Opt2"])
            if igieneplus == 1:
                state = "ON"
            else:
                state = "OFF"

            entity_id = appliance_entity + "_opt2"
            self.set_state(entity_id, state=state, attributes = {"friendly_name": "Igiene +", "icon":"mdi:hospital-box"})
        #    self.retry = 0
        except:
            pass
    ###############  
#antipiega
        try:
            status = self.get_status()
            valueantip = int(status[status_root]["Opt3"])
            if valueantip == 1:
                state = "ON"
            else:
                state = "OFF"

            entity_id = appliance_entity + "_opt3"
            self.set_state(entity_id, state=state, attributes = {"friendly_name": "Antipiega", "icon":"mdi:tshirt-v"})
        #    self.retry = 0
        except:
            pass
    ###############            
#buonanotte
        try:
            status = self.get_status()
            value = int(status[status_root]["Opt4"])
            if value == 1:
                state = "ON"
            else:
                state = "OFF"

            entity_id = appliance_entity + "_opt4"
            self.set_state(entity_id, state=state, attributes = {"friendly_name": "Buonanotte", "icon":"mdi:weather-night"})
        #    self.retry = 0
        except:
            pass
#acqplus
        try:
            status = self.get_status()
            valueacq = int(status[status_root]["Opt8"])
            if valueacq == 1:
                state = "ON"
            else:
                state = "OFF"

            entity_id = appliance_entity + "_opt8"
            self.set_state(entity_id, state=state, attributes = {"friendly_name": "Acquaplus", "icon":"mdi:water-plus"})
        #    self.retry = 0
        except:
            pass
    ###############     
#option9 
        try:
            status = self.get_status()
            value = int(status[status_root]["Opt9"])
            if value == 1:
                state = "ON"
            else:
                state = "OFF"

            entity_id = appliance_entity + "_opt9"
            self.set_state( entity_id, state=state, attributes = {"friendly_name": "Opzione 9 sconosciuta"})
        #    self.retry = 0
        except:
            pass   
#vapore
        try:
            status = self.get_status()
            valuevap = int(status[status_root]["Steam"])
            if valuevap == 1:
                state = "Basso"
            elif valuevap == 2:
                state = "Medio Basso"
            elif valuevap == 3:
                state = "Medio"
            elif valuevap == 4:
                state = "Medio Alto"
            elif valuevap == 5:
                state = "Massimo"
            else:
                state = "ESCLUSO"

            entity_id = appliance_entity + "_vapore"
            self.set_state( entity_id, state=state, attributes = {"friendly_name": "Vapore", "icon":"mdi:cloud-outline"})
        #    self.retry = 0
        except:
            pass
#stato lavaggio
        try:
            status = self.get_status()
            macchine = int(status[status_root]["PrPh"])
            #macchine = 0
            if macchine == 1:
                statemd = "In prelavaggio"
            elif macchine == 2:
                statemd = "In lavaggio"
            elif macchine == 3:
                statemd = "Risciacquo"
            elif macchine == 4:
                statemd = "Ultimo Risciacquo"
            elif macchine == 5:
                statemd = "Fine"
            elif macchine == 6:
                statemd = "Asciugatura"
            elif macchine == 7:
                statemd = "ERRORE"
            elif macchine == 8:
                statemd = "Vapore"
            elif macchine == 9:
                statemd = "Centrifuga Notturna"
            elif macchine == 10:
                statemd = "Centrifuga"
            else:
                statemd = "Inattiva"

            entity_id = appliance_entity + "_stato_lavatrice"
            self.set_state( entity_id, state=statemd, attributes = {"friendly_name": "Candy Stato", "icon":"mdi:washing-machine"})
            self.retry = 0
        except:
            pass
#livello sporco
        try:
            statussp = self.get_status()
            sporco = int(statussp[status_root]["SLevel"])
            #sporco = 0
            if sporco == 1:
                statesp = "Poco"
            elif sporco == 2:
                statesp = "Normale"
            elif sporco == 3:
                statesp = "Molto"
            else:
                statesp = "ESCLUSO"

            entity_id = appliance_entity + "_livello_sporco"
            self.set_state( entity_id, state=statesp, attributes = {"friendly_name": "Livello di Sporco", "icon":"mdi:car-brake-fluid-level"})
        except:
            pass
#controllo remoto
        try:
            status = self.get_status()
            valueremoto = int(status[status_root]["WiFiStatus"])
            
            if valueremoto == 1:
                controllorem = "ON"
            else:
                controllorem = "OFF"

            entity_id = appliance_entity + "_wifi_2"
            self.set_state( entity_id, state=controllorem, 
                            attributes = {"friendly_name": "Controllo Remoto", "WiFiStatus": valueremoto , "icon":"mdi:wifi-cog"})
            self.retry = 0
        except:
            pass
#filtro
        try: 
            statsf = self.get_stats()[stats_root]
            totalef = 0
            for (key, value) in statsf.items():
                if key.startswith("Program"):
                    totalef += int(value)
            filtro_lav = 100 - totalef
            if filtro_lav < 1:
                statefiltro = "Da Pulire"
            elif filtro_lav < 70:
                statef = "Medio Sporco"
            elif filtro_lav < 40:
                statefiltro = "Sporco"
            else:
                statefiltro = "Pulito"
                
            entity_id = appliance_entity + "_filtro"
            self.set_state(entity_id, state=statefiltro, 
                        attributes = {"friendly_name": "Filtro", "Intasamento": totalef , "icon":"mdi:air-filter"})
        except:
            pass
#filtro calcare
        try: 
            statsfc = self.get_stats()[stats_root]
            totalefc = 0
            for (key, value) in statsfc.items():
                if key.startswith("Program"):
                    totalefc += int(value)
            filtro_lav_c = 105 - totalefc
            if filtro_lav_c < 1:
                statefiltroc = "Da Pulire"
            elif filtro_lav_c < 70:
                statefiltroc = "Medio Sporco"
            elif filtro_lav_c < 40:
                statefiltroc = "Sporco"
            else:
                statefiltroc = "Pulito"
                
            entity_id = appliance_entity + "_filtro_calcare"
            self.set_state(entity_id, state=statefiltroc, attributes = {"friendly_name": "Filtro Calcare", "Livello": filtro_lav_c , "icon":"mdi:air-filter"})
        except:
            pass
####################################
#risciacquo
        try:
            status = self.get_status()
            opta = int(status[status_root]["Opt5"])
            optb = int(status[status_root]["Opt6"])
            optc = int(status[status_root]["Opt7"])
            #macchine = 0
            if opta == 1:
                state_risc = "X 1"
            elif optb == 1:
                state_risc = "X 2"
            elif optc == 1:
                state_risc = "X 3"
            else:
                state_risc = "OFF"

            entity_id = appliance_entity + "_risciacquo"
            self.set_state( entity_id, state=state_risc, attributes = {"friendly_name": "Risciaquo", "icon":"mdi:water"})
            self.retry = 0

        except:
            pass
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
