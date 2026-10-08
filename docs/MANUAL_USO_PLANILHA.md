# MANUAL DE USO - ANÁLISE DE RISCO/RETORNO FOREX

## VISÃO GERAL
Esta planilha foi desenvolvida para análise quantitativa de investimentos forex com capital inicial de R$ 10.000. Ela oferece cálculos automatizados, análise de cenários e ferramentas de gestão de risco.

## FUNCIONALIDADES PRINCIPAIS

### 1. PARÂMETROS DE ENTRADA (Células B4-B10)
- **Capital Inicial**: R$ 10.000 (configurável)
- **Alavancagem**: Dropdown com opções de 1:1 até 1:1000
- **Risco por Operação**: Percentual do capital em risco por trade
- **Objetivo de Retorno Mensal**: Meta de rentabilidade mensal
- **Taxa de Acerto**: Percentual histórico de trades vencedores
- **Spread Médio**: Custo médio por operação em pips
- **Comissão por Lote**: Custo fixo por operação

### 2. CÁLCULOS AUTOMÁTICOS (Seção B13-B19)
- **Capital Alavancado**: Poder de compra total
- **Risco por Operação**: Valor em reais arriscado por trade
- **Retorno Esperado**: Ganho esperado por operação
- **Tamanho Ideal da Posição**: Volume recomendado
- **Stop Loss Recomendado**: Nível de parada em pips
- **Take Profit**: Meta de lucro por operação
- **Ratio Risco/Retorno**: Relação entre risco e retorno

### 3. ANÁLISE DE CENÁRIOS (Linhas 23-25)
Três cenários de projeção:
- **Otimista**: 150% do retorno esperado
- **Realista**: Retorno conforme parâmetros
- **Pessimista**: 30% do retorno esperado

Cada cenário calcula:
- Retorno mensal esperado
- Capital final após 12 meses
- Drawdown máximo estimado

### 4. GESTÃO DE CAPITAL (Linhas 28-32)
- **Operações por Mês**: Frequência de trading
- **Capital por Operação**: Valor médio por trade
- **Risco Total Mensal**: Exposição total ao risco
- **Retorno Esperado Mensal**: Ganho projetado
- **Break-even**: Número de operações para equilibrar

### 5. SIMULAÇÃO DE ESTRATÉGIAS (Linhas 36-39)
Quatro estratégias pré-configuradas:
- **Conservadora**: Baixa alavancagem, baixo risco
- **Moderada**: Alavancagem média, risco controlado
- **Agressiva**: Alta alavancagem, risco elevado
- **Especulativa**: Alavancagem máxima, alto risco

### 6. MÉTRICAS DE PERFORMANCE (Linhas 42-46)
- **Sharpe Ratio**: Retorno ajustado ao risco
- **Profit Factor**: Relação lucro/prejuízo
- **Win Rate**: Taxa de acerto
- **Expectativa**: Resultado esperado por operação
- **ROI Anual**: Retorno sobre investimento anualizado

### 7. PROJEÇÃO MENSAL (Colunas E-H)
Tabela com evolução mensal do capital:
- Mês a mês por 12 meses
- Capital inicial e final de cada período
- Percentual de retorno aplicado
- Formatação automática em reais

### 8. ALERTAS DE RISCO (Linhas 19-22)
Sistema de alertas automáticos:
- **Risco Total**: Avisa se exposição > 10%
- **Alavancagem**: Alerta para alavancagem > 100:1
- **Drawdown**: Aviso se drawdown > 20%
- **Capital por Operação**: Alerta se posição > 10% do capital

### 9. GRÁFICO DE PROJEÇÃO
Gráfico de linha mostrando evolução do capital ao longo de 12 meses.

## COMO USAR

### PASSO 1: CONFIGURAR PARÂMETROS
1. Ajuste o capital inicial se diferente de R$ 10.000
2. Selecione a alavancagem desejada no dropdown
3. Defina o percentual de risco por operação (recomendado: 1-3%)
4. Configure sua meta de retorno mensal
5. Insira sua taxa histórica de acerto

### PASSO 2: ANALISAR RESULTADOS
1. Verifique os cálculos automáticos na seção principal
2. Analise os três cenários de projeção
3. Observe as métricas de performance
4. Consulte os alertas de risco

### PASSO 3: OTIMIZAR ESTRATÉGIA
1. Teste diferentes alavancagens
2. Ajuste o risco por operação
3. Compare as estratégias simuladas
4. Use o gráfico para visualizar crescimento

## FÓRMULAS PRINCIPAIS

### Cálculo de Posição Ideal
```
Tamanho da Posição = Risco por Operação / Stop Loss em pips
```

### Expectativa Matemática
```
Expectativa = (Win Rate × Ganho Médio) - (Loss Rate × Perda Média)
```

### Sharpe Ratio
```
Sharpe = (Retorno - Taxa Livre de Risco) / Desvio Padrão
```

### Drawdown Máximo
```
Drawdown = (Pico - Vale) / Pico × 100
```

## ALERTAS IMPORTANTES

**RISCO ALTO**: Quando risco total mensal > 10%
**ALAVANCAGEM EXCESSIVA**: Quando alavancagem > 100:1
**DRAWDOWN PERIGOSO**: Quando drawdown > 20%
**POSIÇÃO GRANDE**: Quando posição > 10% do capital

## RECOMENDAÇÕES DE USO

1. **Iniciantes**: Use estratégia conservadora (alavancagem 1:10, risco 1%)
2. **Intermediários**: Estratégia moderada (alavancagem 1:50, risco 2%)
3. **Avançados**: Estratégia agressiva com gestão rigorosa
4. **Nunca**: Use mais de 5% de risco por operação

## LIMITAÇÕES

- Não considera volatilidade do mercado
- Assume distribuição normal dos retornos
- Não inclui custos de financiamento overnight
- Projeções baseadas em performance passada

## SUPORTE

Para dúvidas ou customizações, consulte a documentação técnica ou entre em contato com o desenvolvedor.

---
**Versão**: 1.0  
**Data**: 2024  
**Desenvolvido para**: Análise quantitativa de trading forex