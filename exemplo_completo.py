#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Completo - Forex Analyzer Pro
Demonstra todas as funcionalidades do sistema de análise quantitativa

Autor: Sistema de Análise Quantitativa
Data: 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importar nossas classes
from forex_analyzer import ForexAnalyzer, TradingParameters
from position_calculator import AdvancedPositionCalculator, CurrencyPair, RiskLevel, MarketConditions

def exemplo_basico():
    """Exemplo básico de uso do ForexAnalyzer"""
    print("=" * 60)
    print("EXEMPLO 1: ANÁLISE BÁSICA DE TRADING FOREX")
    print("=" * 60)
    
    # Configurar parâmetros para trader conservador
    params = TradingParameters(
        capital_inicial=10000.0,
        porcentagem_risco=2.0,
        alavancagem=30,
        win_rate=65.0,
        rr_ratio=1.5,
        spread_pips=2.0,
        comissao_pct=0.05,
        operacoes_mes=20
    )
    
    # Criar analisador
    analyzer = ForexAnalyzer(params)
    
    # Executar simulação de 48 meses
    results = analyzer.simulate_trading_scenario(months=48, stop_loss_pips=20)
    
    # Exibir resultados principais
    print(f"Capital Inicial: R$ {params.capital_inicial:,.2f}")
    print(f"Capital Final: R$ {results['final_capital']:,.2f}")
    print(f"Retorno Total: {results['total_return']:.2f}%")
    print(f"Retorno Mensal Médio: {results['total_return']/48:.2f}%")
    
    # Métricas de performance
    metrics = results['performance_metrics']
    print(f"\nMÉTRICAS DE PERFORMANCE:")
    print(f"Win Rate: {metrics['win_rate']:.1f}%")
    print(f"Profit Factor: {metrics['profit_factor']:.2f}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
    print(f"Maximum Drawdown: R$ {metrics['max_drawdown']:,.2f}")
    print(f"Expectativa Matemática: R$ {metrics['mathematical_expectancy']:,.2f}")
    
    # Verificar alertas de risco
    alerts = analyzer.get_risk_alerts()
    if alerts:
        print(f"\nALERTAS DE RISCO:")
        for alert in alerts:
            print(f"   - {alert['message']}")
    else:
        print(f"\nTodos os parâmetros estão dentro dos limites recomendados")
    
    return results, analyzer

def exemplo_calculadora_posicao():
    """Exemplo de uso da calculadora avançada de posições"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: CALCULADORA AVANÇADA DE POSIÇÕES")
    print("=" * 60)
    
    calculator = AdvancedPositionCalculator()
    
    # Exemplo 1: Cálculo básico de posição
    print("\n1. CÁLCULO BÁSICO DE POSIÇÃO:")
    position = calculator.calculate_position_size_fixed_risk(
        account_balance=10000,
        risk_percentage=2.0,
        stop_loss_pips=20,
        currency_pair=CurrencyPair.EURUSD
    )
    
    print(calculator.generate_position_summary(position))
    
    # Exemplo 2: Critério de Kelly
    print("\n2. CRITÉRIO DE KELLY:")
    kelly_result = calculator.calculate_position_size_kelly_criterion(
        account_balance=10000,
        win_rate=65,
        avg_win=150,
        avg_loss=100
    )
    
    print(f"Fração de Kelly: {kelly_result['kelly_fraction']:.3f}")
    print(f"Risco Ótimo: {kelly_result['optimal_risk_percentage']:.2f}%")
    print(f"Valor em Risco: R$ {kelly_result['risk_amount']:,.2f}")
    print(f"Recomendação: {kelly_result['recommendation']}")
    
    # Exemplo 3: Ajuste por volatilidade
    print("\n3. AJUSTE POR VOLATILIDADE:")
    volatility_position = calculator.calculate_position_size_volatility_adjusted(
        account_balance=10000,
        base_risk_pct=2.0,
        current_volatility=1.5,  # 50% mais volátil que o normal
        average_volatility=1.0,
        stop_loss_pips=20,
        currency_pair=CurrencyPair.EURUSD
    )
    
    print(f"Risco Base: {volatility_position['base_risk_pct']:.2f}%")
    print(f"Risco Ajustado: {volatility_position['adjusted_risk_pct']:.2f}%")
    print(f"Ajuste: {volatility_position['volatility_adjustment']}")
    print(f"Tamanho da Posição: {volatility_position['position_size_lots']:.4f} lotes")
    
    # Exemplo 4: Stop loss ótimo
    print("\n4. STOP LOSS ÓTIMO:")
    stop_loss = calculator.calculate_optimal_stop_loss(
        currency_pair=CurrencyPair.EURUSD,
        timeframe='H1',
        atr_multiplier=2.0
    )
    
    print(f"ATR Base: {stop_loss['base_atr_pips']} pips")
    print(f"Stop Loss Recomendado: {stop_loss['adjusted_stop_pips']:.1f} pips")
    print(f"Spread: {stop_loss['spread_pips']} pips")
    
    # Exemplo 5: Níveis de take profit
    print("\n5. NÍVEIS DE TAKE PROFIT:")
    tp_levels = calculator.calculate_take_profit_levels(stop_loss_pips=20)
    
    for level in tp_levels['take_profit_levels']:
        print(f"R:R {level['rr_ratio']}: {level['take_profit_pips']:.1f} pips (Fechar {level['partial_close_pct']}%)")

def exemplo_comparacao_alavancagem():
    """Exemplo de comparação entre diferentes alavancagens"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: COMPARAÇÃO DE ALAVANCAGENS")
    print("=" * 60)
    
    # Parâmetros base
    params = TradingParameters(
        capital_inicial=10000.0,
        porcentagem_risco=2.0,
        alavancagem=30,  # Será alterado na comparação
        win_rate=65.0,
        rr_ratio=1.5
    )
    
    analyzer = ForexAnalyzer(params)
    
    # Comparar diferentes alavancagens
    leverage_scenarios = analyzer.compare_leverage_scenarios(
        leverage_list=[30, 50, 100, 200, 500],
        months=48
    )
    
    print(f"{'Alavancagem':<12} {'Retorno':<10} {'Sharpe':<8} {'P.Factor':<9} {'Drawdown':<12} {'Margem':<12}")
    print("-" * 70)
    
    for scenario_name, data in leverage_scenarios.items():
        leverage = data['leverage']
        return_pct = data['total_return']
        sharpe = data['sharpe_ratio']
        pf = data['profit_factor']
        dd = data['max_drawdown']
        margin = data['margin_required']
        
        print(f"1:{leverage:<9} {return_pct:>7.2f}% {sharpe:>7.3f} {pf:>8.2f} R${dd:>9,.0f} R${margin:>9,.0f}")
    
    # Recomendação
    print("\nANÁLISE:")
    best_sharpe = max(leverage_scenarios.values(), key=lambda x: x['sharpe_ratio'])
    best_return = max(leverage_scenarios.values(), key=lambda x: x['total_return'])
    
    print(f"Melhor Sharpe Ratio: 1:{best_sharpe['leverage']} ({best_sharpe['sharpe_ratio']:.3f})")
    print(f"Maior Retorno: 1:{best_return['leverage']} ({best_return['total_return']:.2f}%)")
    
    if best_sharpe['leverage'] <= 100:
        print("Recomendação: Alavancagem conservadora com bom risco-retorno")
    else:
        print("Cuidado: Alavancagem alta pode aumentar significativamente o risco")

