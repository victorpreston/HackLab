### Host Scanner
Scan a network for hosts.

First you'd have to figure the local IP of the device you're connected to - something like `ip addr` for Linux, or `ip config` for Windows. Then edit the script (line 11 & 12) with that IP (host) and define what subnet to search (subnet) - ex, .0/24 for the whole subnet.

Run it with root privileges;

    $ sudo python3 hostScanner.py

After just a few seconds you'll begin to get devices that responded to a UDP broadcast.

```
Host Found: 100.103.175.246
Host Found: 100.103.175.253
Host Found: 100.103.175.243
Host Found: 100.103.175.249
```
