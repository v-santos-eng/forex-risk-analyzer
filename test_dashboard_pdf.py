#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar a funcionalidade de PDF no dashboard
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forex_analyzer import ForexAnalyzer, TradingParameters
from pdf_generator import ForexPDFGenerator

def test_dashboard_pdf_integration():
    """Testa a integração PDF como seria no dashboard"""
    print("=== TESTE DE INTEGRAÇÃO PDF DASHBOARD ===")
    
    try:
        # Simular parâmetros do dashboard
        params = TradingParameters(
            capital_inicial=10000,
            porcentagem_risco=2.0,
            alavancagem=100,
            win_rate=65.0,
            rr_ratio=1.5,
            operacoes_mes=20
        )
        
        print("✅ Parâmetros criados")
        
        # Criar analyzer (como no dashboard)
        analyzer = ForexAnalyzer(params)
        print("✅ Analyzer criado")
        
        # Executar simulação (como no dashboard)
        results = analyzer.simulate_trading_scenario(
            months=48,
            stop_loss_pips=20
        )
        print("✅ Simulação executada")
        
        # Testar geração PDF (como no dashboard)
        pdf_generator = ForexPDFGenerator()
        pdf_filename = pdf_generator.generate_complete_report(results, analyzer)
        
        print(f"✅ PDF gerado: {pdf_filename}")
        
        # Verificar se arquivo existe
        if os.path.exists(pdf_filename):
            file_size = os.path.getsize(pdf_filename)
            print(f"✅ Arquivo existe: {file_size} bytes")
            
            # Simular leitura do arquivo (como no dashboard)
            with open(pdf_filename, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            
            print(f"✅ Arquivo lido: {len(pdf_data)} bytes")
            
            # Limpar arquivo temporário (como no dashboard)
            try:
                os.remove(pdf_filename)
                print("✅ Arquivo temporário removido")
            except Exception as e:
                print(f"⚠️ Erro ao remover arquivo: {e}")
            
            return True
        else:
            print("❌ Arquivo PDF não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dashboard_pdf_integration()
    
    if success:
        print("\n🎉 TESTE DE INTEGRAÇÃO PDF PASSOU!")
        print("A funcionalidade está pronta para uso no dashboard.")
    else:
        print("\n❌ TESTE DE INTEGRAÇÃO PDF FALHOU!")
        print("Verifique os erros acima.")
    
    print("\n=== INSTRUÇÕES DE USO ===")
    print("1. Acesse o dashboard: http://localhost:8501")
    print("2. Configure os parâmetros desejados")
    print("3. Clique em 'Executar Análise'")
    print("4. Clique em 'Gerar Relatório PDF Completo'")
    print("5. Clique em '📄 Baixar Relatório PDF' quando aparecer")