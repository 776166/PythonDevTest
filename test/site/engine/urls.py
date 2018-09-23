from django.conf.urls import url
from django.conf.urls import include

from django.contrib import admin
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets

from engine.views import index
from contacts.models import Contact
from rest_framework.documentation import include_docs_urls

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'company', 'email', 'phone', 'interest')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^contacts/', include('contacts.urls')),
    
    url(r'^api/', include(router.urls, namespace='rest_api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/api/', include_docs_urls(title='My API title'), name='api_docs'),
]
