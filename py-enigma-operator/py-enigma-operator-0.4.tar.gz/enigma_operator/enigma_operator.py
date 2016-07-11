from datetime import datetime
import os
import random
import string

from enigma.machine import EnigmaMachine


class EnigmaOperator():
    """
    Wrapper for py-enigma encode/decode. Also provides tools for creating
    key sheets and code books.
    """

    def __init__(self, codebuch_path, day=datetime.now().day):
        """Set up an operator with a copy of this month's codebuch."""
        # Get today's rotor settings.
        with open(codebuch_path) as f:
            self.machine = EnigmaMachine.from_key_file(f, day=day)

        # Generate operator grundstellung.
        self.grundstellung = Enigma.random_letters(3)

    def encrypt(self, plaintext):
        """Have the operator encrypt a message."""

        # Encrpyt message key.
        msg_key = Enigma.random_letters(3)
        while msg_key == self.grundstellung:
            msg_key = Enigma.random_letters(3)
        self.machine.set_display(self.grundstellung)
        enc_key = self.machine.process_text(msg_key)

        # Encrpyt message.
        self.machine.set_display(msg_key)
        ciphertext = self.machine.process_text(plaintext)

        # Encode message with keys.
        return "{enc_key}{ciphertext}{grundstellung}".format(
            enc_key=enc_key,
            ciphertext=ciphertext,
            grundstellung=self.grundstellung
        )

    def decrypt(self, ciphertext):
        """Have the operator decrypt a message."""

        # Separate keys from message.
        enc_key = ciphertext[:3]
        message = ciphertext[3:-3]
        grundstellung = ciphertext[-3:]

        # Decrypt message key.
        self.machine.set_display(grundstellung)
        msg_key = self.machine.process_text(enc_key)
        # Decrpyt message.
        self.machine.set_display(msg_key)
        return self.machine.process_text(message)

    @staticmethod
    def random_letters(count):
        """Get a series of pseudo-random letters with no repeats."""
        rv = random.choice(string.ascii_uppercase)
        while len(rv) < count:
            l = random.choice(string.ascii_uppercase)
            if not l in rv:
                rv += l
        return rv

    @staticmethod
    def random_codebuch(path):
        """Generate a month-long codebuch and save it to a file."""

        lines = []
        for i in range(31):
            line = str(i+1) + " "

            # Pick rotors
            all_rotors = ['I', 'II', 'III', 'IV', 'V']
            rotors = [random.choice(all_rotors)]
            while len(rotors) < 3:
                r = random.choice(all_rotors)
                if not r in rotors:
                    rotors.append(r)
                    line += r + ' '

            # Pick rotor settings.
            settings = [str(random.randint(1, 26))]
            while len(settings) < 3:
                s = str(random.randint(1, 26))
                if not s in settings:
                    settings.append(s)
                    line += s + ' '

            # Pick plugboard settings.
            plugboard = []
            while len(plugboard) < 20:
                p1 = Enigma.random_letters(1)
                p2 = Enigma.random_letters(1)
                if (not p1 == p2 and
                   not p1 in plugboard and not p2 in plugboard):
                    plugboard.extend([p1, p2])
                    line += p1 + p2 + ' '

            # Pick a reflector.
            reflector = random.choice(['B', 'C'])
            line += reflector

            line += os.linesep
            lines.append(line)

        with open(path, 'w') as f:
            f.writelines(lines)

        return lines

