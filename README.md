# blackhatPython
A set of network tools for your hacking delight. 

These tools are created with the help of "Blackhat Python: Python Programming for Hackers and Pentesters". 

Often when you're connected to a server, you don't necessarily have the right tools at hand. Experienced system administrators often removes packages like `netcat` - and you can forget all about `Wireshark`. Luckily we often find the `Python` package to be installed on such servers, though, and that's where these tools come in handy - a replacement for typical needed network tools. 

## Table of Content
* [Host Scanner](#host-scanner)
* [Netcat Replacement](#netcat-replacement)
* [SSH Command](#ssh-command)
* [SSH Reverse](#ssh-reverse)
* [TCP Client and Server](#tcp-client-and-server)
* [TCP Proxy](#tcp-proxy)
* [UDP Client](#udp-client)

<br><br>
### Host Scanner
Scan a network for hosts.

First you'd have to figure the local IP of the device you're connected to - something like `ip addr` for Linux, or `ip config` for Windows. Then edit the script (line 11 & 12) with that IP (host) and define what subnet to search (subnet) - ex, .0/24 for the whole subnet.

Run it with root privileges;

    $ sudo python2 hostScanner.py

After just a few seconds you'll begin to get devices that responded to a UDP broadcast.

```
Host Found: 100.103.175.246
Host Found: 100.103.175.253
Host Found: 100.103.175.243
Host Found: 100.103.175.249
```

<br><br>
### Netcap Replacement
Netcat (NC) is a popular network tool, which in some cases might be completly removed from remote servers. In that case might come in handy to have some simple NC functionality, such as pushing files, executing commands or initializing a shell. 

Run it with `-h` to get a full set of option and examples;

```
Netcat Replacement Tool

Use with: netcatRepl.py -t target_host -p target_port
-l --listen listen on [host]:[port] for incomming connections
-e --execute=file_to_run to execute a given file on receiving a connection
-c --command initialize a command shell
-u --upload=destination to upload a file on receiving a connection


Examples: 
netcatRepl.py -t 192.168.0.1 -p 5555 -l -c
netcatRepl.py -t 192.168.0.1 -p 5555 -l -u=c:\target.exe
netcatRepl.py -t 192.168.0.1 -p 5555 -l -e="cat /etc/passwd"
echo 'Hello World' | ./netcatRepl.py -t 192.168.0.1 -p 5555
```

You can test it locally by first firing up a listener;

    $ ./netcatRepl.py -l -p 9999 -c
    
The `-c` will initialize a command shell for the client machine. Then fire up a second replacement tool, without the listener;

    $ ./netcatRepl.py -t localhost -p 9999
    
On your client, hit `CTRL-D` to interact with the "server" which initializes the command shell;

```
netcatRepl:#  ls ~
Desktop
Documents
Downloads
Dropbox
Music
Pictures
Projects
Public
Templates
Videos
bin
dotfiles
makepkg
```

<br><br>
### SSH Command
Fire off a quick command against a SSH host, that you already have the right credentials. 

This requires you to have the `Paramiko` package installed - do so with your package-manager (preferred) or with `pip` ex.

    $ sudo pacman -S python2-paramiko

First define your SSH Host, Credentials and Command at the last line in this script. My test server is called `serv` and I'll be running the command `id` - Change the IP accordingly;

```
sshCommand('192.168.0.1','serv','PASSWORD','id');
```

Then run it through your glorious system;

```
$ ./sshCommand.py 
uid=1000(serv) gid=1000(serv) groups=1000(serv),10(wheel)
```

<br><br>
### SSH Reverse
Windows doesn't come with SSH out the box, but we'd often like out communication encryption anyways. We can do this by reversing the communication, such as we'll be sending commands from our SSH server to a simple SSH client we set up on the Windows machine. 

We'll be using `sshServer.py` and `sshReverseCmd.py` for this magic. 

This requires you to have the `Paramiko` package installed - do so with your package-manager (preferred) or with `pip` ex.

    $ sudo pacman -S python2-paramiko
    
Note that you'll have to pass along a SSH-Key in the server file. You could use this [Paramiko test key](https://github.com/paramiko/paramiko/blob/master/demos/test_rsa.key) if you feel lazy.

There's no example for this one (didn't want to be bothered firing up a Windows machine), but the idea is that you fire up a cmd window (on your Windows system), run the server file and point it to your own SSH server - Change the IP and Port accordingly;

    $ sshServer.py 192.168.0.1 22
    
Now edit the `sshReverseCmd.py` (last line) with the Credentials for your own SSH server, and run it - This will be acting as our client; 

    $ sshReverseCmd.py

<br><br>
### TCP Client and Server
A simple example of a TCP client/server communication. This could'nt be more fitting, since we've have just been working with socket programming in my CS class. 

Define the IP and Port in the `tcpServer.py` on line 5 & 6 - By default it will bind to all devices (0.0.0.0) and listen on port 9999.


Now, edit the `tcpClient.py` on line 4 & 5 to target the listening server and port. Also edit your request on line 12. This can be done in a test our test-environment;

Now fire up the server and your client (make the request);

```
$ ./tcpServer.py 
[*] Listening on 0.0.0.0:9999
Connection accepted from: 127.0.0.1:49854
[*] Received: Hello World
```

```
$ ./tcpClient.py
ACK!
```

The server only responds with `ACK!`, but you can easily expand this simple concept with your own returns.

<br><br>
### TCP Proxy
Read trafic data to get a better understanding of the applications using the protocol with the `tcpProxy.py`. A nice little test would be to point it at a ftp server. We'll test it on our localhost along with a FTP server that makes sense to you - Port 21 is priviledges, so run it with `sudo`;

```
$ sudo ./tcpProxy.py localhost 21 ftp.SERVER.com 21 True
[*] Listening on localhost:21
```

Now fire up your FTP application and point it to `localhost` at port `21` and connect.

```
[==>] Received connection from 127.0.0.1:53230
0000 32 32 30 20 57 65 6C 63 6F 6D 65 20 74 6F 20 6C  220 Welcome to l
0010 69 6E 75 78 31 34 2E 75 6E 6F 65 75 72 6F 2E 63  inux14.unoeuro.c
0020 6F 6D 2E 20 54 4C 53 20 69 73 20 73 75 70 70 6F  om. TLS is suppo
0030 72 74 65 64 2E 0D 0A                             rted...
[<==] Sending 55 bytes to localhost.
[==>] Received 10 bytes from localhost.
0000 41 55 54 48 20 54 4C 53 0D 0A                    AUTH TLS..
[==>] Sent to remote.
[<==] Received 25 bytes from remote.
0000 32 33 34 20 41 55 54 48 20 54 4C 53 20 73 75 63  234 AUTH TLS suc
0010 63 65 73 73 66 75 6C 0D 0A                       cessful..
[<==] Sent to localhost.
[*] No more data. Closing connection.
```

<br><br>
### UDP Client
Just as our TCP client, the UDP client isn't much different. Define a target IP and Port at line 4 & 5. The UDP client will fire off a message defined at line 9 and wait for the reponse.  
