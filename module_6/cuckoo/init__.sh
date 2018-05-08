#!/usr/bin/bash

# reverse from tutorial because we already have a rule in our forward chain, and we can just set it on the bottom of rules
# aka check these rules first

# poking a hole for mongodb connection
sudo iptables -I INPUT 3 -m state --state NEW -m tcp -p tcp --dport 27017 -j ACCEPT

# poking a hole for web interface, at localhost port 8000
sudo iptables -I INPUT 3 -m tcp -p tcp --dport 8000 -j ACCEPT

# forwarding any established tracked connection
sudo iptables -I FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# forwarding any new connection coming from virtual subnet and going to virtual interface and to be forwarded to our wifi interface
sudo iptables -I FORWARD -o wlp0s20u9u2 -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT

# making sure that all connection coming from our virtual network to be masked by fedora host ip 192.168.1.30, acting as router
sudo iptables -A POSTROUTING -t nat -j MASQUERADE

echo "[!] All the iptables rules have added temporarily"
echo "[!] Please reboot the system once done with cuckoo to restore configured strict firewall rules"

# enabling ip forward
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "[!] ip forward has been enabled, please reboot the system to restore default 0"


