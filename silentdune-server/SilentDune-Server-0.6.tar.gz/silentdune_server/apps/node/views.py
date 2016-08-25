#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from proj.serializer import RecordCountSerializer
from apps.node.serializers import *
from proj.models import RecordCount, GlobalPreferences
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from apps.node.models import *
from apps.alerts.models import *
from apps.accounts.models import UserProfile


class NodeViewSet(viewsets.ModelViewSet):
    """
    Node Model View Set
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    # Return the Node model record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(Node.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Allow filtering Node by machine_id
        """
        queryset = Node.objects.all()

        machine_id = self.request.query_params.get('machine_id', None)
        if machine_id is not None:
            queryset = queryset.filter(machine_id=machine_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        We are doing this long hand because we want to return a HTTP_409_CONFLICT if the node already exists.
        """
        m_id = request.data['machine_id']

        try:
            obj = Node.objects.get(machine_id=m_id)
        except ObjectDoesNotExist:
            obj = None

        serializer = NodeSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            kwargs = {}

            # Set node polling_interval if not given to the global default.
            if 'polling_interval' not in request.data:
                try:
                    kwargs = {'polling_interval': GlobalPreferences.objects.get(pk=1).polling_interval}
                except ObjectDoesNotExist:
                    pass  # We'll use the model default value if we are here.

            serializer.save(**kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK if obj else status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeInterfaceViewSet(viewsets.ModelViewSet):
    """
    Node Interface Model View Set
    """
    queryset = NodeInterfaces.objects.all()
    serializer_class = NodeInterfaceSerializer

    def get_queryset(self):
        """
        Queryset is always filtered by node id portion of the URL.
        """
        return NodeInterfaces.objects.filter(node=self.kwargs['node'])


class NodeBundleViewSet(viewsets.ModelViewSet):
    """
    Node Bundle Model View Set
    """
    queryset = NodeBundle.objects.all()
    serializer_class = NodeBundleSerializer

    def get_queryset(self):
        """
        Queryset is always filtered by node id portion of the URL.
        """
        return NodeBundle.objects.filter(node=self.kwargs['node'])

    def create(self, request, *args, **kwargs):
        """
        We are doing this long hand because we want to do an update or create.
        """
        node = request.data['node']

        try:
            obj = NodeBundle.objects.get(node=node)
        except ObjectDoesNotExist:
            obj = None

        serializer = NodeBundleSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK if obj else status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete a NodeBundle record based on node positional value from url.
        """
        # Get node id from url, must use kwargs to get value.
        node = kwargs['node']

        if node is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            rec = NodeBundle.objects.get(node=node)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        rec.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class NodeProcessViewSet(viewsets.ModelViewSet):

    """
    The Node Process View is used for list processes running on a client.
    The Client sends a list of processes in a batch.

    Before each batch is sent, the client calls "mark" to set the 'delete' field to True.
    After the records have been marked, the client sends the batch.  Each existing record
    is updated and the 'delete' field is set to False.

    After the batch, the client calls 'delete' to delete all records where 'delete' is still True.
    """

    queryset = NodeProcess.objects.all()
    serializer_class = NodeProcessSerializer

    def get_queryset(self):
        """
        Queryset is always filtered by node id portion of the URL.
        """
        return NodeProcess.objects.filter(node=self.kwargs['node'])

    def create(self, request, *args, **kwargs):
        """
        We are doing this long hand because we want to do an update or create.
        """
        node = request.data['node']

        obj = None

        try:
            obj = NodeProcess.objects.get(node=node, name=request.data['name'], category=request.data['category'])
        except ObjectDoesNotExist:
            pass

        serializer = NodeProcessSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK if obj else status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='mark')
    def mark_for_deletion(self, request, *args, **kwargs):
        """
        Mark node process records for deletion.
        """

        # Get node id from url, must use kwargs to get value.
        node = kwargs['node']

        if node is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            processes = NodeProcess.objects.filter(node=node)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        for process in processes:
            process.delete = True
            process.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['get'], url_path='delete')
    def delete_marked_records(self, request, *args, **kwargs):
        """
        Delete a NodeBundle record based on node positional value from url.
        """
        # Get node id from url, must use kwargs to get value.
        node = kwargs['node']

        if node is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            processes = NodeProcess.objects.filter(node=node, delete=True)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        processes.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
def nodes(request):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    display_nodes = None
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
        
        if request.method == "POST":
            txt_cleaner = forms.CharField()
            txt_cleaner.required = False
            search_term = txt_cleaner.clean(request.POST.get('search_term',''))
            display_nodes = Node.objects.filter( Q(hostname__icontains=search_term) | 
                                                 Q(dist__icontains=search_term)  
                                               )
 
        else:    
        # There's no POST data so get all the machine subsets
            display_nodes = Node.objects.all()            
    
    
    context['nodes'] = display_nodes 

    return render(request, 'nodes/nodes.html', context )
    
    
@login_required
def edit_node(request, incoming_id):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
        
    this_node = Node.objects.get(id=incoming_id)
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True  
          
        if request.method == "POST":
             txt_cleaner = forms.CharField()
             txt_cleaner.required = False
             system = txt_cleaner.clean(request.POST['system'])
             notes = txt_cleaner.clean(request.POST['notes'])
             bundle_name = txt_cleaner.clean(request.POST['bundle'])
             
             #update this node's bundle connection
             this_bundle = Bundle.objects.get(name=bundle_name)
             node_bundle = NodeBundle.objects.get(node_id=this_node.id)
             node_bundle.bundle_id = this_bundle.id
             node_bundle.save()
             
             #update node values
             this_node.system = system
             this_node.notes = notes
             this_node.save()
  
    bundles = Bundle.objects.all()
    current_bundle = Bundle.objects.get(id=NodeBundle.objects.get(node_id=this_node.id).bundle_id)
    #current_bundle = BundleNode.objects.get(node_id=this_node.id)
    
    context['current_bundle'] = current_bundle
    context['bundles'] = bundles
    context['next_time'] = datetime.datetime.now() + datetime.timedelta(seconds=this_node.polling_interval) 
    context['node'] = this_node
    return render(request, 'nodes/edit_node.html', context )  
    
@login_required
def delete_node(request, incoming_id):
  
    this_node = Node.objects.get(id=incoming_id)
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        this_node.delete()
  
    return redirect('/node/nodes/')    
    
    
@login_required
def view_node(request, incoming_id):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
        
    this_node = Node.objects.get(id=incoming_id)
    
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True 
        
    bundles = Bundle.objects.all()
    current_bundle = Bundle.objects.get(id=NodeBundle.objects.get(node_id=this_node.id).bundle_id)         
 
    context['current_bundle'] = current_bundle
    context['next_time'] = datetime.datetime.now() + datetime.timedelta(seconds=this_node.polling_interval)  
    context['node'] = this_node
    context['view'] = True  

    return render(request, 'nodes/edit_node.html', context )  
    

@require_http_methods(["POST", "GET"])
def toggle_locked(request):
    node_id = request.POST['node_id']
    
    this_node = Node.objects.get(id=node_id)
    this_node.sync = True
    this_node.locked = not this_node.locked  
        
    this_node.save()
    return HttpResponse("Success") 
