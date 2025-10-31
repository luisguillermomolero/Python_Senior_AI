# Importamos las funciones necesarias del sistema de enrutamiento de Django.
# 'path' se usa para definir rutas y 'include' permite incluir las rutas de otras aplicaciones.
from django.contrib import admin
from django.urls import path, include


# Definimos la lista principal de rutas (urlpatterns)
urlpatterns = [
    # Ruta para el panel de administración de Django
    # Accedes a él desde: http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),

    # Incluimos todas las rutas definidas en la aplicación 'core'
    # El prefijo '' significa que las rutas de core estarán disponibles directamente desde la raíz del sitio.
    # Por ejemplo:
    # /api/tasks/ → rutas definidas en core/urls.py
    path('', include('core.urls')),
]
