# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open(textfile, 'rb')
# Create a text/plain message
msg = MIMEText('test')
fp.close()

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents ' 
msg['From'] = 'fraferra@cisco.com'
msg['To'] = 'elbowen@cisco.com'

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail('fraferra@cisco.com', ['elbowen@cisco.com'], msg.as_string())
s.quit()