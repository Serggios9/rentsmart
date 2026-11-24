"""Orçamento de locação: junta o imóvel, a taxa contratual e a projeção."""
import csv
from decimal import Decimal

from imoveis import arredondar


def formatar_moeda(valor):
    """Formata Decimal como moeda brasileira: R$ 1.234,56."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class Orcamento:
    TAXA_CONTRATUAL = Decimal("2000.00")
    MAX_PARCELAS = 5
    MESES_PROJECAO = 12

    def __init__(self, imovel, parcelas_taxa):
        if not 1 <= parcelas_taxa <= self.MAX_PARCELAS:
            raise ValueError(f"A taxa pode ser paga em 1 a {self.MAX_PARCELAS} parcelas.")
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def valores_parcelas_taxa(self):
        """Divide a taxa em parcelas; a última absorve a diferença de centavos."""
        base = arredondar(self.TAXA_CONTRATUAL / self.parcelas_taxa)
        parcelas = [base] * self.parcelas_taxa
        parcelas[-1] = arredondar(self.TAXA_CONTRATUAL - base * (self.parcelas_taxa - 1))
        return parcelas

    def projecao_12_meses(self):
        """Lista de dicts: mês, aluguel, parcela da taxa e total do mês."""
        aluguel = self.imovel.aluguel_mensal()
        parcelas = self.valores_parcelas_taxa()
        linhas = []
        for mes in range(1, self.MESES_PROJECAO + 1):
            taxa = parcelas[mes - 1] if mes <= len(parcelas) else Decimal("0.00")
            linhas.append({"mes": mes, "aluguel": aluguel, "taxa": taxa,
                           "total": arredondar(aluguel + taxa)})
        return linhas

    def total_primeiro_ano(self):
        return arredondar(sum(l["total"] for l in self.projecao_12_meses()))

    def resumo(self):
        im = self.imovel
        larg = 58
        linhas = ["=" * larg, "RESUMO DO ORÇAMENTO - R.M IMÓVEIS".center(larg), "=" * larg,
                  f"Imóvel: {im.descricao()}", "", "COMPOSIÇÃO DO ALUGUEL MENSAL"]

        def linha(texto, valor):
            return f"  {texto:<40}{formatar_moeda(valor):>16}"

        linhas.append(linha(f"Aluguel-base ({im.tipo})", im.aluguel_base))
        for item in im.itens_adicionais():
            linhas.append(linha(item.descricao, item.valor))
        linhas.append(linha("Subtotal", im.subtotal()))
        if im.percentual_desconto() > 0:
            pct = int(im.percentual_desconto() * 100)
            linhas.append(linha(f"Desconto ({pct}% - sem crianças)", -im.valor_desconto()))
        linhas.append("-" * larg)
        linhas.append(linha("ALUGUEL MENSAL", im.aluguel_mensal()))

        parcelas = self.valores_parcelas_taxa()
        linhas += ["", "TAXA CONTRATUAL (cobrada à parte do aluguel)",
                   linha("Valor total da taxa", self.TAXA_CONTRATUAL),
                   f"  Parcelamento: {self.parcelas_taxa}x de {formatar_moeda(parcelas[0])}"]
        if parcelas[-1] != parcelas[0]:
            linhas.append(f"  (última parcela: {formatar_moeda(parcelas[-1])})")
        linhas += ["", f"TOTAL PREVISTO NOS 12 PRIMEIROS MESES: {formatar_moeda(self.total_primeiro_ano())}",
                   "=" * larg]
        return "\n".join(linhas)

    def exportar_csv(self, caminho="projecao_12_meses.csv"):
        """CSV com ';' e vírgula decimal, para abrir direto no Excel em pt-BR."""
        def num(v):
            return f"{v:.2f}".replace(".", ",")

        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel", "Parcela_Taxa_Contratual", "Total_do_Mes"])
            for l in self.projecao_12_meses():
                escritor.writerow([l["mes"], num(l["aluguel"]), num(l["taxa"]), num(l["total"])])
            escritor.writerow(["Total", num(sum(l["aluguel"] for l in self.projecao_12_meses())),
                               num(self.TAXA_CONTRATUAL), num(self.total_primeiro_ano())])
        return caminho
