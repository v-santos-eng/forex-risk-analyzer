import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import io
import os
import warnings
warnings.filterwarnings('ignore')

# Importar nossas classes
from forex_analyzer import ForexAnalyzer, TradingParameters
from position_calculator import AdvancedPositionCalculator, CurrencyPair, RiskLevel
from pdf_generator import ForexPDFGenerator

# Configuração da página
st.set_page_config(
    page_title="Forex Analyzer Pro",
    page_icon="FX",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
}
.alert-high {
    background-color: #ffebee;
    color: #c62828;
    padding: 0.5rem;
    border-radius: 0.25rem;
    border-left: 4px solid #c62828;
}
.alert-medium {
    background-color: #fff3e0;
    color: #ef6c00;
    padding: 0.5rem;
    border-radius: 0.25rem;
    border-left: 4px solid #ef6c00;
}
.alert-low {
    background-color: #e8f5e8;
    color: #2e7d32;
    padding: 0.5rem;
    border-radius: 0.25rem;
    border-left: 4px solid #2e7d32;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">Forex Analyzer Pro - Análise Quantitativa</h1>', unsafe_allow_html=True)
    
    # Sidebar para parâmetros
    st.sidebar.header("Configurações")
    
    # Seção 1: Parâmetros Básicos
    st.sidebar.subheader("Capital e Risco")
    capital_inicial = st.sidebar.number_input(
        "Capital Inicial (R$)",
        min_value=1000.0,
        max_value=1000000.0,
        value=10000.0,
        step=1000.0,
        format="%.2f"
    )
    
    porcentagem_risco = st.sidebar.slider(
        "Risco por Operação (%)",
        min_value=0.5,
        max_value=10.0,
        value=2.0,
        step=0.1,
        format="%.1f"
    )
    
    # Seção 2: Alavancagem
    st.sidebar.subheader("Alavancagem")
    alavancagem_options = [1, 5, 25, 30, 50, 100, 200, 300, 400, 500, 1000]
    alavancagem = st.sidebar.selectbox(
        "Nível de Alavancagem",
        options=alavancagem_options,
        index=3,  # 1:30 como padrão
        format_func=lambda x: f"1:{x}"
    )
    
    # Seção 3: Estratégia
    st.sidebar.subheader("Parâmetros da Estratégia")
    win_rate = st.sidebar.slider(
        "Win Rate (%)",
        min_value=30.0,
        max_value=90.0,
        value=65.0,
        step=1.0,
        format="%.1f"
    )
    
    rr_ratio = st.sidebar.slider(
        "Risk/Reward Ratio",
        min_value=0.5,
        max_value=5.0,
        value=1.5,
        step=0.1,
        format="%.1f"
    )
    
    # Seção 4: Custos Operacionais
    st.sidebar.subheader("Custos e Impostos")
    spread_pips = st.sidebar.number_input(
        "Spread Médio (pips)",
        min_value=0.5,
        max_value=10.0,
        value=2.0,
        step=0.1,
        format="%.1f"
    )
    
    comissao_pct = st.sidebar.number_input(
        "Comissão (%)",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        step=0.01,
        format="%.3f"
    )
    
    # Seção 5: Simulação
    st.sidebar.subheader("Simulação")
    meses_simulacao = st.sidebar.slider(
        "Período de Simulação (meses)",
        min_value=1,
        max_value=60,
        value=48,
        step=1
    )
    
    operacoes_mes = st.sidebar.slider(
        "Operações por Mês",
        min_value=5,
        max_value=100,
        value=20,
        step=5
    )
    
    stop_loss_pips = st.sidebar.number_input(
        "Stop Loss Padrão (pips)",
        min_value=5.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
        format="%.1f"
    )
    
    # Criar parâmetros
    params = TradingParameters(
        capital_inicial=capital_inicial,
        porcentagem_risco=porcentagem_risco,
        alavancagem=alavancagem,
        win_rate=win_rate,
        rr_ratio=rr_ratio,
        spread_pips=spread_pips,
        comissao_pct=comissao_pct,
        operacoes_mes=operacoes_mes
    )
    
    # Botão para executar análise
    if st.sidebar.button("Executar Análise", type="primary"):
        with st.spinner("Executando análise quantitativa..."):
            # Criar analisador
            analyzer = ForexAnalyzer(params)
            
            # Executar simulação
            results = analyzer.simulate_trading_scenario(
                months=meses_simulacao,
                stop_loss_pips=stop_loss_pips
            )
            
            # Armazenar resultados na sessão
            st.session_state['results'] = results
            st.session_state['params'] = params
            st.session_state['analyzer'] = analyzer
    
    # Exibir resultados se disponíveis
    if 'results' in st.session_state:
        display_results(st.session_state['results'], st.session_state['params'], st.session_state['analyzer'])
    else:
        # Tela inicial
        display_welcome_screen()

def display_welcome_screen():
    """Tela de boas-vindas com instruções"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Bem-vindo ao Forex Analyzer Pro!
        
        Este sistema oferece análise quantitativa avançada para trading forex com:
        
        **Cálculo automático de posições**  
        **Simulação de cenários realistas**  
        **Métricas de performance profissionais**  
        **Análise de risco-retorno**  
        **Impostos e custos brasileiros**  
        
        ### Como usar:
        1. Configure seus parâmetros na barra lateral
        2. Clique em "Executar Análise"
        3. Analise os resultados e gráficos
        4. Exporte os dados para análise posterior
        
        ### Importante:
        - Use parâmetros realistas baseados em sua experiência
        - Considere sempre os custos operacionais
        - Teste diferentes cenários de alavancagem
        - Mantenha disciplina de risco
        """)

