from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from .client import Client


class CommunityBlogListView(View):
    template_name = "balystic/blog_list.html"

    def get(self, request):
        page = request.GET.get('page', 1)
        client = Client()
        blog_entries = client.get_blogs(page=page)['blogs']
        context = {'blog_entries': blog_entries}
        return render(request, self.template_name, context)


class CommunityBlogDetailView(View):
    template_name = "balystic/blog_detail.html"

    def get(self, request, slug):
        client = Client()
        blog_entry = client.get_blog_detail(slug)
        #########################
        if 'blog' not in blog_entry:
            raise Http404
        blog_entry = blog_entry['blog']
        #########################
        context = {'entry': blog_entry}
        return render(request, self.template_name, context)
