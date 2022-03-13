# mqtt-email-srv

This repo offers a script to have a local mail server available for cctv and post a mqtt message for an incoming mail from cctv.

## Use-Cases:

IP-Cameras (e.g. Dahua, InStar, ...) often can send mails when an alarm is triggered. They are not able to post an http request.
A Mail can be useful to see it on your smartphone but there is always a lag of time due to a long delivery time. 
Let's assume you want to switch on the light of your smart home based on the cameras alert - far to slow.

With this script you run a local mail server. The Ip Camera will send a mail immediately (lag of 0.01 s) and you can directly convert it to a mqtt message.

Modify the script as appropriate.

## Installation
Simply run:
> pip install aiosmtpd

As the script runs in TLS authentication mode (as most cameras need it), you need to parse a openssl *cert.pem* and *key.pem* file. If you want to use an unsecure, self generated one for your localhost (recommended for this purpose in local network), execute the following command in Terminal in your working directory (not in Python Console, in the proper Terminal!):
> openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'

## Config of the mail client (e.g. your IP Camera)

I am running the python script on a Raspberry Pi. Simply add the IP address of your Raspberry Pi and the port of the Python script (*here 8025*) to you camera. You can use any dummy mail adresses as it does not matter - the mail stays local in your network. If you want to use proper authentication (I just use a dummy one), set user name and password and uncomment the part in the python script to check whether it matches.

![image](https://user-images.githubusercontent.com/60820820/157892840-d9d2045c-9fda-4b00-ad12-ed7580f92a9b.png)


## Thanks
Thanks to MyDaHua of ipcamtalk for the idea! https://ipcamtalk.com/threads/send-http-request-if-alarm-dahua-ipc-hfw5442e-ze.62080/#post-647785


<sub>Tags: KNX, Kamera, Request, HTTP Request, Server, API </sub>
