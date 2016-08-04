from oe_daemonutils.dossierservice import MasterdataNotFoundException


class DaemonProcessor(object):
    def __init__(self, settings, logger, system_token, service):
        self.settings = settings
        self.logger = logger
        self.system_token = system_token
        self.notifications_dict = {}
        self.service = service(self.settings, self.logger, self.system_token)

    def process_entry(self, entry):
        """
        Common method to create a dossier from an entry
        Keep track of the entry to notify the persons concerned

        :param entry: entry to process
        """
        self.logger.info('Processing entry {0}'.format(entry.id))
        print('Processing entry {0}'.format(entry.id))
        try:
            self.service.create_dossier(entry, self.notifications_dict)
        except MasterdataNotFoundException as e:
            self.logger.warn(e.__str__())

    def notify(self):
        """
        abstract method to notify by sending emails

        """
        pass
