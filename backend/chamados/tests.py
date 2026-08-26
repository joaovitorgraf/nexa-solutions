from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoListFilterTests(APITestCase):
    def setUp(self):
        Chamado.objects.create(titulo="Chamado aberto", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Chamado em andamento", status=Chamado.Status.EM_ANDAMENTO
        )
        Chamado.objects.create(
            titulo="Chamado concluído", status=Chamado.Status.CONCLUIDO
        )

    def test_lista_todos_os_chamados_quando_sem_filtro(self):
        response = self.client.get(reverse("chamado-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filtra_chamados_por_status_aberto(self):
        response = self.client.get(
            reverse("chamado-list-create"), {"status": "ABERTO"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "ABERTO")

    def test_filtra_chamados_por_status_em_andamento(self):
        response = self.client.get(
            reverse("chamado-list-create"), {"status": "EM_ANDAMENTO"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "EM_ANDAMENTO")

    def test_status_invalido_retorna_erro_400(self):
        response = self.client.get(
            reverse("chamado-list-create"), {"status": "NAO_EXISTE"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)
        
class IndicadoresTests(APITestCase):
    def setUp(self):
        Chamado.objects.create(titulo="Chamado aberto 1", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="Chamado aberto 2", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Chamado em andamento", status=Chamado.Status.EM_ANDAMENTO
        )
        Chamado.objects.create(
            titulo="Chamado concluído", status=Chamado.Status.CONCLUIDO
        )

    def test_retorna_totais_por_status(self):
        response = self.client.get(reverse("indicadores"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 4)
        self.assertEqual(response.data["abertos"], 2)
        self.assertEqual(response.data["em_andamento"], 1)
        self.assertEqual(response.data["concluidos"], 1)