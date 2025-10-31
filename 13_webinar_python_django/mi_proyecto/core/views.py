# Importamos las clases y módulos necesarios de Django REST Framework (DRF)
from rest_framework import viewsets  # viewsets permite crear vistas CRUD completas con poco código

# Importamos el modelo que queremos exponer mediante la API
from .models import Task

# Importamos el serializer que convierte los objetos Task a JSON y viceversa
from .serializers import TaskSerializer


# Definimos una clase que hereda de viewsets.ModelViewSet
# ModelViewSet es una clase especial de DRF que automáticamente
# crea todas las operaciones CRUD:
# - GET (listar o ver una tarea)
# - POST (crear nueva tarea)
# - PUT / PATCH (actualizar tarea existente)
# - DELETE (eliminar tarea)
class TaskViewSet(viewsets.ModelViewSet):
    
    # 'queryset' define qué registros del modelo se van a manejar.
    # Aquí obtenemos todas las tareas y las ordenamos de más reciente a más antigua.
    queryset = Task.objects.all().order_by('-created_at')
    
    # 'serializer_class' indica qué serializer se usará para transformar los datos
    # (de modelo a JSON y de JSON a modelo)
    serializer_class = TaskSerializer
    
from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

