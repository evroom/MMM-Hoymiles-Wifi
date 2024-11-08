# MMM-Hoymiles
MagicMirror module for Hoymiles Wifi inverter info

- This module shows current data for Hoymiles Wifi inverter with the help of the hoymiles-wifi python lib
- Project is based on https://github.com/ulrichwisser/MMM-HTMLSnippet
- The Inverter Data is fetched with https://github.com/suaveolent/hoymiles-wifi
- Whenever the widget refreshes, the flask server will call the python script which will render a html with the current data from holymiles-wifi

## Installation
```shell
cd ~/MagicMirror/modules/
git clone https://github.com/schris88/MMM-Hoymiles-Wifi
```

### Config example
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

The test dataset is taken from `response_test_data.txt`.
Do not forget to undo the change after testing.
