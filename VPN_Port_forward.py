import os
import socket
import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


VPN_User =  ''
VPN_Pass = ''
IPADDRESS = get_ip_address('tun0')

os.system('head -n 100 /dev/urandom | md5sum | tr -d " -" > ~/.pia_client_id')


command = 'curl -d "user=' + VPN_User + '&pass=' + VPN_Pass + '&client_id=$(cat ~/.pia_client_id)&local_ip=' + IPADDRESS + '" https://www.privateinternetaccess.com/vpninfo/port_forward_assignment'

output = os.popen(command).read()


port = int(filter(str.isdigit,output))

os.system('zenity --info --text="Your VPN Port is: %d"' % port)