import unittest
from decimal import Decimal as D

from imoveis import Apartamento, Casa, Estudio
from orcamento import Orcamento


class TestImoveis(unittest.TestCase):
    def test_apartamento_1_quarto_com_criancas(self):
        self.assertEqual(Apartamento(1, False, True).aluguel_mensal(), D("700.00"))

    def test_apartamento_1_quarto_sem_criancas_tem_5_por_cento(self):
        self.assertEqual(Apartamento(1, False, False).aluguel_mensal(), D("665.00"))

    def test_apartamento_2_quartos_garagem_sem_criancas(self):
        # (700 + 200 + 300) = 1200 -> 5% = 60 -> 1140
        self.assertEqual(Apartamento(2, True, False).aluguel_mensal(), D("1140.00"))

    def test_casa(self):
        self.assertEqual(Casa(1, False).aluguel_mensal(), D("900.00"))
        self.assertEqual(Casa(2, False).aluguel_mensal(), D("1150.00"))
        self.assertEqual(Casa(2, True).aluguel_mensal(), D("1450.00"))  # sem desconto

    def test_estudio(self):
        self.assertEqual(Estudio().aluguel_mensal(), D("1200.00"))
        self.assertEqual(Estudio(0).aluguel_mensal(), D("1450.00"))
        self.assertEqual(Estudio(3).aluguel_mensal(), D("1630.00"))

    def test_quartos_invalidos(self):
        with self.assertRaises(ValueError):
            Casa(3, False)


class TestOrcamento(unittest.TestCase):
    def test_parcelas_somam_taxa(self):
        for n in range(1, 6):
            self.assertEqual(sum(Orcamento(Casa(1, False), n).valores_parcelas_taxa()), D("2000.00"))

    def test_parcelas_invalidas(self):
        with self.assertRaises(ValueError):
            Orcamento(Casa(1, False), 6)

    def test_projecao_12_meses(self):
        proj = Orcamento(Casa(1, False), 5).projecao_12_meses()
        self.assertEqual(len(proj), 12)
        self.assertEqual(proj[0]["total"], D("1300.00"))
        self.assertEqual(proj[5]["total"], D("900.00"))

    def test_total_primeiro_ano(self):
        self.assertEqual(Orcamento(Casa(1, False), 5).total_primeiro_ano(), D("12800.00"))


if __name__ == "__main__":
    unittest.main()
