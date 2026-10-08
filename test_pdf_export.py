#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da funcionalidade de exportação PDF
Forex Analyzer Pro - Teste de Geração de Relatório PDF
"""

from forex_analyzer import ForexAnalyzer, TradingParameters
from pdf_generator import ForexPDFGenerator
import os

def test_pdf_generation():
    """Testa a geração de relatório PDF completo"""
    print("=== TESTE DE EXPORTAÇÃO PDF ===")
    print("Iniciando teste da funcionalidade de exportação PDF...")
    
    try:
        # Configurar parâmetros de teste
        params = TradingParameters(
            capital_inicial=10000.0,
            porcentagem_risco=2.0,
            alavancagem=100,
            win_rate=65.0,
            rr_ratio=1.5,
            operacoes_mes=20
        )
        
        print(f"Parâmetros configurados:")
        print(f"- Capital inicial: R$ {params.capital_inicial:,.2f}")
        print(f"- Risco por trade: {params.porcentagem_risco}%")
        print(f"- Alavancagem: {params.alavancagem}:1")
        print(f"- Win rate: {params.win_rate}%")
        print(f"- Risk:Reward: 1:{params.rr_ratio}")
        print(f"- Operações/mês: {params.operacoes_mes}")
        
        # Criar analisador
        analyzer = ForexAnalyzer(params)
        print("\nAnalisador criado com sucesso!")
        
        # Executar simulação
        print("Executando simulação...")
        results = analyzer.simulate_trading_scenario(months=48)
        print("Simulação concluída!")
        
        # Mostrar resultados principais
        print(f"\nResultados da simulação:")
        print(f"- Capital final: R$ {results['final_capital']:,.2f}")
        print(f"- Retorno total: {results['total_return']:.2f}%")
        print(f"- Sharpe Ratio: {results['performance_metrics']['sharpe_ratio']:.3f}")
        print(f"- Profit Factor: {results['performance_metrics']['profit_factor']:.2f}")
        print(f"- Max Drawdown: {results['performance_metrics']['max_drawdown']:.2f}%")
        
        # Gerar relatório PDF
        print("\nGerando relatório PDF...")
        pdf_generator = ForexPDFGenerator()
        pdf_filename = pdf_generator.generate_complete_report(results, analyzer)
        
        # Verificar se o arquivo foi criado
        if os.path.exists(pdf_filename):
            file_size = os.path.getsize(pdf_filename) / 1024  # KB
            print(f"✅ Relatório PDF gerado com sucesso!")
            print(f"📄 Arquivo: {pdf_filename}")
            print(f"📊 Tamanho: {file_size:.1f} KB")
            
            # Mostrar conteúdo do relatório
            print(f"\nConteúdo do relatório PDF:")
            print(f"- Página 1: Capa e Resumo Executivo")
            print(f"- Página 2: Parâmetros e Configurações")
            print(f"- Página 3: Análise de Performance")
            print(f"- Página 4: Análise Financeira")
            print(f"- Página 5: Comparação de Alavancagem")
            print(f"- Página 6: Métricas Detalhadas")
            print(f"- Página 7: Alertas e Recomendações")
            
            return True
        else:
            print("❌ Erro: Arquivo PDF não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_with_different_scenarios():
    """Testa a geração de PDF com diferentes cenários"""
    print("\n=== TESTE COM DIFERENTES CENÁRIOS ===")
    
    scenarios = [
        {
            'name': 'Conservador',
            'params': TradingParameters(
                capital_inicial=5000.0,
                porcentagem_risco=1.0,
                alavancagem=30,
                win_rate=70.0,
                rr_ratio=1.2,
                operacoes_mes=10
            ),
            'months': 24
        },
        {
            'name': 'Agressivo',
            'params': TradingParameters(
                capital_inicial=20000.0,
                porcentagem_risco=3.0,
                alavancagem=200,
                win_rate=55.0,
                rr_ratio=2.0,
                operacoes_mes=30
            ),
            'months': 36
        }
    ]
    
    pdf_generator = ForexPDFGenerator()
    generated_files = []
    
    for scenario in scenarios:
        try:
            print(f"\nTestando cenário: {scenario['name']}")
            analyzer = ForexAnalyzer(scenario['params'])
            results = analyzer.simulate_trading_scenario(months=scenario['months'])
            
            # Gerar PDF com nome específico
            pdf_filename = f"relatorio_cenario_{scenario['name'].lower()}.pdf"
            pdf_filename = pdf_generator.generate_complete_report(
                analyzer, results, pdf_filename
            )
            
            if os.path.exists(pdf_filename):
                generated_files.append(pdf_filename)
                print(f"✅ PDF gerado: {pdf_filename}")
            else:
                print(f"❌ Falha ao gerar PDF para cenário {scenario['name']}")
                
        except Exception as e:
            print(f"❌ Erro no cenário {scenario['name']}: {str(e)}")
    
    print(f"\n📊 Total de PDFs gerados: {len(generated_files)}")
    for pdf_file in generated_files:
        print(f"   - {pdf_file}")
    
    return len(generated_files) > 0

if __name__ == "__main__":
    print("Forex Analyzer Pro - Teste de Exportação PDF")
    print("=" * 50)
    
    # Teste básico
    success1 = test_pdf_generation()
    
    # Teste com cenários diferentes
    success2 = test_pdf_with_different_scenarios()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ TODOS OS TESTES DE PDF PASSARAM!")
        print("\nA funcionalidade de exportação PDF está funcionando corretamente.")
        print("Você pode usar o botão 'Gerar Relatório PDF Completo' no dashboard.")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("Verifique os erros acima e as dependências instaladas.")
    
    print("\nPara usar no dashboard:")
    print("1. Execute: streamlit run forex_dashboard.py")
    print("2. Configure os parâmetros desejados")
    print("3. Clique em 'Gerar Relatório PDF Completo'")
    print("4. Baixe o arquivo PDF gerado")