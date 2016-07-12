from .exceptions import RequestValidationError


class Method(object):
    request_serializer = None
    response_serializer = None

    @classmethod
    def as_function(cls):
        def f(request):
            obj = cls()
            return obj(request)
        return f

    def __call__(self, request):
        self.request = request
        self.request_data = self.deserialize_request()
        self.response_data = self.call()
        self.response = self.serialize_response()
        return self.response

    def deserialize_request(self):
        if self.request_serializer:
            serializer = self.request_serializer(data=self.request.data)
            if not serializer.is_valid():
                raise RequestValidationError(serializer.errors)
            return serializer.validated_data
        else:
            return self.request.data

    def serialize_response(self, many=False):
        if self.response_serializer:
            return self.response_serializer(self.response_data, many=many).data
        else:
            return self.response_data


class ListMethod(Method):

    def call(self):
        return self.get_objects()

    def get_objects(self):
        return []


class PaginatedListMethod(ListMethod):
    paginator_min_count = 1
    paginator_max_count = None
    paginator_default_count = None
    paginator_max_offset = None

    def call(self):
        self.paginator_offset = self.request.data.get('offset', 0)
        if isinstance(self.paginator_offset, int):
            if self.paginator_offset < 0:
                # FIXME raise a RequestValidationError?
                self.paginator_offset = 0
        else:
            # FIXME raise a RequestValidationError?
            self.paginator_offset = self.paginator_default_count
        self.paginator_count = self.request.data.get('count', None)
        if isinstance(self.paginator_count, int):
            if self.paginator_count < self.paginator_min_count:
                self.paginator_count = self.paginator_min_count
            elif self.paginator_count > self.paginator_max_count:
                self.paginator_count = self.paginator_max_count
        else:
            if self.paginator_count is None:
                self.paginator_count = self.paginator_max_count
            else:
                # FIXME raise a RequestValidationError?
                self.paginator_count = None
        super(PaginatedListMethod, self).call()
        self.all_objects = self.get_objects()
        self.object_count = self.get_object_count()
        self.objects = self.apply_pagination()
        return self.objects

    def get_object_count(self):
        return 0

    def apply_pagination(self):
        objects = self.all_objects
        if self.paginator_offset or self.paginator_count:
            if self.paginator_count:
                objects = objects[:self.paginator_count]
            else:
                objects = objects[self.paginator_offset:self.paginator_offset+self.paginator_count]
        return objects

    def serialize_response(self):
        return {
            'list': super(PaginatedListMethod, self).serialize_response(many=True),
            'count': self.object_count
        }
