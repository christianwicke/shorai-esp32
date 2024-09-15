# shorai-esp32

This is a fork of https://github.com/toremick/shorai-esp32/ . 
It provides mqtt control for Toshiba Shorai and Seiya air conditioner.
This fork has a few modifications since the original didn't work for me.

This works great for me, but is at your own risk!

## Software install
* Install thonny (www.thonny.org) on your computer.
* Flash MicroPython on your esp32 using these instructions: https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/ , section "Flashing MicroPython Firmware using Thonny IDE". (I used MicroPython v1.23.0.)
  ![thonny options](images/thonny-options-interpreter.png)
  ![thonny flash options](images/thonny-flash-options.png)
* Open this project in thonny.
* copy config_example.py to config.py and insert your configuration there.
* Click right on the folder main and choose "Upload to /"
  ![upload main folder](images/upload_main.png)
* Upload config.py and boot.py the same way. (thonny asks you whether you want to overwrite boot.py. Accept with OK.)
* Finally click on the red STOP-icon to reset the esp32.

### PCB Schematic
![PCB Schematic](images/schematic.PNG?raw=true "PCB Schematic")

### PCB Layout
![PCB layout](images/pcb.PNG?raw=true "PCB layout")
U5 is a jumper, close the jumper to be powered from the heatpump. Remove jumper when powered from usb.

R1: 220R  
R2: 470R  
R3: 10K  
R7,R8,R9,R10: 1K  
U1,U2: 817A (Optocouplers)  
C1: 100uF  
U5: When connected with a Jumper, the pcb is powered from the AC (can be soldered)  

Files for PCB (and possible to order): https://oshwlab.com/toremick/toshiba-ac-heatpump-mqtt  

### Parts list

* 1 x ESP32-DevKitC v4 (38 pins)
* 2 x EL817A Optocoupler (https://www.ebay.com/itm/Straight-Plug-Optocoupler-EL817-A-B-C-D-F-DIP-4-Compatible-PC817-Isolator/253795050804?hash=item3b175d2534:g:LjcAAOSwXVNbY~z3)
* 4 x 0.25w 1K resistors
* 1 x 0.25w 470R resistor
* 1 x 0.25w 10K resistor
* 1 x 0.25w 220R resistor
* 1 x 100uF (11mmx5mm) Capacitor 
* 1 x S05B-PASK-2 (header for connection cable) or 1 x S5B-PH-K-S (header for PH 2.0 connection cable, see below)
* and 2.54mm header pins and sockets

### Connecting the esp to the air conditioner
Unfortunately, Toshiba is using a JST PA connection to connect WIFI support. 
The PA type is seldom used.
I didn't find any crimped extension cables to buy.
If you see some, please let me know, I add a link to them here.
So there are 3 choices, how you can connect your esp:
#### (A) Crimping your own JST PA extension cable

Here is the extra part list for creating a extension cable:

* JST, PA Female Crimp Connector Housing, 2mm Pitch, 5 Way, 1 Row (https://no.rs-online.com/web/p/wire-housings-plugs/1630360/)
* JST, PA Female Connector Housing, 2mm Pitch, 5 Way, 1 Row (https://no.rs-online.com/web/p/wire-housings-plugs/4766798/)
* JST, PA Female Crimp Connector Housing SPAL-001T-P0.5 (https://no.rs-online.com/web/p/crimp-contacts/1630376/)
* JST, PA, PBV, PHD Female Crimp Terminal Contact 22AWG SPHD-001T-P0.5 (https://no.rs-online.com/web/p/crimp-contacts/6881381/)

#### (B) Connecting esp without extension cable

toremick skipped crimping the connection cable. He soldered the capacitor on the solder side laying flat. This way it will fit inside the AC unit:

![PCB solder](images/pcb_solder.png?raw=true "PCB Solder")
![PCB cover](images/pcb_cover.png?raw=true "PCB Cover")

#### (C) Using a PH 2.0 extension cable
I was worried that the metal cover might shield the WIFI from the esp if I go for (B) and connect the esp directly.
But instead of crimping my own JST PA extension cable, I bought 10cm JST PH 2.0 extension cables.
![PH 2.0 extension](images/PH-20-extension.png)
I solederd a S5B-PH-K-S on the pcb instead of the S05B-PASK-2.
![pcb with S5B-PH-K-S](images/pcb-with-S5B-PH-K-S.png)
![soldered esp32](images/soldered-esp32.png)
The extension cable therfore fits the pcb, but the housing has to be clipped a bit.
![clip PH 2.0 extension](images/clip-PH-20-extension.png)
![clipped PH 2.0 extension](images/clipped-PH-20-extension.png)
Afterwards it can be connected to the air conditioner.
![connected PH 2.0 extension](images/connected-PH-20-extension.png)
![connected esp32](images/connected-esp32.png)



### Home assistant Climate config part

**Important note:**
If you have more than one device, please remember to change the *name*, *unique_id* and all the mqtt strings to have unique names. 
For each device replace the 'ac/livingroom' name with the unique 'maintopic' you have configured in the config.py of your ESP32 device.
Also give each device a separate hostname.

```
mqtt:
  climate:
    - name: HeatPump
      icon: mdi:air-conditioner
      unique_id: toshibaheatpump
      modes:
        - "off"
        - "auto"
        - "cool"
        - "heat"
        - "dry"
        - "fan_only"
      swing_modes:
        - "on"
        - "off"
      fan_modes:
        - "quiet"
        - "lvl_1"
        - "lvl_2"
        - "lvl_3"
        - "lvl_4"
        - "lvl_5"
        - "auto"
      power_command_topic: "ac/livingroom/state/set"
      power_state_topic: "ac/livingroom/state/state"
      mode_command_topic: "ac/livingroom/mode/set"
      mode_state_topic: "ac/livingroom/mode/state"
      current_temperature_topic: "ac/livingroom/roomtemp"
      temperature_command_topic: "ac/livingroom/setpoint/set"
      temperature_state_topic: "ac/livingroom/setpoint/state"
      fan_mode_command_topic: "ac/livingroom/fanmode/set"
      fan_mode_state_topic: "ac/livingroom/fanmode/state"
      swing_mode_command_topic: "ac/livingroom/swingmode/set"
      swing_mode_state_topic: "ac/livingroom/swingmode/state"
      temp_step: 1
      precision: 1
    
```


### Add following to automations.yaml or where you have your automations
(this will query the heatpump for all values so HA will have current state
for everything)

``` 
- id: gethpvalues_on_startup 
  alias: "HP states on HA start-up" 
  trigger:
    platform: homeassistant
    event: start
  action: 
  - service: mqtt.publish 
    data: 
      topic: ac/livingroom/doinit
      payload: startup-ha
    
```


