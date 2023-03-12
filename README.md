# XTools

* 免密码自动登录ssh
* 批量免密码scp

安装(基于python3)
--------

1.安装pexpect
pip install pexpect

2.保存XTools到
/Users/xxxx/tools/XTools

3.修改~/.bash_profile 增加
```shell
export XTOOLS_HOME=/Users/xxxx/tools/XTools
PATH=$PATH:$XTOOLS_HOME
export PATH
```

4.XTools目录增加hosts.txt
```shell
#alias 		ip/host		user		password	port	
dev		131.x.x.x	root		111111		22
prd		132.x.x.x	root		111111		22
```

5.自动登录xssh dev,就这么简单
