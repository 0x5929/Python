_________________________________________________________________________________________________________________________________________________

					HOW TO RUN CUCKOO IN CMDLINE & WEB INTERFACE
-------------------------------------------------------------------------------------------------------------------------------------------------


[1] Please run the init__.sh script with a prepending sudo first

[2] init__.sh will set up iptables config to start a virtual network 

[3] Please start up mongodb database as cuckoo needs a running db server in back: systemctl start mongod

[4] Then make sure the virtual machine that uses vboxnet0 is turned on, resulting turning on vboxnet0 interface

			| cuckoo should be globally installed, now we can run it anywhere on our system |

[!] run commandline interface: cuckoo
[!] run web interface: cuckoo web runserver localhost:8000

NOTE: there is a cuckoo hidden directory with all of its configuration settings in the home directory call: .cuckoo


Please restart system after all analysis is complete, in order to restore original strict firewall settings
