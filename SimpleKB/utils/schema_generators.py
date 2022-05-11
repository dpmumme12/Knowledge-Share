from rest_framework.schemas.openapi import SchemaGenerator, AutoSchema
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import exceptions, serializers
import warnings


class ServerSchemaGenerator(SchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema['servers'] = [{"url": 'http://127.0.0.1:8000'}]
        return schema


class CustomSchema(AutoSchema):

    def get_operation_id_base(self, path, method, action):
        """
        Compute the base part for operation ID from the model, serializer or view name.
        """
        model = getattr(getattr(self.view, 'queryset', None), 'model', None)

        if self.operation_id_base is not None:
            name = self.operation_id_base

        # Try to deduce the ID from the view's model
        elif model is not None:
            name = model.__name__

        # Try with the serializer class name
        elif self.get_request_serializer(path, method) is not None:
            name = self.get_request_serializer(path, method).__class__.__name__
            if name.endswith('Serializer'):
                name = name[:-10]

        elif self.get_response_serializer(path, method) is not None:
            name = self.get_response_serializer(path, method).__class__.__name__
            if name.endswith('Serializer'):
                name = name[:-10]

        # Fallback to the view name
        else:
            name = self.view.__class__.__name__
            if name.endswith('APIView'):
                name = name[:-7]
            elif name.endswith('View'):
                name = name[:-4]

            # Due to camel-casing of classes and `action` being lowercase, apply title in order to
            # find if action truly comes at the end of the name
            if name.endswith(action.title()):  # ListView, UpdateAPIView, ThingDelete ...
                name = name[:-len(action)]

        if action == 'list' and not name.endswith('s'):  # listThings instead of listThing
            name += 's'

        return name

    def get_request_serializer(self, path, method):
        view = self.view

        if not hasattr(view, 'get_request_serializer'):
            return None

        try:
            return view.get_request_serializer()
        except exceptions.APIException:
            warnings.warn('{}.get_request_serializer() raised an exception during '
                          'schema generation. Serializer fields will not be '
                          'generated for {} {}.'
                          .format(view.__class__.__name__, method, path))
            return None

    def get_response_serializer(self, path, method):
        view = self.view

        if not hasattr(view, 'get_response_serializer'):
            return None

        try:
            return view.get_response_serializer()
        except exceptions.APIException:
            warnings.warn('{}.get_request_serializer() raised an exception during '
                          'schema generation. Serializer fields will not be '
                          'generated for {} {}.'
                          .format(view.__class__.__name__, method, path))
            return None


class CustomGenericView(GenericAPIView):
    request_serializer = None
    response_serializer = None
    schema = CustomSchema()

    def get_serializer_class(self):
        if self.request.method not in ('PUT', 'PATCH', 'POST'):
            assert self.response_serializer is not None, (
                "'%s' should either include a `response_serializer` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
            )

            return self.response_serializer

        assert self.request_serializer is not None, (
            "'%s' should either include a `request_serializer` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.request_serializer

    def get_request_serializer(self, *args, **kwargs):
        request_serializer = self.request_serializer
        if request_serializer:
            kwargs.setdefault('context', self.get_serializer_context())
            return request_serializer(*args, **kwargs)
        return None

    def get_response_serializer(self, *args, **kwargs):
        response_serializer = self.response_serializer
        if response_serializer:
            kwargs.setdefault('context', self.get_serializer_context())
            return response_serializer(*args, **kwargs)
        return None
