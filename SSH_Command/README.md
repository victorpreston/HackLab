### SSH Command
Fire off a quick command against a SSH host, that you already have the right credentials. 

This requires you to have the `Paramiko` package installed - do so with your package-manager (preferred) or with `pip` ex.

    $ sudo pacman -S python3-paramiko

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

    $ sudo pacman -S python3-paramiko
    
Note that you'll have to pass along a SSH-Key in the server file. You could use this [Paramiko test key](https://github.com/paramiko/paramiko/blob/master/demos/test_rsa.key) if you feel lazy.

There's no example for this one (didn't want to be bothered firing up a Windows machine), but the idea is that you fire up a cmd window (on your Windows system), run the server file and point it to your own SSH server - Change the IP and Port accordingly;

    $ sshServer.py 192.168.0.1 22
    
Now edit the `sshReverseCmd.py` (last line) with the Credentials for your own SSH server, and run it - This will be acting as our client; 

    $ sshReverseCmd.py

