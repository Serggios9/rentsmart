"""RentSmart - Sistema de orçamento de locação da R.M Imóveis."""
from entrada import ler_inteiro, ler_opcao, ler_sim_nao
from imoveis import Apartamento, Casa, Estudio
from orcamento import Orcamento


def montar_imovel():
    print("Tipos de imóvel:")
    print("  1 - Apartamento (base R$ 700,00)")
    print("  2 - Casa        (base R$ 900,00)")
    print("  3 - Estúdio     (base R$ 1.200,00)")
    opcao = ler_opcao("Escolha o tipo (1-3): ", ("1", "2", "3"))

    if opcao == "3":
        vagas_extras = None
        if ler_sim_nao("Deseja estacionamento? (pacote de 2 vagas: R$ 250,00)"):
            vagas_extras = ler_inteiro("Vagas adicionais (R$ 60,00 cada, 0 se nenhuma): ", 0, 20)
        return Estudio(vagas_extras)

    quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
    garagem = ler_sim_nao("Deseja vaga de garagem? (+ R$ 300,00)")
    if opcao == "1":
        tem_criancas = ler_sim_nao("Possui crianças?")
        return Apartamento(quartos, garagem, tem_criancas)
    return Casa(quartos, garagem)


def main():
    print("=== RentSmart | R.M Imóveis ===\n")
    imovel = montar_imovel()
    parcelas = ler_inteiro("Parcelas da taxa contratual de R$ 2.000,00 (1 a 5): ", 1, 5)

    orcamento = Orcamento(imovel, parcelas)
    print("\n" + orcamento.resumo())

    caminho = orcamento.exportar_csv("projecao_12_meses.csv")
    print(f"\nProjeção dos 12 meses salva em: {caminho}")


if __name__ == "__main__":
    main()
