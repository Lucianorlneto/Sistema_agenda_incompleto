from django.contrib import admin
from myapp.models import *

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Papel)
admin.site.register(Usuario_papel)
admin.site.register(Ficha)
admin.site.register(Horario)