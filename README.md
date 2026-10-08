# Forex Risk Analyzer

## Sistema de Análise Quantitativa para Trading Forex

Um sistema robusto e altamente customizável para análise quantitativa de trading forex, desenvolvido especificamente para o mercado brasileiro com cálculos precisos de impostos (IR e IOF) e custos operacionais.

## Características Principais

### Parâmetros Configuráveis
- **Capital Inicial**: Valor inicial para investimento
- **Risco por Operação**: Percentual do capital em risco (1% a 10%)
- **Alavancagem**: Níveis de 1:30 até 1:500
- **Win Rate**: Taxa de acerto das operações
- **Risk:Reward Ratio**: Relação risco-retorno
- **Custos Operacionais**: Spread, comissão, swap
- **Impostos Brasileiros**: IR (15%) e IOF (0.38%)

### Funcionalidades Avançadas
- **Cálculo Automático de Posição**: Métodos de risco fixo, Kelly Criterion e ajuste por volatilidade
- **Análise de Risco-Retorno**: Sharpe Ratio, Profit Factor, Maximum Drawdown
- **Simulação de Cenários**: Comparação entre diferentes alavancagens
- **Simulação Monte Carlo**: Análise probabilística com 100+ cenários
- **Interface Web Interativa**: Dashboard completo com Streamlit
- **Relatórios Detalhados**: Exportação para Excel e PDF

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências
```bash
pip install -r requirements.txt
```

## Como Usar

### 1. Interface Web (Recomendado)
```bash
streamlit run forex_dashboard.py
```
Acesse: http://localhost:8501

### 2. Exemplos Práticos
```bash
python exemplo_completo.py
```

### 3. Uso Programático
```python
from forex_analyzer import ForexAnalyzer, TradingParameters

# Configurar parâmetros
params = TradingParameters(
    capital_inicial=10000.0,
    porcentagem_risco=2.0,
    alavancagem=50,
    win_rate=65.0,
    rr_ratio=1.5
)

# Criar analisador
analyzer = ForexAnalyzer(params)

# Executar simulação
results = analyzer.simulate_trading_scenario(months=48)
print(f"Retorno Total: {results['total_return']:.2f}%")
```

## Estrutura do Projeto

```
forex-risk-analyzer/
├── forex_analyzer.py          # Classe principal de análise
├── position_calculator.py     # Calculadora avançada de posições
├── forex_dashboard.py         # Interface web Streamlit
├── exemplo_completo.py        # Exemplos práticos
├── requirements.txt           # Dependências
├── README.md                  # Este arquivo
└── docs/                      # Fórmulas, manual da planilha e validação de cenários
```

## Componentes Principais

### ForexAnalyzer
Classe principal que gerencia:
- Parâmetros de trading
- Simulação de cenários
- Cálculo de métricas de performance
- Análise de risco

### AdvancedPositionCalculator
Calculadora especializada em:
- Tamanho de posição por risco fixo
- Critério de Kelly
- Ajuste por volatilidade
- Stop loss e take profit ótimos

### Dashboard Streamlit
Interface web com:
- Entrada de parâmetros interativa
- Visualizações gráficas em tempo real
- Relatórios executivos
- Exportação de dados

## Métricas Calculadas

### Performance
- **ROI**: Retorno sobre investimento
- **Sharpe Ratio**: Retorno ajustado ao risco
- **Profit Factor**: Relação lucro/prejuízo
- **Calmar Ratio**: Retorno/Maximum Drawdown
- **Mathematical Expectancy**: Expectativa matemática por trade

### Risco
- **Maximum Drawdown**: Maior perda consecutiva
- **Value at Risk (VaR)**: Valor em risco
- **Risk-Adjusted Return**: Retorno ajustado ao risco
- **Volatilidade**: Desvio padrão dos retornos

## Visualizações

### Gráficos Disponíveis
1. **Evolução do Capital**: Bruto vs Líquido
2. **Distribuição de Custos**: Spread, Comissão, Impostos
3. **Comparação de Lucros**: Mensal e acumulado
4. **Análise de Drawdown**: Períodos de perda
5. **Cenários de Alavancagem**: Comparativo de performance

## Especificidades do Brasil

### Impostos
- **Imposto de Renda**: 15% sobre lucros
- **IOF**: 0.38% sobre operações
- **Cálculo Automático**: Integrado nas simulações

### Custos Operacionais
- **Spread**: Diferença bid/ask
- **Comissão**: Taxa por operação
- **Swap**: Custo de financiamento overnight
- **Margem**: Cálculo baseado na alavancagem

## Alertas de Risco

O sistema monitora automaticamente:
- Risco total mensal > 20%
- Alavancagem > 100:1
- Margem líquida < 10%
- Expectativa matemática negativa
- Drawdown > 15% do capital

## Exemplos de Uso

### Trader Conservador
```python
params = TradingParameters(
    capital_inicial=10000.0,
    porcentagem_risco=1.0,  # 1% por operação
    alavancagem=30,         # Baixa alavancagem
    win_rate=70.0,          # Alta taxa de acerto
    rr_ratio=1.2            # R:R conservador
)
```

### Trader Agressivo
```python
params = TradingParameters(
    capital_inicial=10000.0,
    porcentagem_risco=5.0,  # 5% por operação
    alavancagem=200,        # Alta alavancagem
    win_rate=55.0,          # Menor taxa de acerto
    rr_ratio=2.5            # R:R agressivo
)
```

## Validação e Testes

O sistema foi validado com:
- **Cenários Históricos**: Dados reais de mercado
- **Simulação Monte Carlo**: 100+ cenários aleatórios
- **Stress Testing**: Condições extremas de mercado
- **Backtesting**: Estratégias históricas

## Relatórios Gerados

### Excel
- Resumo executivo
- Dados mensais detalhados
- Histórico de trades
- Métricas de performance

### PDF
- Relatório profissional
- Gráficos e análises
- Recomendações de risco

## Personalização

### Adicionando Novos Pares
```python
class CurrencyPair(Enum):
    EURUSD = "EURUSD"
    GBPUSD = "GBPUSD"
    USDJPY = "USDJPY"
    # Adicione novos pares aqui
```

### Modificando Custos
```python
# Ajustar custos por broker
params.spread_pips = 1.5      # Spread menor
params.comissao_pct = 0.03    # Comissão reduzida
params.swap_diario = 0.01     # Swap favorável
```

## Avisos Importantes

1. **Risco de Mercado**: Trading forex envolve risco significativo
2. **Simulação**: Resultados passados não garantem performance futura
3. **Regulamentação**: Verifique regulamentações locais
4. **Capital**: Nunca invista mais do que pode perder
5. **Educação**: Sistema para análise, não aconselhamento financeiro

## Licença

MIT. Veja [LICENSE](LICENSE).

*Esta é uma ferramenta de análise, não aconselhamento financeiro. Trading envolve risco de perda.*