def display_results(results, params, analyzer):
    """Exibe os resultados da análise"""
    
    # Métricas principais
    st.header("Resumo Executivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Capital Final",
            f"R$ {results['final_capital']:,.2f}",
            f"R$ {results['final_capital'] - params.capital_inicial:,.2f}"
        )
    
    with col2:
        st.metric(
            "Retorno Total",
            f"{results['total_return']:.2f}%",
            f"{results['total_return']/12:.2f}% ao mês" if len(results['monthly_results']) == 12 else ""
        )
    
    with col3:
        st.metric(
            "Sharpe Ratio",
            f"{results['performance_metrics']['sharpe_ratio']:.3f}",
            "Excelente" if results['performance_metrics']['sharpe_ratio'] > 1.5 else "Bom" if results['performance_metrics']['sharpe_ratio'] > 1.0 else "Regular"
        )
    
    with col4:
        st.metric(
            "Profit Factor",
            f"{results['performance_metrics']['profit_factor']:.2f}",
            "Lucrativo" if results['performance_metrics']['profit_factor'] > 1.0 else "Prejuízo"
        )
    
    # Alertas de risco
    st.header("Alertas de Risco")
    alerts = analyzer.get_risk_alerts()
    
    if alerts:
        for alert in alerts:
            alert_class = "alert-high" if alert['type'] in ['HIGH_RISK', 'HIGH_LEVERAGE'] else "alert-medium"
            st.markdown(f'<div class="{alert_class}">ALERTA: {alert["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-low">Todos os parâmetros estão dentro dos limites recomendados</div>', unsafe_allow_html=True)
    
    # Tabs para diferentes análises
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Performance", "Análise Financeira", "Alavancagem", "Métricas", "Monte Carlo", "Relatório"])
    
    with tab1:
        display_performance_charts(results)
    
    with tab2:
        display_financial_analysis(results)
    
    with tab3:
        display_leverage_analysis(params, analyzer)
    
    with tab4:
        display_detailed_metrics(results)
    
    with tab5:
        display_monte_carlo_explanation()
    
    with tab6:
        display_detailed_report(results, params, analyzer)

