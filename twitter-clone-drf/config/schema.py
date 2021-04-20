from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
import os


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = '/' + os.environ.get('REDIRECT_PREFIX', 'api')
        return schema


def get_custom_schema_view():
    return get_schema_view(
        openapi.Info(
            title="Twitter Clone",
            default_version='v1',
            description="""Twitter API clone, allows functionality like FOLLOW/UNFOLLOW users,
            LIKE/UNLIKE Tweets and also comment tweets""",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="jeancalarcon98@gmail.com"),
            license=openapi.License(name="MIT"),
        ),
        url='https://jcalarcon.me/',
        public=True,
        permission_classes=[AllowAny],
        generator_class=SchemaGenerator
    )
