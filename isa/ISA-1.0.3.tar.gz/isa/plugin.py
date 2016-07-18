class Plugin:
    def collect(self, server):
        """
        Collect results using the plugin and give back a list of dictionaries where all dictionaries have the same keys.

        :param: server SSHServer object which is used to execute commands on
        :return: list of dictionaries
        """
        raise Exception("Method 'collect' of this plugin is not implemented")