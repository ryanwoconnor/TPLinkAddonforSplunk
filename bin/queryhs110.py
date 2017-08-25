import unicodedata
import socket   #for sockets
import sys  #for exit
import struct
import time
import StringIO

def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    #join all parts to make final string
    return ''.join(total_data)

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

print 'Socket Created'


keys_dict = {}

try:
    get_path = '/servicesNS/nobody/TPLinkAddonforSplunk/storage/passwords?output_mode=json'
    serverResponse = splunk.rest.simpleRequest(get_path, sessionKey=sessionKey, method='GET',
                                               raiseAllErrors=True)

    jsonObj = json.loads(serverResponse[1])

    my_app = "TPLinkAddonforSplunk"

    if len(jsonObj['entry']) == 0:
        logger.warn("No credentials found.")
        sleep(60)
        sys.exit(0)
    else:
        for entry in jsonObj['entry']:
            if entry['acl']['app'] != my_app:
                continue
            if 'clear_password' in entry['content'] and 'username' in entry['content']:
                keys_dict[entry['content']['username']] = entry['content']['clear_password']


except Exception, e:
    raise Exception("Could not GET credentials: %s" % (str(e)))

for apiKeyName, apiKeyVal in keys_dict.iteritems():
    try:
        remote_ip = socket.gethostbyname( apiKeyVal )
    except socket.gaierror:
        #could not resolve
        print 'Hostname could not be resolved. Exiting'
        sys.exit()
    
for apiKeyName, apiKeyVal in keys_dict.iteritems(): 
    #Connect to remote server
    s.connect((remote_ip , port))
 
    print 'Socket Connected to ' + host + ' on ip ' + remote_ip
 
    #Send some data to remote server
    message = "AAAAJNDw0rfav8uu3P7Ev5+92r/LlOaD4o76k/6buYPtmPSYuMXlmA==".decode('base64')
 
    try :
        #Set the whole string
        s.sendall(message)
    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()
 
    print 'Message sent successfully'
 
    #get reply and print
    ciphertext = recv_timeout(s)

    #Decode Response
    key = 171
    buffer = []

    ciphertext = ciphertext.decode('latin-1')
    plaintext=''
    for char in ciphertext:
        plain = key ^ ord(char)
        key = ord(char)
        buffer.append(chr(plain))
        plaintext = ''.join(buffer)

    #print response
    print plaintext[5:]
#Close the socket
s.close()
