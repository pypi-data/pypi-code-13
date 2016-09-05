import sys
import xerox
from getpass import getpass
from crypt_keeper import crypt, Keeper

try:
    input = raw_input
except NameError:
    pass

def get_master_key(keeper, master_password):
    if 'salt' not in keeper:
        salt = crypt.random_salt()
        keeper['salt'] = salt
        keeper['accounts'] = {}
    else:
        salt = keeper['salt']
    return crypt.derive_key(master_password, salt)

def get_secure_key(keeper, master_key):
    if 'key' not in keeper:
        key = crypt.random_key()
        iv = crypt.random_iv()
        tag, keeper['key'] = crypt.encrypt_aes_gcm(
            key=master_key,
            iv=iv,
            plaintext=key
        )
        keeper['iv'] = iv
        keeper['tag'] = tag
    else:
        iv = keeper['iv']
        tag = keeper['tag']
        key = crypt.decrypt_aes_gcm(
            key=master_key,
            iv=iv,
            tag=tag,
            ciphertext=keeper['key']
        )
    return key

def set_password(keeper, key, account, password):
    iv = crypt.random_iv()
    pw = crypt.encrypt_aes_cbc(
        key=key,
        iv=iv,
        plaintext=crypt.pad(password.encode('utf8'))
    )
    keeper['accounts'][account] = {
        'iv': iv,
        'pw': pw
    }

def get_password(keeper, key, account):
    entry = keeper['accounts'][account]
    iv = entry['iv']
    pw = entry['pw']
    return crypt.unpad(crypt.decrypt_aes_cbc(
        key=key,
        iv=iv,
        ciphertext=pw
    )).decode('utf8')

def help():
    print('crypt_keeper commands:')
    print('')
    print('    new  -- Generate new password')
    print('    get  -- Get password')
    print('    set  -- Set password')
    print('    list -- List accounts')

def main(cmd, *args):
    keeper = Keeper('safe.db')
    master_password = getpass('Master password: ')
    master_key = get_master_key(keeper, master_password)
    try:
        key = get_secure_key(keeper, master_key)
    except crypt.InvalidTag:
        print('password incorrect')
        return
    if cmd == 'new':
        account = input('Account: ')
        password = crypt.random_password()
        set_password(keeper, key, account, password)
        xerox.copy(password)
        print('\ncopied to clipboard')
    elif cmd == 'get':
        account = input('Account: ')
        if account not in keeper['accounts']:
            print('no account found')
            return
        password = get_password(keeper, key, account)
        xerox.copy(password)
        print('\ncopied to clipboard')
    elif cmd == 'set':
        account = input('Account: ')
        password = getpass('Password: ')
        set_password(keeper, key, account, password)
    elif cmd == 'list':
        print('')
        for account in keeper['accounts']:
            print(account)
    elif cmd == 'help':
        help()

if len(sys.argv) > 1:
    main(sys.argv[1], *sys.argv[2:])
else:
    help()