# Importamos las funciones necesarias del módulo de URLs de Django
from django.urls import path, include

# Importamos el sistema de enrutamiento de Django REST Framework (DRF)
# 'routers' nos permite registrar ViewSets de manera automática sin definir cada ruta manualmente.
from rest_framework import routers

# Importamos el ViewSet que creamos para el modelo Task
from .views import TaskViewSet, index


# Creamos una instancia del router por defecto de DRF.
# Este router se encargará de generar automáticamente las rutas CRUD
# (GET, POST, PUT, DELETE) para el TaskViewSet.
router = routers.DefaultRouter()

# Registramos el ViewSet 'TaskViewSet' dentro del router.
# - El primer argumento ('r"tasks"') define la ruta base de la API: /api/tasks/
# - El segundo argumento es la vista (TaskViewSet)
# - 'basename' se usa internamente por DRF para generar nombres únicos de rutas
router.register(r'tasks', TaskViewSet, basename='task')


# Definimos la lista de patrones de URL (urlpatterns)
urlpatterns = [
    # Incluimos todas las rutas generadas automáticamente por el router
    # bajo el prefijo 'api/'. Esto significa que las URLs finales serán:
    # /api/tasks/        → lista y creación
    # /api/tasks/<id>/   → detalle, actualización o eliminación
    path('', index, name='index'),
    path('api/', include(router.urls)),
]

