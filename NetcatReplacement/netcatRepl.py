#!/usr/bin/env python2
import sys;
import socket;
import getopt;
import threading as thread;
import subprocess as sub;

listen      = False;
command     = False;
upload      = False;
execute     = "";
target      = "";
upload_dest = "";
port        = 0;

# Help (options) 
def usage():
    print "Netcat Replacement Tool";
    print
    print "Use with: netcatRepl.py -t target_host -p target_port";
    print "-l --listen listen on [host]:[port] for incomming connections";
    print "-e --execute=file_to_run to execute a given file on receiving a connection";
    print "-c --command initialize a command shell";
    print "-u --upload=destination to upload a file on receiving a connection";
    print 
    print 
    print "Examples: ";
    print "netcatRepl.py -t 192.168.0.1 -p 5555 -l -c";
    print "netcatRepl.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe";
    print "netcatRepl.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"";
    print "echo 'Hello World' | ./netcatRepl.py -t 192.168.0.1 -p 5555";
    sys.exit(0);

# Client 
def clientSender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    try:
        client.connect((target, port));
        if len(buffer):
            client.send(buffer);

        while True:
            recv_len = 1;
            answer   = "";

            while recv_len:
                data     = client.recv(4096);
                recv_len = len(data);
                answer  += data;

                if recv_len < 4096:
                    break;

            print answer,

            buffer = raw_input("");
            buffer+= "\n";
            client.send(buffer);
    except:
        raise
        client.close();

# Listener
def serverLoop():
    global target;

    # If target is not set, listen to all devices
    if not len(target):
        target = "0.0.0.0";

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    server.bind((target, port));
    server.listen(5);

    while True:
        client_socket, addr = server.accept();
        client_thread = thread.Thread(target=clientHandler, args=(client_socket,));
        client_thread.start();

# Commands
def runCommand(command):
    command = command.rstrip();

    try:
        output = sub.check_output(command, stderr=sub.STDOUT, shell=True);
    except:
        output = "Failed to execute command.\r\n";

    return output;

# Logic for upload, execution and shell
def clientHandler(client_socket):
    global upload
    global execute
    global command

    # Check for upload
    if len(upload_dest):
        file_buffer = "";
        while True:
            data = client_socket.recv(1024);
            if not data:
                break;
            else:
                file_buffer += data;

        try:
            file_desc = open(upload_dest, "wb");
            file_desc.write(file_buffer);
            file_desc.close();
            client_socket.send("File saved to %s\r\n" % upload_dest);
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_dest);

    # Check for command execution
    if len(execute):
        output = runCommand(execute);
        client_socket.send(output);

    # Check for command shell
    if command:
        while True:
            client_socket.send("netcatRepl:# ");
            cmd_buffer = "";
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024);

            response = runCommand(cmd_buffer);
            client_socket.send(response);

def main():
    global listen;
    global port;
    global execute;
    global command;
    global upload_dest;
    global target;

    if not len(sys.argv[1:]):
        usage();

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"]);
    except getopt.GetoptError as eRR:
        print str(eRR);
        usage();

    for o,a in opts:
        if o in ("-h", "--help"):
            usage();
        elif o in ("-l", "--listen"):
            listen = True;
        elif o in ("-e", "--execute"):
            execute = a;
        elif o in ("-c", "--command"):
            command = True;
        elif o in ("-u", "--upload"):
            upload_dest = a;
        elif o in ("-t", "--target"):
            target = a;
        elif o in ("-p", "--port"):
            port = int(a);
        else:
            assert False, "Unknown Option";

    if not listen and len(target) and port > 0:
        # Blocking - use CTRL-D if not sending input
        buffer = sys.stdin.read();
        clientSender(buffer);

    if listen:
        serverLoop();

main();