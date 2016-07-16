
import threading
import time
import os.path

import wayround_org.utils.shlex
import wayround_org.toxcorebind.tox
import wayround_org.utils.program


class Bot:

    def __init__(
            self,
            commands,
            savedata_file,
            name=b'Bot',
            status_message=b'description',
            bootstrap_hosts=None
            ):

        if not isinstance(savedata_file, str):
            raise TypeError("`status_save_file' must be str")

        self._commands = commands
        self._tox = None
        self._start_stop_lock = threading.Lock()

        self._name = name
        self._status_message = status_message

        if bootstrap_hosts is None:
            bootstrap_hosts = \
                wayround_org.toxcorebind.tox.get_std_bootstrap_hosts()

        self._bootstrap_hosts = bootstrap_hosts
        self._savedata_file = savedata_file

        self._stop_flag = True

        self._job_thread = None

        return

    def start(self):

        error = None

        with self._start_stop_lock:
            if self._tox is None:

                self._stop_flag = False

                options, error = wayround_org.toxcorebind.tox.Tox_Options.new()

                if (self._savedata_file is not None
                        and os.path.isfile(self._savedata_file)):

                    options.savedata_type = \
                        wayround_org.toxcorebind.tox.TOX_SAVEDATA_TYPE_TOX_SAVE

                    with open(self._savedata_file, 'rb') as f:
                        options.savedata_data = f.read()

                tox, error = wayround_org.toxcorebind.tox.Tox.new(
                    options=options
                    )
                if error == 0:
                    self._tox = tox
                    self._tox.self_set_name(self._name)
                    self._tox.self_set_status_message(self._status_message)

                    self._tox.callback_friend_request(self._friend_request_cb)
                    self._tox.callback_friend_message(self._friend_message_cb)
                    self._tox.callback_self_connection_status(
                        self._connection_status
                        )

                    for i in self._bootstrap_hosts:
                        _r = self._tox.bootstrap(*i)
                        del _r

                    self._job_thread = threading.Thread(
                        target=self._job_thread_meth
                        )
                    self._job_thread.start()
                else:
                    print("error starting bot. tox error id: {}".format(error))

        return error

    def stop(self):
        with self._start_stop_lock:
            if self._tox is not None:
                self._stop_flag = True
                self._job_thread.join()
                if self._savedata_file is not None:
                    savedata = self._tox.get_savedata()
                    with open(self._savedata_file, 'wb') as f:
                        f.write(savedata)
                    del savedata
                self._tox.kill()
                self._tox = None
        return

    def _job_thread_meth(self):
        while True:
            if self._stop_flag:
                break
            self._tox.iterate()
            time.sleep(self._tox.iteration_interval() / 1000)
        return

    def get_address(self):
        ret = None
        if self._tox is not None:
            ret = self._tox.self_get_address()
        return ret

    def _friend_request_cb(self, obj, public_key, message):
        # if public_key in self._admin_keys:
        print("got friend request")
        r = self._tox.friend_add_norequest(public_key)
        self._tox.friend_send_message(
            r[0],
            0,
            b'Hello! This is bot. Wellcome! You have been added as a friend.'
            )
        print("answered friend request")
        return

    def _friend_message_cb(self, obj, friend_number, type_, message):
        threading.Thread(
            target=self._friend_message_cb_t,
            args=(obj, friend_number, type_, message,)
            ).start()
        return

    def _friend_message_cb_t(self, obj, friend_number, type_, message):
        print("got message")
        cmd_line = wayround_org.utils.shlex.split(
            str(message, 'utf-8').splitlines()[0]
            )

        if len(cmd_line) == 0:
            pass
        else:

            messages = []
            asker_addr = self._tox.friend_get_public_key(friend_number)

            res = wayround_org.utils.program.command_processor(
                command_name=None,
                commands=self._commands,
                opts_and_args_list=cmd_line,
                additional_data={
                    'asker_addr': asker_addr,
                    'messages': messages
                    }
                )

            messages_text = ''

            for i in messages:

                typ = i['type']
                text = i['text']

                typ_text = ''
                if typ not in [
                        'plain', 'text', 'simple',
                        'warning', 'info', 'error'
                        ]:
                    raise ValueError("invalid message `type' value")

                if typ not in ['plain', 'text', 'simple']:
                    typ_text = '[{typ}]: '.format(typ=typ)

                messages_text += '{typ_text}{text}\n'.format(
                    typ_text=typ_text,
                    text=text
                    )

            if 'main_message' in res and res['main_message']:
                messages_text += '{}\n'.format(res['main_message'])

            messages_text += 'Exit Code: {} ({})\n'.format(
                res['code'],
                res['message']
                )

            self._tox.friend_send_message(
                friend_number,
                0,
                bytes(messages_text, 'utf-8')
                )
        return

    def _connection_status(self, obj, connection_status):

        csn = None

        if connection_status == wayround_org.toxcorebind.tox.TOX_CONNECTION_NONE:
            csn = 'NONE'
        elif connection_status == wayround_org.toxcorebind.tox.TOX_CONNECTION_UDP:
            csn = 'UDP'
        elif connection_status == wayround_org.toxcorebind.tox.TOX_CONNECTION_TCP:
            csn = 'TCP'
        else:
            csn = 'ERROR'
        print("connection status now is: {}".format(csn))
        return
