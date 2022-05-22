from rest_framework.schemas.openapi import SchemaGenerator, AutoSchema
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import exceptions, serializers
import warnings


class ServerSchemaGenerator(SchemaGenerator):
    """
    Overrides the SchemGenerator class to appened the
    'servers' object to the shchema.
    """
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema['servers'] = [{"url": 'http://127.0.0.1:8000'}]
        return schema


class RequestResponseSchema(AutoSchema):
    """
    Adds the abillity to clearly define a request and
    response serializer for the view by implementing
    the 'get_request_serializer' and 'get_response_serializer'
    functions
    """

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


class SerializerSchemaMixin:
    """
    Mixin that already will allow the ability the define a
    request and response serializer for the view by.

    To implement define the request_serializer and response_serializer
    variables on the view class.
    """

    request_serializer = None
    response_serializer = None
    schema = RequestResponseSchema()

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
