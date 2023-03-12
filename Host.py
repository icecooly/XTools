#!/usr/bin/python
#-*-coding:utf-8-*-

class Host:
    alias=''
    host=''
    user=''
    password=''
    port='22'

    def __init__(self, alias,host,user,password,port):
        self.alias=alias
        self.host=host
        self.user=user
        self.password=password
        self.port=port

    def __str__(self):
        return self.alias + "\t" + self.host + "\t" + self.user + "\t" + self.password + "\t" + self.port