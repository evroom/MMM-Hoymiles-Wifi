# MMM-Hoymiles
MagicMirror module for Hoymiles Wifi inverter info

- This module shows current data for Hoymiles Wifi inverter with the help of the hoymiles-wifi python lib
- Project is based on https://github.com/ulrichwisser/MMM-HTMLSnippet
- The Inverter Data is fetched with https://github.com/suaveolent/hoymiles-wifi
- Whenever the widget refreshes, the flask server will call the python script which will render a html with the current data from holymiles-wifi

## Project Status
This module is still under development.<br>
It might not work, can show incorrect results, will lack some counters, etc.

Test environment:
- Micro Inverter: Hoymiles HMS-800W-2T with 2 panels connected
- MagicMirror version: 2.30.0-develop
- Raspberry Pi 4 Model B Rev 1.5
- Raspbian GNU/Linux 12 (bookworm)

## TODO:
- get rid of external shell script
- change pv_data to dtu date for combined output of inverter
- add config options for DTU IP, PV-Power Range, Positioning, Size, Colors...
- ~~add template if inverter is offline (currently only displays a text)~~

## Installation
Installation can be done using the original repository **or** the develop repository.
### Main master repository:
Clone the repository:
```shell
cd ~/MagicMirror/modules/
git clone https://github.com/schris88/MMM-Hoymiles-Wifi
```
Make `HoymilesWifi.sh` executable:
```shell
chmod +x ~/MagicMirror/modules/MMM-Hoymiles-Wifi/HoymilesWifi.sh
```
### Main develop repository (to be used with caution):
Clone the repository:
```shell
cd ~/MagicMirror/modules/
git clone https://github.com/evroom/MMM-Hoymiles-Wifi
```
Make `HoymilesWifi.sh` executable:
```shell
chmod +x ~/MagicMirror/modules/MMM-Hoymiles-Wifi/HoymilesWifi.sh
```
### Config Example
Edit the file `~/MagicMirror/config/config.js` to add or modify the module.
```javascript
{
  module: "MMM-Hoymiles-Wifi",
  position: "top_left",
  config: {
    width: "300px",
    height: "320px",
    updateInterval: 60000, // in milli seconds
    frames : [
      { src: 'http://127.0.0.1:5000' },
    ]
  },
},
```

### Hoymiles Example
<img src="mmm-hoymiles.jpg" alt="mmm-hoymiles" width="300"/>

## Python Requirements
Install all Python requirements:
```shell
pip install -r requirements.txt
```
If you see this error:
```
error: externally-managed-environment
````
then try this:
```shell
python -m pip install -r requirements.txt --break-system-packages
```

## Enter DTU IP address of DTU
Change directory:
```shell
cd ~/MagicMirror/modules/MMM-Hoymiles-Wifi
```
Use you favorite editor to make the change (here nano).
```shell
nano HoymilesWifi.sh
```
Line to edit:
```
python hoymiles_data.py --dtu_ip_address <DTU_HOST_IP>
```
Where `<DTU_HOST_IP>` is the IP address of the DTU.

To turn on debugging:
```
python hoymiles_data.py --dtu_ip_address <DTU_HOST_IP> --debug
```
## Start Flask server by running HoymilesWifi.sh or add it to pm2
To start `HoymilesWifi.sh` manually:
```shell
./HoymilesWifi.sh
```

To add `HoymilesWifi.sh` to pm2:
```shell
pm2 start HoymilesWifi.sh
pm2 save
```

## Various checks
### Verify hoymiles-wifi command:
```shell
hoymiles-wifi --host <DTU_HOST_IP> identify-inverters
```
Where `<DTU_HOST_IP>` is the IP address of the DTU.

When this message is printed, it means that the inverter is turned off (mostly after sunset):
```
No response or unable to retrieve response for identify-inverters
```
### Check the HoymilesWifi status:
```shell
pm2 status
pm2 info HoymilesWifi
```
### Check the HoymilesWifi log:
```shell
pm2 logs HoymilesWifi --lines 100
```
### Make a test run, using a test dataset
Use you favorite editor to make the change (here nano).
```shell
nano HoymilesWifi.sh
```
Line to edit (add --debug --test):
```
python hoymiles_data.py --dtu_ip_address <DTU_HOST_IP> --debug --test
```
Where `<DTU_HOST_IP>` is the IP address of the DTU.

The test dataset is taken from `response_test_data.json`.
You can edit this file and replace it with your own data, for example using the output of this command:
`hoymiles-wifi --host <DTU_HOST_IP> get-real-data-new --as-json`

Do not forget to remove `--test` after testing.
