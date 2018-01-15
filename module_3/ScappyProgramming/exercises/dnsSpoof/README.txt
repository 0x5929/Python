TO RUN THIS EXERCISE, JUST RUN THE dnsspoof.py FILE. 


we sniffed the packet from my host computer to my router on port 53, 
we then switched up the destination and source ip and port, to reverse the direction of the packet
however this creates a problem, because its a race between my spoofed packet and the dns response from my router port 53
so whichever one comes up reaches my host computer's destination port first will be cached into my browser from its resposne. 
and EVERYTIME the router wins.. but we technically did spoofed the dns packet, it just arrived a little later


in order to solve this problem, we need to mess with the iptables and the firewall configuration within my python code, 
see the comments in the dnsspoof.py file and look for the reference website. 

within the reference website, the author wrote about a program which I cannot find in my fedora repositories. this program can be import
as a module in python, along with scapy.all . this program can manipulate the iptables and firewall settings along with the os module. 
after the packet coming from port 53 of my router ip will be blocked and denied. for the swole reason of dns spoofing, now the victim
can only recieve my spoofed dns response, misleading the browswer to cache my redirected ip which can lead to malicious sites. 


