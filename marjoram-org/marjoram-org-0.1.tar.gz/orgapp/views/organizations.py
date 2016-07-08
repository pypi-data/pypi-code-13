from django.views.generic import ListView, DetailView, TemplateView, FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from . import NameSearchMixin
from orgapp.models import Organization
from orgapp.forms import CreateOrganizationForm, ContactForm, OrganizationFilterForm


class CreateOrganizationView(FormView):
    template_name = 'org/create_organization.html'
    form_class = CreateOrganizationForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(CreateOrganizationForm, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateOrganizationView, self).dispatch(request, *args, **kwargs)

    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            self.org_inst = get_object_or_404(Organization, pk=pk)
            self.template_name = 'org/organization_settings.html'
        else:
            self.org_inst = Organization(creator=self.request.user)
        self.org_form = CreateOrganizationForm(
            user=self.request.user,
            instance=self.org_inst,
            data=request.POST
        )

        if self.org_form.is_valid():
            data = self.org_form.cleaned_data
            data['creator'] = request.user

        return redirect(
            'organization_profile',
            pk=organization.pk,
        )
        return self.get(request, *args, **kwargs)


class OrganizationDelete(DetailView):
    model = Organization
    success_url = reverse_lazy('list_organization')


class UpdateOrganizationView(UpdateView):

    model = Organization
    form_class = CreateOrganizationForm
    template_name = 'org/organization_settings.html'
    success_url = 'organization_profile'

class OrganizationDetailView(DetailView):
    template_name = 'org/organization_detail.html'
    model = Organization


class ContactOrganizationView(FormView):
    template_name = 'org/contact.html'
    form_class = ContactForm
    success_url = 'org/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(ContactView, self).form_valid(form)


class OrganizationListView(NameSearchMixin, ListView):
    template_name = 'org/organization_list.html'
    paginate_by = 10
    model = Organization

    def dispatch(self, *args, **kwargs):
        return super(OrganizationListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(OrganizationListView, self).get_queryset()
        form = OrganizationFilterForm(self.request.GET)
        if form.is_valid():
            return form.get_organizations(qs)

        return Organization.objects.none()

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        initial = self.request.GET.copy()
        context.update({
            'form': OrganizationFilterForm(initial=initial),
        })
        return context

organization_add_view = CreateOrganizationView.as_view()
organization_delete_view = OrganizationDelete.as_view()
organization_contact_view = ContactOrganizationView.as_view()
organization_detail_view = OrganizationDetailView.as_view()
organization_list_view = OrganizationListView.as_view()
organization_settings_view = UpdateOrganizationView.as_view()
#sorganization_json_view = OrganizationJsonView.as_view()
