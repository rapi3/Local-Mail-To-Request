#!/usr/bin/python3
# install aiosmtpd with:
# pip install aiosmtpd
# generate key for TLS:
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 999 -nodes -subj '/CN=localhost'

import asyncio
import logging
import requests
import ssl
import sys
import re
import paho.mqtt.publish as publish

from aiosmtpd.controller import Controller
from aiosmtpd.handlers import AsyncMessage
from aiosmtpd.smtp import SMTP as Server, syntax
from aiosmtpd.smtp import AuthResult

# define here string to search for camera Alarm
ezip_string = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gU3RhcnQ"
ipc_string = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24NCkFsYXJtIElucHV0IENoYW5uZWw"
gs_string = "EVENT TYPE: Motion Detected"
sender = "name"

class MyController(Controller):
    @staticmethod
    def authenticator_func(server, session, envelope, mechanism, auth_data):
        # For this simple example, we'll ignore other parameters
        # assert isinstance(auth_data, LoginPassword)
        # username = auth_data.login
        # password = auth_data.password
        # # If we're using a set containing tuples of (username, password),
        # # we can simply use `auth_data in auth_set`.
        # # Or you can get fancy and use a full-fledged database to perform
        # # a query :-)
        # if auth_db.get(username) == password
# For debug:        
#        print("authenticator function called")
        return AuthResult(success=True)

    def factory(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain('cert.pem', 'key.pem')
        return Server(self.handler, tls_context=context, authenticator=self.authenticator_func)

class MyMessageHandler(AsyncMessage):
    
# change to accept only emails for your domain here it is defined for: mycctv.local
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith('@mycctv.local'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
# For debug to check email sent by camera:        
#        print('.....Message from %s' % envelope.mail_from)
#        print('.....Message for %s' % envelope.rcpt_tos)
#        print('.....Message data:\n')
#        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
#            print(f'.........> {ln}'.strip())
#        print()
#        print('.....End of message')

# search in email body for camera Alarm string defined up:
        if ezip_string in envelope.content.decode('utf8', errors='replace') or ipc_string in envelope.content.decode('utf8', errors='replace') or gs_string in envelope.content.decode('utf8', errors='replace'):
# find sender name from cctv email name:
          sender = re.search(r".+?(?=\@)", envelope.mail_from)
          sender = sender.group()
# execute MQTT for camera:
          publish.single('IOT/cctv/{}'.format(sender), "Alarm", hostname="your.mqtt.server.ip", client_id="mqtt-email", auth = {'username':"your_mqtt_user", 'password':"your_mqtt_pass"})
# For debug:
#          print('.....Debug sender: ', sender)
#          print('.....Debug EXECUTE MQTT !')
        return '250 Message accepted for delivery'

async def amain(loop):
    cont = MyController(MyMessageHandler(), hostname='', port=8025)
    cont.start()

if __name__ == '__main__':
# For debug:    
#    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop=loop))
    print(".....Starting Job.....")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
