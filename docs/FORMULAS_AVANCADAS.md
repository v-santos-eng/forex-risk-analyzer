# FÓRMULAS AVANÇADAS - ANÁLISE QUANTITATIVA FOREX

## FÓRMULAS DE GESTÃO DE RISCO

### 1. Cálculo de Position Sizing (Kelly Criterion)
```excel
=((Win_Rate * Avg_Win) - (Loss_Rate * Avg_Loss)) / Avg_Win
```
**Onde:**
- Win_Rate = Taxa de acerto (ex: 0.6)
- Avg_Win = Ganho médio por operação vencedora
- Loss_Rate = Taxa de erro (1 - Win_Rate)
- Avg_Loss = Perda média por operação perdedora

### 2. Value at Risk (VaR) - 95% Confiança
```excel
=Capital_Total * Volatilidade_Diaria * 1.645
```
**Aplicação:** Perda máxima esperada em 95% dos casos

### 3. Maximum Drawdown Esperado
```excel
=1 - (1 - Risco_Por_Operacao)^Sequencia_Perdas_Maxima
```
**Exemplo:** Risco 2%, 10 perdas seguidas = 18.3% drawdown

---

## FÓRMULAS DE PERFORMANCE

### 4. Sharpe Ratio Modificado
```excel
=(Retorno_Medio - Taxa_Livre_Risco) / DESVPAD(Retornos_Diarios) * RAIZ(252)
```
**Interpretação:**
- > 2.0: Excelente
- 1.0-2.0: Bom
- < 1.0: Questionável

### 5. Sortino Ratio (Foca apenas no downside)
```excel
=(Retorno_Medio - Taxa_Livre_Risco) / Desvio_Downside * RAIZ(252)
```

### 6. Calmar Ratio
```excel
=Retorno_Anualizado / Drawdown_Maximo
```
**Mínimo aceitável:** > 0.5

---

## FÓRMULAS DE EXPECTATIVA

### 7. Expectativa Matemática Completa
```excel
=(Win_Rate * Avg_Win * (1 - Spread/Avg_Win)) - (Loss_Rate * Avg_Loss * (1 + Spread/Avg_Loss)) - Comissao
```

### 8. Profit Factor Ajustado
```excel
=(Lucro_Bruto - Custos_Totais) / (Prejuizo_Bruto + Custos_Totais)
```

### 9. Recovery Factor
```excel
=Lucro_Liquido_Total / Drawdown_Maximo
```
**Mínimo recomendado:** > 2.0

---

## FÓRMULAS DE VOLATILIDADE

### 10. Volatilidade Realizada (20 períodos)
```excel
=DESVPAD(LN(Preco_Atual/Preco_Anterior)) * RAIZ(252)
```

### 11. Average True Range (ATR)
```excel
=MEDIA(MAXIMO(Alta-Baixa; ABS(Alta-Fechamento_Anterior); ABS(Baixa-Fechamento_Anterior)))
```

### 12. Volatilidade Implícita Aproximada
```excel
=ATR_14_Periodos / Preco_Atual * RAIZ(252/14)
```

---

## FÓRMULAS DE CORRELAÇÃO

### 13. Correlação Entre Pares
```excel
=CORREL(Retornos_Par1; Retornos_Par2)
```
**Interpretação:**
- > 0.7: Alta correlação positiva
- -0.7 a 0.7: Correlação moderada
- < -0.7: Alta correlação negativa

### 14. Beta do Portfolio
```excel
=COVAR(Retornos_Portfolio; Retornos_Benchmark) / VAR(Retornos_Benchmark)
```

---

## FÓRMULAS DE TIMING

### 15. Optimal f (Fração Ótima de Kelly)
```excel
=Kelly_Percentage * 0.25
```
**Razão:** Reduz volatilidade mantendo crescimento

### 16. Tempo Esperado para Dobrar Capital
```excel
=LN(2) / LN(1 + Retorno_Medio_Mensal)
```

### 17. Probabilidade de Ruína
```excel
=((1-Edge)/(1+Edge))^(Capital_Inicial/Risco_Por_Operacao)
```
**Onde Edge = (Win_Rate * Avg_Win) - (Loss_Rate * Avg_Loss)**

---

