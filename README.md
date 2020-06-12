## PTP calculation demonstration

####Overview

The purpose of this project was to get familiar with PTP operation.
It uses socket API.

It demonstrates time calculation performed by PTP. Counter variables incremented in some time interval are used for the demonstration. In a more realistic case, internal time would need to be used instead and the right PTP frame format. 

Counter value is sent by Master, Client updates its counter value based on calculations of the format analogous to PTP.

####Instructions:

Run Client.py (slave) and master.py at the same time to demo PTP behaviour

####References:

PTP tutorial:
https://www.nist.gov/system/files/documents/el/isd/ieee/tutorial-basic.pdf 