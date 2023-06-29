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