## VALIDAÇÕES TÉCNICAS

### 18. Teste de Normalidade (Jarque-Bera)
```excel
=N/6 * (Skewness^2 + (Kurtosis-3)^2/4)
```
**Se > 5.99:** Rejeita normalidade (95% confiança)

### 19. Autocorrelação de Retornos
```excel
=CORREL(Retornos[1:N-1]; Retornos[2:N])
```
**Ideal:** Próximo de zero

### 20. Teste de Estacionariedade (ADF Simplificado)
```excel
=CORREL(Diferenca_Precos; Precos_Defasados)
```

---

## FÓRMULAS DE OTIMIZAÇÃO

### 21. Efficient Frontier (Retorno vs Risco)
```excel
=Retorno_Esperado - Lambda * Variancia_Portfolio
```

### 22. Índice de Treynor
```excel
=(Retorno_Portfolio - Taxa_Livre_Risco) / Beta_Portfolio
```

### 23. Information Ratio
```excel
=(Retorno_Portfolio - Retorno_Benchmark) / DESVPAD(Tracking_Error)
```

---

## IMPLEMENTAÇÃO NO EXCEL

### Células de Validação:
```excel
// Validar se risco total < 10%
=SE(Risco_Total_Mensal > 0.1; "RISCO ALTO"; "OK")

// Validar Sharpe Ratio
=SE(Sharpe_Ratio < 1; "BAIXO"; SE(Sharpe_Ratio > 2; "EXCELENTE"; "BOM"))

// Validar Drawdown
=SE(Drawdown_Atual > 0.15; "CRÍTICO"; SE(Drawdown_Atual > 0.1; "ATENÇÃO"; "OK"))
```

### Formatação Condicional:
```excel
// Para células de retorno
=SE(Valor > 0; "Verde"; "Vermelho")

// Para alertas de risco
=SE(PROCURAR("RISCO"; Celula) > 0; "Amarelo"; "Branco")
```

---

## MACROS VBA ÚTEIS

### Cálculo Automático de Posição:
```vba
Function CalcularPosicao(Capital As Double, Risco As Double, StopLoss As Double) As Double
    CalcularPosicao = (Capital * Risco / 100) / StopLoss
End Function
```

### Alerta de Drawdown:
```vba
Sub AlertaDrawdown()
    If Range("DrawdownAtual").Value > 0.15 Then
        MsgBox "ATENÇÃO: Drawdown crítico detectado!", vbCritical
    End If
End Sub
```

---

## FÓRMULAS DE BACKTESTING

### 24. Win Rate Móvel (20 operações)
```excel
=CONT.SE(DESLOC(Resultados;-19;0;20;1);">0")/20
```

### 25. Profit Factor Móvel
```excel
=SOMASE(DESLOC(Resultados;-19;0;20;1);">0") / ABS(SOMASE(DESLOC(Resultados;-19;0;20;1);"<0"))
```

### 26. Máximo Drawdown Histórico
```excel
=MÁXIMO(Pico_Historico - Capital_Atual) / Pico_Historico
```

---

## ALERTAS AUTOMATIZADOS

### Sistema de Semáforo:
```excel
=SE(E(Sharpe>1.5; Drawdown<0.1; WinRate>0.55); "VERDE";
SE(OU(Sharpe<1; Drawdown>0.15; WinRate<0.45); "VERMELHO"; "AMARELO"))
```

### Score de Qualidade (0-100):
```excel
=MÍNIMO(100; 
   (Sharpe_Ratio/3*25) + 
   ((1-Drawdown_Max)*25) + 
   (Win_Rate*25) + 
   (MÍNIMO(Profit_Factor/2;1)*25))
```

---

## CONSIDERAÇÕES IMPORTANTES

1. **Todas as fórmulas assumem distribuição normal dos retornos**
2. **Ajuste os parâmetros conforme seu histórico de trading**
3. **Valide as fórmulas com dados reais antes de usar**
4. **Considere custos de transação em todos os cálculos**
5. **Revise periodicamente os parâmetros estatísticos**

---

**AVISO LEGAL**: Estas fórmulas são ferramentas de análise. Trading forex envolve risco substancial de perda. Sempre consulte um profissional qualificado antes de tomar decisões de investimento.