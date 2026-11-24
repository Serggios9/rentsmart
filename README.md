# RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

Aplicação em Python, com Programação Orientada a Objetos, que calcula o orçamento
de locação de apartamentos, casas e estúdios, mostra um resumo detalhado e gera um
CSV com a projeção dos 12 primeiros meses de contrato.

Projeto da disciplina **Algorithmic Thinking & Introduction to Object-Oriented Programming**.

## Requisitos

- Python 3.8 ou superior (somente biblioteca padrão, não precisa instalar nada)

## Como executar

```bash
python main.py
```

(no Windows, se necessário: `py main.py`)

O programa pergunta o tipo de imóvel e as opções, valida cada resposta, exibe o
orçamento e cria o arquivo `projecao_12_meses.csv` na mesma pasta.

## Como rodar os testes

```bash
python -m unittest -v
```

## Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Fluxo da aplicação (perguntas, chamada do orçamento, exibição) |
| `entrada.py` | Leitura e validação das entradas do usuário |
| `imoveis.py` | Classes `Imovel`, `ImovelResidencial`, `Apartamento`, `Casa`, `Estudio` e `ItemOrcamento` |
| `orcamento.py` | Classe `Orcamento`: taxa contratual, parcelas, resumo, projeção e CSV |
| `test_rentsmart.py` | Testes automatizados das regras de negócio |

## Regras implementadas

- Aluguel-base: apartamento R$ 700,00 · casa R$ 900,00 · estúdio R$ 1.200,00
- 2 quartos: + R$ 200,00 (apartamento) ou + R$ 250,00 (casa)
- Garagem (casa e apartamento): + R$ 300,00
- Estúdio: pacote de 2 vagas por R$ 250,00 + R$ 60,00 por vaga adicional
- Apartamento sem crianças: 5% de desconto sobre aluguel-base + adicionais
- Taxa contratual de R$ 2.000,00, em 1 a 5 parcelas, exibida separadamente do aluguel

## Decisões e premissas

- O estacionamento do estúdio é **opcional**; ao contratá-lo, o pacote inicial já inclui 2 vagas.
- O desconto de 5% incide sobre o aluguel-base somado a **todos** os adicionais (2º quarto e garagem).
- As parcelas da taxa são cobradas nos primeiros meses; se a divisão gerar centavos, a última parcela absorve a diferença.
- Valores monetários usam `Decimal` para evitar erros de ponto flutuante.
- O CSV usa `;` como separador e vírgula decimal, para abrir corretamente no Excel em português, e inclui uma linha final de totais.

## Exemplo de saída (CSV)

```
Mes;Aluguel;Parcela_Taxa_Contratual;Total_do_Mes
1;1140,00;666,67;1806,67
2;1140,00;666,67;1806,67
3;1140,00;666,66;1806,66
4;1140,00;0,00;1140,00
...
Total;13680,00;2000,00;15680,00
```

## Autor

Sérgio Dos Santos Filho — ADS
