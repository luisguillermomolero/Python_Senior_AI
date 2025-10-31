# Importa el módulo 'admin' que permite registrar y personalizar la interfaz
# de administración de Django (el panel que se accede en /admin).
from django.contrib import admin

# Importa el modelo 'Task' desde el archivo models.py del mismo módulo (app actual).
from .models import Task


# Usa el decorador '@admin.register' para registrar el modelo 'Task'
# directamente en el panel de administración.
# Esto evita tener que escribir admin.site.register(Task, TaskAdmin)
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Esta clase personaliza la forma en que el modelo Task se muestra
    y se gestiona dentro del panel de administración de Django.
    Hereda de admin.ModelAdmin, que ofrece opciones avanzadas de configuración.
    """

    # Define qué campos se mostrarán en la lista del panel de administración.
    # Es decir, las columnas visibles en la tabla de tareas.
    list_display = ('id', 'title', 'completed', 'created_at')

    # Permite agregar un filtro lateral por el campo 'completed' (True/False)
    # para que el administrador pueda filtrar fácilmente las tareas completadas o no.
    list_filter = ('completed',)

    # Habilita una barra de búsqueda en la parte superior del panel de tareas,
    # permitiendo buscar por 'title' o 'description'.
    search_fields = ('title', 'description')
