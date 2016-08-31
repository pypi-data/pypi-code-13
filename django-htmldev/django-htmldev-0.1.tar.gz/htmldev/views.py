from django.shortcuts import render
from django.views.generic import View


class HtmlDev(View):

    def get(self, *args, **kwargs):
        template = "%s.html" % (kwargs['path'],)
        return render(self.request, template, {})
