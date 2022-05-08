from rest_framework.schemas.openapi import SchemaGenerator


class ServerSchemaGenerator(SchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema['servers'] = [{"url": 'http://127.0.0.1:8000'}]
        return schema
