from ftw.upgrade import UpgradeStep


class RegisterFixedHeaderScript(UpgradeStep):
    """Register fixed header script.
    """

    def __call__(self):
        self.install_upgrade_profile()
