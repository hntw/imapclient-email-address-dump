from imapclient import IMAPClient
import pyzmail

HOST = 'your-host'
USERNAME = 'your-email'
PASSWORD = 'your-supersecret-password'
ssl = True # You are using SSL, right?
port = 993 # When SSL is true, IMAPClient defaults to 143

server = IMAPClient(HOST, port=port,use_uid=True, ssl=ssl)
server.login(USERNAME,PASSWORD)

# Select the folder you want to extract email addresses from
select_info = server.select_folder('INBOX')

# Pull back the message IDs you'd like to grab, in this case everything that is not deleted
messages = server.search(['NOT DELETED'])

# Retrieve the messages
# Note: this pulls back just about everything and can take awhile with a big mailbox
responses = server.fetch(messages,['BODY[]'])

# Loop through the messages and parse them out with the pyzmail library
addresses = []
for response in responses:
    if response > 0:
        message = pyzmail.PyzMessage.factory(responses[response]['BODY[]'])
        addresses.append(message.get_addresses('from')[0][1])

# Boil the list down to a unique set
unique_addresses = set(addresses)

# Log out of the server
server.logout()

# Dump the unique list to a file with an unoriginal name
f = open('uniques','w')
for address in unique_addresses:
    f.write(address)
    f.write('\n')
    f.flush()

f.close()