def exemplo_cenarios_estrategia():
    """Exemplo de diferentes cenários de estratégia"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: CENÁRIOS DE ESTRATÉGIAS")
    print("=" * 60)
    
    estrategias = {
        "Conservadora": {
            "porcentagem_risco": 1.0,
            "alavancagem": 30,
            "win_rate": 70.0,
            "rr_ratio": 1.2,
            "operacoes_mes": 15
        },
        "Moderada": {
            "porcentagem_risco": 2.0,
            "alavancagem": 50,
            "win_rate": 65.0,
            "rr_ratio": 1.5,
            "operacoes_mes": 20
        },
        "Agressiva": {
            "porcentagem_risco": 3.0,
            "alavancagem": 100,
            "win_rate": 60.0,
            "rr_ratio": 2.0,
            "operacoes_mes": 25
        },
        "Especulativa": {
            "porcentagem_risco": 5.0,
            "alavancagem": 200,
            "win_rate": 55.0,
            "rr_ratio": 2.5,
            "operacoes_mes": 30
        }
    }
    
    resultados_estrategias = {}
    
    for nome, config in estrategias.items():
        params = TradingParameters(
            capital_inicial=10000.0,
            porcentagem_risco=config["porcentagem_risco"],
            alavancagem=config["alavancagem"],
            win_rate=config["win_rate"],
            rr_ratio=config["rr_ratio"],
            operacoes_mes=config["operacoes_mes"]
        )
        
        analyzer = ForexAnalyzer(params)
        results = analyzer.simulate_trading_scenario(months=48, stop_loss_pips=20)
        
        resultados_estrategias[nome] = {
            'retorno': results['total_return'],
            'capital_final': results['final_capital'],
            'sharpe': results['performance_metrics']['sharpe_ratio'],
            'profit_factor': results['performance_metrics']['profit_factor'],
            'max_drawdown': results['performance_metrics']['max_drawdown'],
            'win_rate_real': results['performance_metrics']['win_rate']
        }
    
    # Exibir comparação
    print(f"{'Estratégia':<13} {'Retorno':<10} {'Capital Final':<15} {'Sharpe':<8} {'P.Factor':<9} {'Drawdown':<12}")
    print("-" * 80)
    
    for nome, dados in resultados_estrategias.items():
        print(f"{nome:<13} {dados['retorno']:>7.2f}% R${dados['capital_final']:>11,.0f} {dados['sharpe']:>7.3f} {dados['profit_factor']:>8.2f} R${dados['max_drawdown']:>9,.0f}")
    
    # Análise de risco-retorno
    print("\nANÁLISE RISCO-RETORNO:")
    
    for nome, dados in resultados_estrategias.items():
        risco_score = (dados['max_drawdown'] / 10000) * 100  # % do capital inicial
        retorno_score = dados['retorno']
        ratio = retorno_score / risco_score if risco_score > 0 else 0
        
        print(f"{nome}: Retorno/Risco = {ratio:.2f} (Retorno: {retorno_score:.1f}%, Risco: {risco_score:.1f}%)")

def exemplo_analise_custos():
    """Exemplo de análise detalhada de custos"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: ANÁLISE DETALHADA DE CUSTOS")
    print("=" * 60)
    
    # Parâmetros com diferentes custos
    cenarios_custos = {
        "Broker Premium": {
            "spread_pips": 1.0,
            "comissao_pct": 0.02,
            "swap_diario": 0.01
        },
        "Broker Padrão": {
            "spread_pips": 2.0,
            "comissao_pct": 0.05,
            "swap_diario": 0.02
        },
        "Broker Econômico": {
            "spread_pips": 3.0,
            "comissao_pct": 0.08,
            "swap_diario": 0.03
        }
    }
    
    for nome_broker, custos in cenarios_custos.items():
        print(f"\n--- {nome_broker.upper()} ---")
        
        params = TradingParameters(
            capital_inicial=10000.0,
            porcentagem_risco=2.0,
            alavancagem=50,
            win_rate=65.0,
            rr_ratio=1.5,
            spread_pips=custos["spread_pips"],
            comissao_pct=custos["comissao_pct"],
            swap_diario=custos["swap_diario"],
            operacoes_mes=20
        )
        
        analyzer = ForexAnalyzer(params)
        results = analyzer.simulate_trading_scenario(months=48, stop_loss_pips=20)
        
        # Calcular custos totais
        monthly_results = results['monthly_results']
        total_costs = sum([month['total_costs'] for month in monthly_results])
        total_taxes = sum([month['total_taxes'] for month in monthly_results])
        total_gross = sum([month['gross_profit'] for month in monthly_results])
        total_net = sum([month['net_profit'] for month in monthly_results])
        
        print(f"Lucro Bruto: R$ {total_gross:,.2f}")
        print(f"Custos Operacionais: R$ {total_costs:,.2f}")
        print(f"Impostos: R$ {total_taxes:,.2f}")
        print(f"Lucro Líquido: R$ {total_net:,.2f}")
        print(f"Margem Líquida: {(total_net/total_gross*100):.1f}%")
        print(f"Retorno Total: {results['total_return']:.2f}%")

