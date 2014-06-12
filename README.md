USAGE
======

from chikka import Chikka

c = Chikka(client_id=CLIENT_ID, secret_key=SECRET_KEY, shortcode=SHORTCODE)

c.send('09991234567', 'Mensahe mo')


Before sending your message you can define a message_id
if you do not supply a message_id a random message_id will
be generated 

c.send('09991234567', 'Mensahe mo na may message id', message_id='1234567890')



