"""Funções de leitura e validação de dados digitados pelo usuário."""


def ler_opcao(mensagem, opcoes_validas):
    """Repete a pergunta até o usuário digitar uma opção válida."""
    while True:
        resposta = input(mensagem).strip()
        if resposta in opcoes_validas:
            return resposta
        print(f"  Opção inválida. Escolha entre: {', '.join(opcoes_validas)}.")


def ler_inteiro(mensagem, minimo, maximo=None):
    """Lê um número inteiro dentro do intervalo permitido."""
    while True:
        resposta = input(mensagem).strip()
        try:
            numero = int(resposta)
        except ValueError:
            print("  Digite um número inteiro.")
            continue
        if numero < minimo or (maximo is not None and numero > maximo):
            limite = f"entre {minimo} e {maximo}" if maximo is not None else f"a partir de {minimo}"
            print(f"  Valor fora do permitido. Digite um número {limite}.")
            continue
        return numero


def ler_sim_nao(mensagem):
    """Retorna True para 's' e False para 'n'."""
    while True:
        resposta = input(mensagem + " (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("  Responda com 's' ou 'n'.")