def exemplo_monte_carlo():
    """Exemplo de simulação Monte Carlo"""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: SIMULAÇÃO MONTE CARLO")
    print("=" * 60)
    
    params = TradingParameters(
        capital_inicial=10000.0,
        porcentagem_risco=2.0,
        alavancagem=50,
        win_rate=65.0,
        rr_ratio=1.5
    )
    
    # Executar múltiplas simulações
    num_simulacoes = 100
    resultados_mc = []
    
    print(f"Executando {num_simulacoes} simulações Monte Carlo...")
    
    for i in range(num_simulacoes):
        analyzer = ForexAnalyzer(params)
        results = analyzer.simulate_trading_scenario(months=48, stop_loss_pips=20)
        resultados_mc.append({
            'retorno': results['total_return'],
            'capital_final': results['final_capital'],
            'sharpe': results['performance_metrics']['sharpe_ratio'],
            'max_drawdown': results['performance_metrics']['max_drawdown']
        })
    
    # Análise estatística
    df_mc = pd.DataFrame(resultados_mc)
    
    print(f"\nRESULTADOS MONTE CARLO ({num_simulacoes} simulações):")
    print(f"Retorno Médio: {df_mc['retorno'].mean():.2f}% ± {df_mc['retorno'].std():.2f}%")
    print(f"Retorno Mediano: {df_mc['retorno'].median():.2f}%")
    print(f"Melhor Caso: {df_mc['retorno'].max():.2f}%")
    print(f"Pior Caso: {df_mc['retorno'].min():.2f}%")
    
    # Percentis
    print(f"\nPERCENTIS:")
    print(f"5%: {df_mc['retorno'].quantile(0.05):.2f}%")
    print(f"25%: {df_mc['retorno'].quantile(0.25):.2f}%")
    print(f"75%: {df_mc['retorno'].quantile(0.75):.2f}%")
    print(f"95%: {df_mc['retorno'].quantile(0.95):.2f}%")
    
    # Probabilidade de lucro
    prob_lucro = (df_mc['retorno'] > 0).mean() * 100
    print(f"\nProbabilidade de Lucro: {prob_lucro:.1f}%")
    
    # Drawdown médio
    print(f"Drawdown Médio: R$ {df_mc['max_drawdown'].mean():,.2f}")
    print(f"Drawdown Máximo: R$ {df_mc['max_drawdown'].max():,.2f}")

