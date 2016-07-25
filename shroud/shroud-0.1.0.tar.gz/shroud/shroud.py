from __future__ import absolute_import

from os.path import expanduser, isfile

import click
import keyring

from shroud import encryption


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    pass


@click.command()
@click.option('--name', '-n',
              prompt="Name for keypair", default='shroud',
              help="The filename to use for the keys.")
@click.option('--keydir', '-d',
              prompt="Directory to place keys in",
              type=click.Path(exists=True, file_okay=False, writable=True),
              default=expanduser('~') + '/.ssh',
              help="The directory to store the keys in.")
@click.option('--passphrase', '-p',
              prompt="Passphrase for private key", default='',
              hide_input=True, confirmation_prompt=True,
              help="The passphrase for the RSA private key.")
@click.option('--keychain', '-l',
              is_flag=True, default=False,
              help="Load the private key passphrase into the keychain.")
@click.option('--forcewrite', '-f',
              is_flag=True, default=False,
              help="Overwrite existing keyfiles if applicable.")
def generate_keypair(name, keydir, passphrase, keychain, forcewrite):
    if keychain and passphrase != '':
        keyring.set_password('shroud', 'shroud', passphrase)

    pub_filename = '{}/{}.pub'.format(keydir, name)
    priv_filename = '{}/{}'.format(keydir, name)
    if isfile(pub_filename) and not forcewrite:
        click.confirm("{} already exists. Would you like to write over it?"
                      .format(pub_filename), abort=True, default=True)
    if isfile(priv_filename) and not forcewrite:
        click.confirm("{} already exists. Would you like to write over it?"
                      .format(priv_filename), abort=True, default=True)

    click.echo("Generating keypair")
    pub, priv = encryption.generate_rsa_key_pair(passphrase=passphrase)

    click.echo("Storing public key in {}".format(pub_filename))
    with click.open_file(pub_filename, 'wb') as f:
        f.write(pub)
    click.echo("Storing private key in {}".format(priv_filename))
    with click.open_file(priv_filename, 'wb') as f:
        f.write(priv)


@click.command()
@click.option('--passphrase', '-p',
              prompt="Passphrase for private key",
              hide_input=True, confirmation_prompt=True,
              help="The RSA private key passphrase to store in keychain.")
def arm_keychain(passphrase):
    keyring.set_password('shroud', 'shroud', passphrase)


@click.command()
@click.argument('secret')
@click.option('--pubkey', '-k',
              type=click.File('rb'),
              default=expanduser('~') + '/.ssh/shroud.pub',
              help="The public key file to encrypt with.")
@click.option('--secretsfile', '-s',
              type=click.File('ab'),
              default='secrets.txt',
              help="The file to write the encrypted secret to.")
def encrypt(secret, pubkey, secretsfile):
    ciphertext = encryption.encrypt_secret_with_rsa_key(
        secret.encode(), pubkey.read())
    click.echo("Writing encrypted secret to {}".format(secretsfile.name))
    secretsfile.write(ciphertext)


@click.command()
@click.option('--secretsfile', '-s',
              type=click.File('rb'),
              default='secrets.txt',
              help="The file to read the encrypted secrets from.")
@click.option('--privkey', '-k',
              type=click.File('rb'),
              default=expanduser('~') + '/.ssh/shroud',
              help="The private key file to decrypt with.")
@click.option('--passphrase', '-p',
              default=None,
              help="The passphrase for the RSA private key.")
@click.option('--keychain', '-l',
              is_flag=True, default=False,
              help="Load the private key passphrase from keychain. "
                   "Overrides '-p'.")
def decrypt(secretsfile, privkey, passphrase, keychain):
    ciphertext = secretsfile.read()
    private_key = privkey.read()

    if b'ENCRYPTED' in private_key:
        if passphrase is None and not keychain:
            exit("{} is an encrypted private key that requires a passphrase. "
                 "Use the '-p' or '-l' option to proceed."
                 .format(privkey.name))
        elif keychain:
            passphrase = keyring.get_password('shroud', 'shroud')

    decrypted_secrets = list()
    for i in range(len(ciphertext) // 256):
        decrypted_secrets.append(
            encryption.decrypt_secret_with_rsa_key(
                ciphertext[256 * i:256 * i + 256],
                private_key,
                passphrase=passphrase
            ).decode())

    click.echo(', '.join(decrypted_secrets))


cli.add_command(generate_keypair)
cli.add_command(arm_keychain)
cli.add_command(encrypt)
cli.add_command(decrypt)
