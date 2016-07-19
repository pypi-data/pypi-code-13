from pexpect import pxssh

s = pxssh.pxssh(options={
    'StrictHostKeyChecking': 'no'
})
s.login('lxplus', 'kjacobs', 'knop0602R!')
s.sendline('uptime')
s.prompt()
print(s.before)