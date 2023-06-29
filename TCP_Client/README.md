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
