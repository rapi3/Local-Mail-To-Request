# mqtt-email-srv
Python code that it will run as a local email server for CCTV, and translate emails sent by Dahua CCTV EZIP & IPC camera in MQTT message.<br>
Another variant of code that it will run under Postfix it is available here: https://github.com/rapi3/mqtt-email<br>
```
q: why ?
a: Because for Dahua EZIP camera don't exist until now an integration for IOT and you can't integrate in HA (untill now).

q: what it does ?
a: run as email server for cctv parse emails sent by cctv camera, search for alarm string and if found it publish MQTT message in camera topic.

q: can work for any camera ?
a: yes, you need to add string to find and it will work for any camera that can send email when it detect motion.

q: what do I need to run ?
a: You need to have Python at least v3.6 and MQTT server running and optional Home Assistant.
```
----
Some camera will send mesages encoded in MIME 64 format.<br>
To decode email sent by camera if it is encoded MIME Base 64 use:

https://online-free-tools.com/en/base_64_encoder_decoder

----
<b>Dahua EZIP</b> camera when detect motion send email message (encoded) in this format:
```
Alarm Event: Motion Detection Start
Alarm Input Channel: 1
Alarm Start Time(D/M/Y H:M:S): 21/12/2021 22:15:33
Alarm Device Name: EZIP08
Alarm Name: 
IP Address: 192.168.2.155
```
we need to search for first line: "Alarm Event: Motion Detection Start"<br>
encoded will be: "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gU3RhcnQ"

<b>Dahua IPC</b> camera when detect motion send email message (encoded) in this format:
```
Alarm Event: Motion Detection
Alarm Input Channel: 1
Alarm Start Time(D/M/Y H:M:S): 23/12/2021 10:27:46
Alarm Device Name: IPC06
Alarm Name: 
IP Address: 192.168.2.164
```
we need to search for first line and part of seccond line.<br>
encoded will be: "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24NCkFsYXJtIElucHV0IENoYW5uZWw"

<b>No Name</b> camera when detect motion send email message (not encoded) in this format:
```
	This is an automatically generated e-mail from your IPC.

		EVENT TYPE: Motion Detected
		EVENT TIME: 27/12/2021 17:42:19
		IPC NAME: IPC
		CHANNEL NUMBER: 01
		IPC IP: 192.168.2.111
```
we need to search for first line: "EVENT TYPE: Motion Detected"<br>

when string it is found script will publish message <b>Alarm</b> in camera named topic: <b>IOT/cctv/XXXX</b><br>
sender-name it is taken from cctv email:
```
From: XXXX@mycctv.local
```
so you can have any nr of cameras sending messages and each camera will have his own topic.

<b>You need to add in python code your MQTT server-ip, user & password.</b><br>
Modify the script as appropriate.<br>

## Installation it is for Python >3.6
Simply run:
> pip install aiosmtpd

As the python code runs in TLS authentication mode (as most cameras need it), you need to parse a openssl *cert.pem* and *key.pem* file.
If you want to use an unsecure, self generated one for your localhost (recommended for this purpose in local network), execute the following command in Terminal in your working directory (not in Python Console, in the proper Terminal!):
> openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 9989 -nodes -subj '/CN=localhost'

## Config of the mail client (e.g. your IP Camera)

This python code can run on Raspberry Pi. Simply add the IP address of your Raspberry Pi and the port usede in the Python code (*here 8025*) to you camera. You can use any email adresses as it does not matter - the mail stays local in your network.<br>
However first part of camera email address is important as it is used to identify the camera and post MQTT alert in that camera topic for each camera, so try to use something  like: <b> IPC01</b>@mycctv.local, <b> IPC02</b>@mycctv.local... <b> IPC99</b>@mycctv.local<br>
The script now will check only if the domain name match <b>@mycctv.local</b> - <i>this can be modified by you in the python code</i>).<br>
If you want to use proper authentication, python code need to be changed: set user name and password and uncomment the part in the python to check whether it matches...

![image](https://user-images.githubusercontent.com/60820820/157892840-d9d2045c-9fda-4b00-ad12-ed7580f92a9b.png)

----
## Home Assistant - optional
you need to create binary sensor motion for every camera<br>
There is no need to send message when Alarm is off because the sensor created will auto change state to off after 60s
```
# CCTV EZIP08 Alarm
- platform: mqtt
  state_topic: "IOT/cctv/ez08"
  name: "CCTV-EZ08"
  off_delay: 60
  payload_on: "Alarm"
  unique_id: 333-00000000844444444444
  device_class: motion
  ```
![Home Assistant motion sensors ](https://github.com/rapi3/mqtt-email/blob/main/Screenshot_2021-12-22_20-19-55.png)

<sub>Tags: CCTV, Dahua, MQTT, email, IOT, Tasmota</sub>
