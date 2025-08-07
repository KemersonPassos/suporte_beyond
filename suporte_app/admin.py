from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Cliente

admin.site.register(Cliente)



from django.contrib import admin
from .models import Dispositivo

admin.site.register(Dispositivo)



from django.contrib import admin
from .models import Protocolo

admin.site.register(Protocolo)
