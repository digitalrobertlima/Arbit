# Script de Arbitragem entre Exchanges Brasileiras de Bitcoin

Este script realiza arbitragem entre exchanges de Bitcoin no Brasil, buscando oportunidades de lucro com base nas diferenças de preço de compra e venda nas exchanges.

## Descrição

O script automatiza a execução de ordens de compra e venda em duas exchanges, visando aproveitar variações de preços entre elas para gerar lucro. Ele utiliza APIs de várias exchanges brasileiras para obter dados de saldo, livro de ordens e taxas de negociação.

## Funcionalidades

- **Arbitragem de mercado (ordem a mercado)**: Compra Bitcoin na exchange com preço mais baixo e vende na exchange com preço mais alto.
- **Taxas de exchanges**: Utiliza as taxas de cada exchange para calcular o melhor cenário de lucro.
- **Otimização da quantidade de trade**: A quantidade negociada é ajustada com base no potencial de lucro.
  - Se o lucro for baixo (0,5% ou menos), negocia uma pequena quantidade.
  - Se o lucro for alto (5% ou mais), negocia todo o saldo disponível.
- **Ordens de mercado e ordens limitadas**: O script pode escolher entre ordens a mercado (rápidas, mas menos lucrativas) e ordens limitadas (mais lentas, mas com potencial de maior lucro).

## Pré-requisitos

- Python 3.x
- Bibliotecas Python necessárias: `requests`, `pprint`, além de APIs específicas das exchanges (ex: `mbapi`, `foxapi`).
- Um arquivo `credentials.py` que contenha as credenciais de acesso para as exchanges utilizadas.

### Estrutura de `credentials.py`:
```
MercadoBitcoin = {
    'id': 'seu_id',
    'pin': 'seu_pin',
    'secret': 'seu_secret'
}

FoxBit = {
    'key': 'sua_chave',
    'secret': 'seu_secret'
}
```

## Como usar

1. Configure suas credenciais de API para as exchanges no arquivo `credentials.py`.
2. Edite as variáveis globais no script para ajustar os valores desejados, como quantidade inicial de BTC para venda, exchanges permitidas, etc.
3. Execute o script.

```
python arbitrage.py
```

Se desejar executar o script em modo de depuração (sem enviar ordens reais), defina a variável `debugAll = True`.

## Futuras Melhorias (TODOs)

- Buscar automaticamente os dados de taxas das APIs das exchanges.
- Implementar uma lógica mais robusta para ajustar a quantidade de BTC negociada com base no lucro esperado.
- Criar funções personalizadas para ordens de "taker" (ordem a mercado) e "maker" (ordem limitada).

---

Este README fornece uma visão geral do funcionamento do script e instruções para configurá-lo.