def gerar_relatorio_completo():
    """Gera um relatório completo em Excel"""
    print("\n" + "=" * 60)
    print("GERANDO RELATÓRIO COMPLETO EM EXCEL")
    print("=" * 60)
    
    # Parâmetros para relatório
    params = TradingParameters(
        capital_inicial=10000.0,
        porcentagem_risco=2.0,
        alavancagem=50,
        win_rate=65.0,
        rr_ratio=1.5,
        operacoes_mes=20
    )
    
    analyzer = ForexAnalyzer(params)
    results = analyzer.simulate_trading_scenario(months=48, stop_loss_pips=20)
    
    # Criar DataFrames
    monthly_df = pd.DataFrame(results['monthly_results'])
    trades_df = pd.DataFrame(results['trades_data'])
    metrics_df = pd.DataFrame([results['performance_metrics']])
    
    # Salvar em Excel
    filename = f"relatorio_forex_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Aba 1: Resumo
        summary_data = {
            'Parâmetro': [
                'Capital Inicial', 'Capital Final', 'Retorno Total (%)',
                'Retorno Mensal Médio (%)', 'Win Rate (%)', 'Profit Factor',
                'Sharpe Ratio', 'Maximum Drawdown', 'Total de Trades'
            ],
            'Valor': [
                f"R$ {params.capital_inicial:,.2f}",
                f"R$ {results['final_capital']:,.2f}",
                f"{results['total_return']:.2f}%",
                f"{results['total_return']/48:.2f}%",
                f"{results['performance_metrics']['win_rate']:.1f}%",
                f"{results['performance_metrics']['profit_factor']:.2f}",
                f"{results['performance_metrics']['sharpe_ratio']:.3f}",
                f"R$ {results['performance_metrics']['max_drawdown']:,.2f}",
                f"{results['performance_metrics']['total_trades']:,}"
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Resumo', index=False)
        
        # Aba 2: Dados Mensais
        monthly_df.to_excel(writer, sheet_name='Dados_Mensais', index=False)
        
        # Aba 3: Todos os Trades
        trades_df.to_excel(writer, sheet_name='Todos_Trades', index=False)
        
        # Aba 4: Métricas Detalhadas
        metrics_df.to_excel(writer, sheet_name='Metricas', index=False)
    
    print(f"Relatório salvo como: {filename}")
    return filename

def main():
    """Função principal que executa todos os exemplos"""
    print("FOREX ANALYZER PRO - EXEMPLOS COMPLETOS")
    print("Sistema de Análise Quantitativa para Trading Forex")
    print("=" * 60)
    
    try:
        # Executar todos os exemplos
        exemplo_basico()
        exemplo_calculadora_posicao()
        exemplo_comparacao_alavancagem()
        exemplo_cenarios_estrategia()
        exemplo_analise_custos()
        exemplo_monte_carlo()
        
        # Gerar relatório final
        relatorio_file = gerar_relatorio_completo()
        
        print("\n" + "=" * 60)
        print("TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("=" * 60)
        print(f"Relatório completo: {relatorio_file}")
        print("Para interface web, execute: streamlit run forex_dashboard.py")
        print("Documentação completa disponível nos arquivos .md")
        
    except Exception as e:
        print(f"Erro durante execução: {str(e)}")
        print("Verifique se todas as dependências estão instaladas:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()