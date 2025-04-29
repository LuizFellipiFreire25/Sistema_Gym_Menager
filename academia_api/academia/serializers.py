from rest_framework import serializers
from .models import Usuario, Treino, Pagamento, Presenca


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class TreinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treino
        fields = '__all__'


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'


class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = '__all__'
