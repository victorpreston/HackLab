#!/usr/bin/env python2
import threading as thread;
import paramiko as ssh;
import subprocess as sub;

def sshCommand(ip, user, passwd, command):
    client = ssh.SSHClient();

    # For SSH-key connection
    # client.load_host_keys('/home/stick/.ssh/know_hosts');
    
    # Accept the SSH-Key
    client.set_missing_host_key_policy(ssh.AutoAddPolicy());

    client.connect(ip, username=user, password=passwd);
    session = client.get_transport().open_session();
    if session.active:
        session.exec_command(command);
        print session.recv(1024);
    return;

# [host], [username], [password], [command]
sshCommand('','','','');
