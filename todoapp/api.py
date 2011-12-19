from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.validation import Validation
from models import Todo

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']
        resource_name = 'user'

    def get_object_list(self, request, **kwargs):
        obj_list = super(UserResource, self)\
                .get_object_list(request)
        if request is not None:
            obj_list = obj_list.filter(id=request.user.id)
        return obj_list


class TodoResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')
    class Meta:
        queryset = Todo.objects.all()
        authorization = DjangoAuthorization()
        authentication = BasicAuthentication()
        resource_name = 'todo'
        validation = Validation()
        filtering = {'id':['exact'], 'done':['exact']}

    def get_object_list(self, request, **kwargs):
        return super(TodoResource, self)\
                .get_object_list(request)\
                .filter(user=request.user)
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        if filters.has_key('done'):
            filters['done'] = filters['done'] == '1' or filters['done'].lower() == 'true'
        orm_filters = super(TodoResource, self).build_filters(filters)
        return orm_filters



