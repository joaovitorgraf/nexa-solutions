from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "O título é obrigatório.",
            "blank": "O título é obrigatório.",
        },
    )

    class Meta:
        model = Chamado

        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]

        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]