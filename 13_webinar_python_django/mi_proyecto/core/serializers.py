# Importamos el módulo serializers del framework DRF.
# Este módulo contiene clases que permiten convertir (serializar y deserializar)
# objetos de Django a formatos como JSON o XML.
from rest_framework import serializers

# Importamos el modelo Task que definimos previamente en models.py.
# Este modelo será la base para construir el serializer.
from .models import Task


# Definimos una clase que hereda de serializers.ModelSerializer,
# una clase del DRF que simplifica la creación de serializers basados en modelos de Django.
class TaskSerializer(serializers.ModelSerializer):

    # La clase interna Meta define cómo se comportará el serializer.
    class Meta:
        # Especificamos cuál es el modelo que queremos convertir a JSON.
        model = Task
        
        # Con 'fields = "__all__"' indicamos que queremos incluir TODOS los campos
        # del modelo (id, title, description, completed, created_at, etc.).
        # Si quisiéramos solo algunos, podríamos usar: fields = ['title', 'completed']
        fields = '__all__'
