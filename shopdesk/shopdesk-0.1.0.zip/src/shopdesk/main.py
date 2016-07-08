#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

from shopdesk import scheduler

class ShopdeskApp(appier.WebApp):

    def __init__(self, *args, **kwargs):
        appier.WebApp.__init__(
            self,
            name = "shopdesk",
            parts = (
                appier_extras.AdminPart,
            ),
            *args, **kwargs
        )
        self.scheduler = scheduler.Scheduler(self)

    def start(self):
        appier.WebApp.start(self)
        scheduler = appier.conf("SCHEDULER", True, cast = bool)
        if scheduler: self.scheduler.start()

if __name__ == "__main__":
    app = ShopdeskApp()
    app.serve()
