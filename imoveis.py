"""Modelos de imóveis da R.M Imóveis.

Cada tipo de imóvel sabe calcular o próprio aluguel (polimorfismo):
quem monta o orçamento não precisa conhecer as regras de cada categoria.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


def arredondar(valor):
    """Arredonda para 2 casas decimais (centavos)."""
    return Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class ItemOrcamento:
    """Uma linha do orçamento (aluguel-base, adicional, desconto...)."""
    descricao: str
    valor: Decimal


class Imovel(ABC):
    """Classe base: define o contrato que todo imóvel precisa cumprir."""

    tipo = "Imóvel"
    aluguel_base = Decimal("0")

    @abstractmethod
    def descricao(self):
        """Texto curto com as características escolhidas."""

    @abstractmethod
    def itens_adicionais(self):
        """Lista de ItemOrcamento com os acréscimos do imóvel."""

    def percentual_desconto(self):
        """Desconto sobre o aluguel (0 por padrão; subclasses podem mudar)."""
        return Decimal("0")

    def subtotal(self):
        """Aluguel-base + adicionais, ainda sem desconto."""
        total = self.aluguel_base
        for item in self.itens_adicionais():
            total += item.valor
        return arredondar(total)

    def valor_desconto(self):
        return arredondar(self.subtotal() * self.percentual_desconto())

    def aluguel_mensal(self):
        return arredondar(self.subtotal() - self.valor_desconto())


class ImovelResidencial(Imovel):
    """Comportamento comum de casas e apartamentos (quartos e garagem)."""

    adicional_dois_quartos = Decimal("0")
    adicional_garagem = Decimal("300.00")

    def __init__(self, quartos, tem_garagem):
        if quartos not in (1, 2):
            raise ValueError("A quantidade de quartos deve ser 1 ou 2.")
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def descricao(self):
        garagem = "com garagem" if self.tem_garagem else "sem garagem"
        plural = "quarto" if self.quartos == 1 else "quartos"
        return f"{self.tipo} de {self.quartos} {plural}, {garagem}"

    def itens_adicionais(self):
        itens = []
        if self.quartos == 2:
            itens.append(ItemOrcamento("Adicional de 2º quarto", self.adicional_dois_quartos))
        if self.tem_garagem:
            itens.append(ItemOrcamento("Vaga de garagem", self.adicional_garagem))
        return itens


class Apartamento(ImovelResidencial):
    tipo = "Apartamento"
    aluguel_base = Decimal("700.00")
    adicional_dois_quartos = Decimal("200.00")
    desconto_sem_criancas = Decimal("0.05")

    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__(quartos, tem_garagem)
        self.tem_criancas = tem_criancas

    def descricao(self):
        criancas = "com crianças" if self.tem_criancas else "sem crianças"
        return f"{super().descricao()}, {criancas}"

    def percentual_desconto(self):
        # Regra exclusiva de apartamentos: sem crianças = 5% de desconto.
        return Decimal("0") if self.tem_criancas else self.desconto_sem_criancas


class Casa(ImovelResidencial):
    tipo = "Casa"
    aluguel_base = Decimal("900.00")
    adicional_dois_quartos = Decimal("250.00")


class Estudio(Imovel):
    tipo = "Estúdio"
    aluguel_base = Decimal("1200.00")
    vagas_pacote = 2
    preco_pacote = Decimal("250.00")
    preco_vaga_extra = Decimal("60.00")

    def __init__(self, vagas_extras=None):
        """vagas_extras=None -> sem estacionamento;
        0 ou mais -> pacote de 2 vagas + essa quantidade de vagas extras."""
        if vagas_extras is not None and vagas_extras < 0:
            raise ValueError("A quantidade de vagas extras não pode ser negativa.")
        self.vagas_extras = vagas_extras

    @property
    def total_vagas(self):
        if self.vagas_extras is None:
            return 0
        return self.vagas_pacote + self.vagas_extras

    def descricao(self):
        if self.vagas_extras is None:
            return "Estúdio, sem estacionamento"
        return f"Estúdio, com estacionamento ({self.total_vagas} vagas)"

    def itens_adicionais(self):
        itens = []
        if self.vagas_extras is not None:
            itens.append(ItemOrcamento(
                f"Pacote de estacionamento ({self.vagas_pacote} vagas)", self.preco_pacote))
            if self.vagas_extras > 0:
                itens.append(ItemOrcamento(
                    f"{self.vagas_extras} vaga(s) adicional(is) x R$ {self.preco_vaga_extra}",
                    self.preco_vaga_extra * self.vagas_extras))
        return itens