def display_performance_charts(results):
    """Exibe gráficos de performance"""
    
    # Preparar dados mensais
    monthly_df = pd.DataFrame(results['monthly_results'])
    
    # Gráfico 1: Evolução do Capital
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=monthly_df['month'],
        y=monthly_df['capital_end'],
        mode='lines+markers',
        name='Capital Total',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig1.update_layout(
        title="Evolução do Capital ao Longo do Tempo",
        xaxis_title="Mês",
        yaxis_title="Capital (R$)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Lucro Mensal
    fig2 = go.Figure()
    
    colors = ['green' if profit > 0 else 'red' for profit in monthly_df['net_profit']]
    
    fig2.add_trace(go.Bar(
        x=monthly_df['month'],
        y=monthly_df['net_profit'],
        name='Lucro Líquido Mensal',
        marker_color=colors
    ))
    
    fig2.update_layout(
        title="Lucro Líquido Mensal",
        xaxis_title="Mês",
        yaxis_title="Lucro (R$)",
        showlegend=False
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico 3: Distribuição de Custos
    total_costs = sum([month['total_costs'] for month in monthly_df.to_dict('records')])
    total_taxes = sum([month['total_taxes'] for month in monthly_df.to_dict('records')])
    
    fig3 = go.Figure(data=[go.Pie(
        labels=['Custos Operacionais', 'Impostos'],
        values=[total_costs, total_taxes],
        hole=0.3
    )])
    
    fig3.update_layout(title="Distribuição de Custos Totais")
    
    st.plotly_chart(fig3, use_container_width=True)

def display_financial_analysis(results):
    """Exibe análise financeira detalhada"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Análise de Lucros")
        
        monthly_df = pd.DataFrame(results['monthly_results'])
        
        total_gross_profit = sum([month['gross_profit'] for month in monthly_df.to_dict('records')])
        total_net_profit = sum([month['net_profit'] for month in monthly_df.to_dict('records')])
        total_costs = sum([month['total_costs'] for month in monthly_df.to_dict('records')])
        total_taxes = sum([month['total_taxes'] for month in monthly_df.to_dict('records')])
        
        st.metric("Lucro Bruto Total", f"R$ {total_gross_profit:,.2f}")
        st.metric("Lucro Líquido Total", f"R$ {total_net_profit:,.2f}")
        st.metric("Total de Custos", f"R$ {total_costs:,.2f}")
        st.metric("Total de Impostos", f"R$ {total_taxes:,.2f}")
        
        # Margem líquida
        margin = (total_net_profit / total_gross_profit * 100) if total_gross_profit > 0 else 0
        st.metric("Margem Líquida", f"{margin:.1f}%")
    
    with col2:
        st.subheader("Breakdown Mensal")
        
        # Tabela com dados mensais
        display_df = monthly_df[['month', 'net_profit', 'total_costs', 'total_taxes', 'capital_end']].copy()
        display_df.columns = ['Mês', 'Lucro Líquido', 'Custos', 'Impostos', 'Capital Final']
        
        # Formatar valores monetários
        for col in ['Lucro Líquido', 'Custos', 'Impostos', 'Capital Final']:
            display_df[col] = display_df[col].apply(lambda x: f"R$ {x:,.2f}")
        
        st.dataframe(display_df, use_container_width=True)

def display_leverage_analysis(params, analyzer):
    """Exibe análise de diferentes alavancagens"""
    
    st.subheader("Comparação de Alavancagens")
    
    # Comparar diferentes alavancagens
    leverage_scenarios = analyzer.compare_leverage_scenarios(
        leverage_list=[30, 50, 100, 200, 500],
        months=48
    )
    
    # Criar DataFrame para comparação
    comparison_data = []
    for scenario_name, data in leverage_scenarios.items():
        comparison_data.append({
            'Alavancagem': f"1:{data['leverage']}",
            'Retorno Total (%)': f"{data['total_return']:.2f}%",
            'Capital Final': f"R$ {data['final_capital']:,.2f}",
            'Sharpe Ratio': f"{data['sharpe_ratio']:.3f}",
            'Profit Factor': f"{data['profit_factor']:.2f}",
            'Max Drawdown': f"R$ {data['max_drawdown']:,.2f}",
            'Margem Necessária': f"R$ {data['margin_required']:,.2f}",
            'Tamanho Posição': f"{data['position_size']:.4f} lotes"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    # Gráfico de comparação
    leverage_values = [data['leverage'] for data in leverage_scenarios.values()]
    returns = [data['total_return'] for data in leverage_scenarios.values()]
    drawdowns = [data['max_drawdown'] for data in leverage_scenarios.values()]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Retorno vs Alavancagem', 'Drawdown vs Alavancagem')
    )
    
    fig.add_trace(
        go.Scatter(x=leverage_values, y=returns, mode='lines+markers', name='Retorno %'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=leverage_values, y=drawdowns, mode='lines+markers', name='Drawdown', line=dict(color='red')),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Alavancagem", row=1, col=1)
    fig.update_xaxes(title_text="Alavancagem", row=1, col=2)
    fig.update_yaxes(title_text="Retorno (%)", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown (R$)", row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)

def display_detailed_metrics(results):
    """Exibe métricas detalhadas"""
    
    metrics = results['performance_metrics']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Métricas de Performance")
        
        st.metric("Total de Trades", f"{metrics['total_trades']:,}")
        st.metric("Trades Vencedores", f"{metrics['winning_trades']:,}")
        st.metric("Trades Perdedores", f"{metrics['losing_trades']:,}")
        st.metric("Win Rate", f"{metrics['win_rate']:.1f}%")
        st.metric("Ganho Médio", f"R$ {metrics['avg_win']:,.2f}")
        st.metric("Perda Média", f"R$ {metrics['avg_loss']:,.2f}")
    
    with col2:
        st.subheader("Métricas Avançadas")
        
        st.metric("Expectativa Matemática", f"R$ {metrics['mathematical_expectancy']:,.2f}")
        st.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")
        st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.3f}")
        st.metric("Maximum Drawdown", f"R$ {metrics['max_drawdown']:,.2f}")
        st.metric("ROI Anual", f"{metrics['roi']:.2f}%")
        st.metric("Calmar Ratio", f"{metrics['calmar_ratio']:.3f}")
    
    # Interpretação das métricas
    st.subheader("Interpretação das Métricas")
    
    interpretations = {
        "Sharpe Ratio": {
            "value": metrics['sharpe_ratio'],
            "excellent": 2.0,
            "good": 1.0,
            "poor": 0.5,
            "interpretation": "Mede retorno ajustado ao risco"
        },
        "Profit Factor": {
            "value": metrics['profit_factor'],
            "excellent": 2.0,
            "good": 1.5,
            "poor": 1.0,
            "interpretation": "Razão entre lucros e perdas"
        },
        "Calmar Ratio": {
            "value": metrics['calmar_ratio'],
            "excellent": 1.0,
            "good": 0.5,
            "poor": 0.2,
            "interpretation": "Retorno anual / Maximum Drawdown"
        }
    }
    
    for metric_name, data in interpretations.items():
        value = data['value']
        if value >= data['excellent']:
            status = "Excelente"
        elif value >= data['good']:
            status = "🟡 Bom"
        elif value >= data['poor']:
            status = "Regular"
        else:
            status = "Ruim"
        
        st.write(f"**{metric_name}**: {value:.3f} - {status} - {data['interpretation']}")

def display_detailed_report(results, params, analyzer):
    """Exibe relatório detalhado"""
    
    st.subheader("Relatório Completo")
    
    # Seção 1: Parâmetros utilizados
    st.write("### Parâmetros da Simulação")
    
    param_data = {
        "Parâmetro": [
            "Capital Inicial",
            "Risco por Operação",
            "Alavancagem",
            "Win Rate",
            "Risk/Reward Ratio",
            "Spread Médio",
            "Comissão",
            "Operações por Mês"
        ],
        "Valor": [
            f"R$ {params.capital_inicial:,.2f}",
            f"{params.porcentagem_risco:.1f}%",
            f"1:{params.alavancagem}",
            f"{params.win_rate:.1f}%",
            f"{params.rr_ratio:.1f}",
            f"{params.spread_pips:.1f} pips",
            f"{params.comissao_pct:.3f}%",
            f"{params.operacoes_mes} trades"
        ]
    }
    
    st.dataframe(pd.DataFrame(param_data), use_container_width=True)
    
    # Seção 2: Resumo dos resultados
    st.write("### Resumo dos Resultados")
    
    metrics = results['performance_metrics']
    
    summary_text = f"""
    **Período de Simulação**: {len(results['monthly_results'])} meses  
    **Capital Final**: R$ {results['final_capital']:,.2f}  
    **Retorno Total**: {results['total_return']:.2f}%  
    **Retorno Mensal Médio**: {results['total_return']/len(results['monthly_results']):.2f}%  
    
    **Performance**:  
    - Total de Trades: {metrics['total_trades']:,}  
    - Win Rate Realizado: {metrics['win_rate']:.1f}%  
    - Profit Factor: {metrics['profit_factor']:.2f}  
    - Sharpe Ratio: {metrics['sharpe_ratio']:.3f}  
    - Maximum Drawdown: R$ {metrics['max_drawdown']:,.2f}  
    
    **Análise de Custos**:  
    - Custos Operacionais Totais: R$ {sum([m['total_costs'] for m in results['monthly_results']]):,.2f}  
    - Impostos Totais: R$ {sum([m['total_taxes'] for m in results['monthly_results']]):,.2f}  
    - Margem Líquida: {(sum([m['net_profit'] for m in results['monthly_results']]) / sum([abs(m['gross_profit']) for m in results['monthly_results']]) * 100):.1f}%  
    """
    
    st.markdown(summary_text)
    
    # Botões de exportação
    col1, col2 = st.columns(2)
    
    with col1:
        # Botão para download dos dados em CSV
        if st.button("Baixar Dados Completos (CSV)"):
            # Preparar dados para download
            monthly_df = pd.DataFrame(results['monthly_results'])
            trades_df = pd.DataFrame(results['trades_data'])
            
            # Criar arquivo CSV em memória
            import io
            buffer = io.StringIO()
            
            # Escrever dados mensais
            buffer.write("=== DADOS MENSAIS ===\n")
            monthly_df.to_csv(buffer, index=False)
            buffer.write("\n\n=== DADOS DOS TRADES ===\n")
            trades_df.to_csv(buffer, index=False)
            
            # Download
            st.download_button(
                label="Download CSV",
                data=buffer.getvalue(),
                file_name=f"forex_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        # Botão para gerar relatório PDF
        if st.button("Gerar Relatório PDF Completo", type="primary"):
            try:
                with st.spinner("Gerando relatório PDF... Isso pode levar alguns minutos."):
                    pdf_generator = ForexPDFGenerator()
                    pdf_filename = pdf_generator.generate_complete_report(results, analyzer)
                    
                    # Ler o arquivo PDF gerado
                    with open(pdf_filename, "rb") as pdf_file:
                        pdf_data = pdf_file.read()
                    
                    # Criar nome de arquivo mais amigável
                    friendly_filename = f"relatorio_forex_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    # Botão de download do PDF
                    st.download_button(
                        label="📄 Baixar Relatório PDF",
                        data=pdf_data,
                        file_name=friendly_filename,
                        mime="application/pdf",
                        key="download_pdf"
                    )
                    
                    # Limpar arquivo temporário
                    try:
                        os.remove(pdf_filename)
                    except:
                        pass
                    
                    st.success("✅ Relatório PDF gerado com sucesso! Clique no botão acima para baixar.")
                    
            except Exception as e:
                st.error(f"❌ Erro ao gerar relatório PDF: {str(e)}")
                st.info("💡 Certifique-se de que todas as dependências estão instaladas: pip install reportlab")
                # Debug adicional
                import traceback
                st.code(traceback.format_exc())

def display_monte_carlo_explanation():
    """Exibe explicação detalhada sobre simulação de Monte Carlo"""
    
    st.header("📊 Simulação de Monte Carlo")
    
    # Introdução
    st.markdown("""
    ### 🎯 Definição
    
    A simulação de Monte Carlo é um método computacional estatístico que utiliza **amostragem aleatória repetida** 
    para resolver problemas matemáticos complexos e modelar sistemas com incerteza. O método recebe esse nome em 
    homenagem ao famoso cassino de Monte Carlo, devido ao uso extensivo de números aleatórios.
    
    **Princípio fundamental**: Transformar problemas determinísticos complexos em problemas probabilísticos mais 
    simples através da geração de amostras aleatórias.
    """)
    
    # Processo passo a passo
    st.subheader("🔄 Processo Passo a Passo")
    
    with st.expander("1. Definição do Problema", expanded=False):
        st.markdown("""
        - **Identificar variáveis de entrada** (inputs) que possuem incerteza
        - **Definir variável de saída** (output) que se deseja analisar  
        - **Estabelecer relações matemáticas** entre inputs e outputs
        
        **Exemplo no Trading Forex:**
        - *Inputs*: Win rate, Risk/Reward ratio, spread, volatilidade
        - *Output*: Retorno do portfólio, drawdown máximo
        """)
    
    with st.expander("2. Modelagem Matemática", expanded=False):
        st.code("""
# Exemplo: Cálculo de retorno de portfólio
def modelo_portfolio(win_rate, rr_ratio, n_trades, capital_inicial):
    resultados = []
    capital_atual = capital_inicial
    
    for trade in range(n_trades):
        # Simular resultado do trade
        if np.random.random() < win_rate:
            # Trade vencedor
            lucro = capital_atual * 0.02 * rr_ratio  # 2% de risco
            capital_atual += lucro
        else:
            # Trade perdedor
            perda = capital_atual * 0.02
            capital_atual -= perda
        
        resultados.append(capital_atual)
    
    return resultados
        """, language="python")
    
    with st.expander("3. Especificação das Distribuições", expanded=False):
        st.markdown("""
        **Distribuições Comuns em Finanças:**
        
        - **Normal**: Para retornos de ativos financeiros
        - **Log-normal**: Para preços de ações
        - **Uniforme**: Para parâmetros com faixas conhecidas
        - **Triangular**: Para estimativas com valor mais provável
        - **Beta**: Para win rates e probabilidades
        """)
        
        st.code("""
import numpy as np
from scipy import stats

# Distribuição normal para retornos
retornos = np.random.normal(mu=0.01, sigma=0.05, size=1000)

# Distribuição beta para win rate (entre 0 e 1)
win_rates = np.random.beta(a=6, b=4, size=1000)  # Média ~0.6

# Distribuição triangular para R:R ratio
rr_ratios = np.random.triangular(left=1.0, mode=1.5, right=3.0, size=1000)
        """, language="python")
    
    with st.expander("4. Execução das Simulações", expanded=False):
        st.code("""
def simulacao_monte_carlo(n_simulacoes=10000):
    resultados_finais = []
    
    for i in range(n_simulacoes):
        # Gerar parâmetros aleatórios
        win_rate = np.random.beta(6, 4)  # Win rate variável
        rr_ratio = np.random.triangular(1.0, 1.5, 3.0)  # R:R variável
        n_trades = np.random.poisson(20)  # Número de trades por mês
        
        # Executar simulação do mês
        resultado_mes = modelo_portfolio(win_rate, rr_ratio, n_trades, 10000)
        resultados_finais.append(resultado_mes[-1])  # Capital final
    
    return np.array(resultados_finais)

# Executar simulação
resultados = simulacao_monte_carlo(10000)
        """, language="python")
    
    with st.expander("5. Análise Estatística dos Resultados", expanded=False):
        st.code("""
# Estatísticas descritivas
media = np.mean(resultados)
desvio_padrao = np.std(resultados)
percentis = np.percentile(resultados, [5, 25, 50, 75, 95])

# Métricas de risco
var_95 = np.percentile(resultados, 5)  # Value at Risk 95%
cvar_95 = np.mean(resultados[resultados <= var_95])  # Conditional VaR

# Probabilidade de lucro
prob_lucro = np.mean(resultados > capital_inicial)

# Máximo drawdown esperado
drawdowns = (capital_inicial - resultados) / capital_inicial
max_drawdown_esperado = np.percentile(drawdowns, 95)
        """, language="python")
    
    # Aplicações
    st.subheader("🎯 Aplicações no Trading Forex")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Gestão de Risco:**
        - Cálculo de Value at Risk (VaR)
        - Expected Shortfall (CVaR)
        - Probabilidade de ruína
        - Drawdown máximo esperado
        
        **Otimização de Estratégias:**
        - Teste de diferentes win rates
        - Análise de R:R ratios ótimos
        - Dimensionamento de posições
        - Frequência de trading
        """)
    
    with col2:
        st.markdown("""
        **Análise de Cenários:**
        - Stress testing de portfólios
        - Simulação de crises de mercado
        - Impacto de mudanças regulatórias
        - Análise de correlações extremas
        
        **Precificação:**
        - Opções exóticas
        - Produtos estruturados
        - Derivativos complexos
        """)
    
    # Vantagens
    st.subheader("✅ Vantagens Técnicas")
    
    st.markdown("""
    **Flexibilidade Modelística:**
    - Incorpora distribuições não-normais complexas
    - Modela correlações e dependências não-lineares  
    - Permite análise de cenários extremos (tail events)
    
    **Robustez Estatística:**
    - Convergência garantida pela Lei dos Grandes Números
    - Intervalos de confiança através do Teorema Central do Limite
    - Análise de sensibilidade através de variação paramétrica
    
    **Interpretabilidade:**
    - Resultados em formato de distribuições de probabilidade
    - Métricas de risco quantificadas
    - Visualização clara de cenários possíveis
    """)
    
    # Limitações
    st.subheader("⚠️ Limitações e Considerações Críticas")
    
    with st.expander("Convergência e Precisão", expanded=False):
        st.markdown("""
        - **Erro padrão**: Proporcional a 1/√n, onde n é o número de simulações
        - **Regra prática**: 10.000 simulações para precisão de 1%, 1.000.000 para 0.1%
        - **Técnicas de redução de variância**: Antithetic variates, control variates, importance sampling
        """)
        
        st.code("""
# Cálculo do erro padrão
def calcular_erro_padrao(resultados):
    n = len(resultados)
    std = np.std(resultados)
    erro_padrao = std / np.sqrt(n)
    
    # Intervalo de confiança 95%
    media = np.mean(resultados)
    ic_inferior = media - 1.96 * erro_padrao
    ic_superior = media + 1.96 * erro_padrao
    
    return erro_padrao, (ic_inferior, ic_superior)
        """, language="python")
    
    with st.expander("Qualidade do Modelo", expanded=False):
        st.markdown("""
        - **Garbage in, garbage out**: Resultados dependem criticamente das premissas
        - **Validação necessária**: Backtesting, comparação com dados históricos
        - **Model risk**: Risco de especificação incorreta das distribuições
        - **Overfitting**: Cuidado com modelos excessivamente complexos
        """)
    
    with st.expander("Complexidade Computacional", expanded=False):
        st.markdown("""
        - **Tempo de processamento**: Cresce linearmente com número de simulações
        - **Memória**: Pode ser limitante para simulações muito grandes
        - **Paralelização**: Essencial para simulações complexas
        """)
        
        st.code("""
# Otimização computacional
import multiprocessing as mp
from numba import jit

@jit(nopython=True)  # Compilação JIT para aceleração
def simulacao_otimizada(n_simulacoes):
    # Código otimizado com Numba
    pass

# Paralelização
def simulacao_paralela(n_simulacoes, n_processos=4):
    with mp.Pool(n_processos) as pool:
        chunk_size = n_simulacoes // n_processos
        resultados_parciais = pool.map(simulacao_otimizada, 
                                     [chunk_size] * n_processos)
    return np.concatenate(resultados_parciais)
        """, language="python")
    
    # Implementação prática
    st.subheader("🛠️ Implementação Prática Completa")
    
    with st.expander("Classe MonteCarloSimulator", expanded=False):
        st.code("""
class MonteCarloSimulator:
    def __init__(self, modelo, distribuicoes, n_simulacoes=10000):
        self.modelo = modelo
        self.distribuicoes = distribuicoes
        self.n_simulacoes = n_simulacoes
        self.resultados = None
    
    def executar_simulacao(self):
        resultados = []
        
        for _ in range(self.n_simulacoes):
            # Gerar inputs aleatórios
            inputs = {}
            for var, dist in self.distribuicoes.items():
                inputs[var] = dist.rvs()
            
            # Executar modelo
            resultado = self.modelo(**inputs)
            resultados.append(resultado)
        
        self.resultados = np.array(resultados)
        return self.resultados
    
    def calcular_metricas(self):
        if self.resultados is None:
            raise ValueError("Execute a simulação primeiro")
        
        return {
            'media': np.mean(self.resultados),
            'desvio_padrao': np.std(self.resultados),
            'var_95': np.percentile(self.resultados, 5),
            'var_99': np.percentile(self.resultados, 1),
            'percentis': np.percentile(self.resultados, [10, 25, 50, 75, 90]),
            'prob_lucro': np.mean(self.resultados > 0)
        }
    
    def analise_sensibilidade(self, variacao_pct=0.1):
        # Análise de sensibilidade dos parâmetros
        sensibilidades = {}
        resultado_base = np.mean(self.resultados)
        
        for param in self.distribuicoes.keys():
            # Variar parâmetro e recalcular
            # ... implementação da análise de sensibilidade
            pass
        
        return sensibilidades
        """, language="python")
    
    # Conclusão
    st.subheader("🎯 Conclusão Técnica")
    
    st.info("""
    **A simulação de Monte Carlo é uma ferramenta fundamental na análise quantitativa moderna**, 
    especialmente em contextos com alta incerteza e complexidade. 
    
    **Sua eficácia depende criticamente de:**
    - Qualidade da modelagem matemática
    - Número adequado de simulações (mínimo 10.000)
    - Validação rigorosa dos resultados
    - Especificação correta das distribuições de probabilidade
    
    **Para aplicações em trading forex, recomenda-se sempre complementar com:**
    - Análise de sensibilidade
    - Stress testing
    - Backtesting com dados históricos
    - Validação out-of-sample
    """)
    
    # Exemplo interativo
    st.subheader("🎮 Exemplo Interativo Simples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Parâmetros da Simulação:**")
        sim_win_rate = st.slider("Win Rate (%)", 40, 80, 60) / 100
        sim_rr_ratio = st.slider("Risk/Reward Ratio", 1.0, 3.0, 1.5, 0.1)
        sim_n_trades = st.slider("Trades por Mês", 10, 50, 20)
        sim_capital = st.number_input("Capital Inicial (R$)", 1000, 100000, 10000)
    
    with col2:
        if st.button("🎲 Executar Simulação Monte Carlo", type="primary"):
            # Simulação simples
            n_simulacoes = 1000
            resultados_sim = []
            
            for _ in range(n_simulacoes):
                capital_atual = sim_capital
                for _ in range(sim_n_trades):
                    if np.random.random() < sim_win_rate:
                        capital_atual += capital_atual * 0.02 * sim_rr_ratio
                    else:
                        capital_atual -= capital_atual * 0.02
                resultados_sim.append(capital_atual)
            
            resultados_sim = np.array(resultados_sim)
            
            # Métricas
            st.markdown("**Resultados da Simulação:**")
            st.metric("Capital Médio Final", f"R$ {np.mean(resultados_sim):,.2f}")
            st.metric("Probabilidade de Lucro", f"{np.mean(resultados_sim > sim_capital)*100:.1f}%")
            st.metric("VaR 95%", f"R$ {sim_capital - np.percentile(resultados_sim, 5):,.2f}")
            
            # Gráfico simples
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=resultados_sim,
                nbinsx=50,
                name="Distribuição dos Resultados",
                marker_color="lightblue"
            ))
            fig.add_vline(x=sim_capital, line_dash="dash", line_color="red", 
                         annotation_text="Capital Inicial")
            fig.update_layout(
                title="Distribuição dos Resultados - Monte Carlo",
                xaxis_title="Capital Final (R$)",
                yaxis_title="Frequência"
            )
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()