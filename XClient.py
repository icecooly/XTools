#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import sys
import re
import pexpect
import struct,fcntl,signal
import termios
from Host import *
from XComm import *

X_PROMPT = ['#','$','>','\$','>>>']


class XClient:
    host=None
    child=None
    #
    def __init__(self, host):
        self.host=host

    def sendCommand(self,child, cmd, expect=None):
        child.sendline(cmd)
        if expect != None:
            child.expect(expect)

    def sigwinch_passthrough (self,sig, data):
    	winsize = self.getwinsize()
    	self.child.setwinsize(winsize[0],winsize[1])

    def getwinsize(self):
    	"""This returns the window size of the child tty.
    	The return value is a tuple of (rows, cols).
    	"""
    	if 'TIOCGWINSZ' in dir(termios):
        	TIOCGWINSZ = termios.TIOCGWINSZ
    	else:
        	TIOCGWINSZ = 1074295912 # Assume
    	s = struct.pack('HHHH', 0, 0, 0, 0)
    	x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    	return struct.unpack('HHHH', x)[0:2]

    def login(self):
        command = 'ssh -o ServerAliveInterval=60 ' + self.host.user + '@' + self.host.host + ' -p ' + self.host.port
        logDebug('%s'%command)
        self.child = pexpect.spawn(command)
        ret = self.child.expect([pexpect.TIMEOUT, 'Are you sure you want to continue connecting', '[p]assword:'])
        if ret == 0:
            logError('[-] Error Connecting')
            return
        if ret == 1:
            self.child.sendline('yes')
            ret = self.child.expect([pexpect.TIMEOUT, '[p|P]assword'])
            if ret == 0:
                logError('[-] Error Connecting')
                return
            if ret == 1:
                return self.sendPassword()
        if ret == 2:
            return self.sendPassword()
        return self.child

    def sendPassword(self):
        self.sendCommand(self.child,self.host.password, X_PROMPT)
        signal.signal(signal.SIGWINCH, self.sigwinch_passthrough)
        winsize = self.getwinsize();
        self.child.setwinsize(winsize[0], winsize[1])
        self.child.interact()
        return self.child

    def run(self,command):
        loginCmd = 'ssh -o ServerAliveInterval=60 ' + self.host.user + '@' + self.host.host + ' -p ' + self.host.port
        self.child = pexpect.spawn(loginCmd)
        ret = self.child.expect([pexpect.TIMEOUT, 'Are you sure you want to continue connecting', '[p]assword:'])
        if ret == 0:
            logError('[-] Error Connecting')
            return
        if ret == 1:
            self.child.sendline('yes')
            ret = self.child.expect([pexpect.TIMEOUT, '[p|P]assword'])
            if ret == 0:
                logError('[-] Error Connecting')
                return
            if ret == 1:
                self.child.sendline(self.host.password)
        if ret == 2:
            self.child.sendline(self.host.password)
        self.child.expect('\$')
        self.child.sendline(command)
        self.child.expect('\$')
        print(self.child.before.decode('utf-8'))
        self.child.close()

if __name__ == '__main__':
    host = getHostByAlias('dev')
    client = XClient(host)
    client.login()
