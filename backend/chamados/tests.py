from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoCreateTests(APITestCase):
    def test_criacao_sem_titulo_retorna_erro_de_validacao(self):
        response = self.client.post(
            reverse("chamado-list-create"),
            {"descricao": "Chamado sem título"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["titulo"], ["O título é obrigatório."])
        self.assertEqual(Chamado.objects.count(), 0)
