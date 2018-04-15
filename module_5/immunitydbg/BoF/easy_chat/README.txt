Due to the recent security update of microsoft windows xp service pack 3


There has been implementations against the type of attack that binds a shell at a port

that has a return execution call to the structured exception handler (seh), thus preventing
seh based buffer overflow attacks. 

Using the attack.py script, I was able to see an open port on 4444 for the tcp shell
However using netcat on our attacker machine I cannot connect properly. 

It would crash our easy server on the victim pc, and the error code is from module hungapp
which is a security implemenation of ms-windows. So I assumed that was the reason why the payload 
did not execute properly.


Luckily there will be no seh based BoF attack on the OSCP, at least years ago they didn't.
