from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from .client import Client


class CommunityUserList(View):
    """
    Displays a list of the users retrieved from 7dhub
    """
    template_name = 'balystic/user_list.html'
    client = Client()

    def get(self, request):
        context = {'users': self.client.get_users()}
        return render(request, self.template_name, context)


class CommunityUserDetail(View):
    """
    Displays the details for the given user
    """
    templat_name = 'balystic/user_detail.html'
    client=Client()

    def get(self, request, username):
        context = {'user': self.client.get_user(username)}
        return render(request, self.template_name, context)


class CommunityBlogListView(View):
    template_name = "balystic/blog_list.html"

    def get(self, request):
        page = request.GET.get('page', 1)
        client = Client()
        blog_entries = client.get_blogs(page=page)
        #############################
        if 'blogs' not in blog_entries:
            raise Http404
        blog_entries = blog_entries['blogs']
        #############################
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


class CommunityQAListView(View):
    template_name = "balystic/qa_list.html"

    def get(self, request):
        page = request.GET.get('page', 1)
        client = Client()
        questions = client.get_questions(page=page)
        #############################
        if 'questions' not in questions:
            raise Http404
        questions = questions['questions']
        #############################
        context = {'questions': questions}
        return render(request, self.template_name, context)


class CommunityQADetailView(View):
    template_name = "balystic/qa_detail.html"

    def get(self, request, pk):
        client = Client()
        question = client.get_question_detail(pk)
        #########################
        if 'question' not in question:
            raise Http404
        question = question['question']
        #########################
        context = {'question': question}
        return render(request, self.template_name, context)
