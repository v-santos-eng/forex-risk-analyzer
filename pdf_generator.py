import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import base64
from typing import Dict, Any
import numpy as np

class ForexPDFGenerator:
    """Gerador de relatórios PDF completos para análise forex"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configura estilos personalizados para o PDF"""
        # Título principal - cor mais moderna
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.Color(0.2, 0.3, 0.5)  # Azul escuro moderno
        ))
        
        # Subtítulo - cor verde mais suave
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_LEFT,
            textColor=colors.Color(0.1, 0.4, 0.2)  # Verde escuro
        ))
        
        # Texto de métricas
        self.styles.add(ParagraphStyle(
            name='MetricStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_LEFT,
            textColor=colors.Color(0.2, 0.2, 0.2)  # Cinza escuro
        ))
        
        # Alerta - cores mais suaves
        self.styles.add(ParagraphStyle(
            name='AlertStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_LEFT,
            textColor=colors.Color(0.6, 0.1, 0.1),  # Vermelho escuro
            backColor=colors.Color(0.95, 0.95, 0.95)  # Cinza muito claro
        ))
    
    def generate_complete_report(self, results: Dict, analyzer, filename: str = None) -> str:
        """Gera relatório PDF completo com todas as seções"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'relatorio_forex_completo_{timestamp}.pdf'
        
        # Criar documento PDF
        doc = SimpleDocTemplate(filename, pagesize=A4, 
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Página 1: Capa e Resumo Executivo
        story.extend(self._create_cover_page(analyzer, results))
        story.append(PageBreak())
        
        # Página 2: Parâmetros e Configurações
        story.extend(self._create_parameters_section(analyzer))
        story.append(PageBreak())
        
        # Página 3: Análise de Performance
        story.extend(self._create_performance_section(results))
        story.append(PageBreak())
        
        # Página 4: Análise Financeira
        story.extend(self._create_financial_section(results))
        story.append(PageBreak())
        
        # Página 5: Comparação de Alavancagem
        story.extend(self._create_leverage_section(analyzer))
        story.append(PageBreak())
        
        # Página 6: Métricas Detalhadas
        story.extend(self._create_metrics_section(results))
        story.append(PageBreak())
        
        # Página 7: Alertas e Recomendações
        story.extend(self._create_alerts_section(analyzer))
        
        # Construir PDF
        doc.build(story)
        return filename
    
    def _create_cover_page(self, analyzer, results: Dict) -> list:
        """Cria página de capa idêntica ao Streamlit"""
        story = []
        
        # Título principal idêntico ao Streamlit
        story.append(Paragraph("Forex Analyzer Pro - Análise Quantitativa", self.styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        # Resumo Executivo - igual ao Streamlit
        story.append(Paragraph("Resumo Executivo", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        # Métricas principais em formato de cards (4 colunas como no Streamlit)
        metrics_data = [
            ['Capital Final', 'Retorno Total', 'Sharpe Ratio', 'Profit Factor'],
            [f"R$ {results['final_capital']:,.2f}", 
             f"{results['total_return']:.2f}%", 
             f"{results['performance_metrics']['sharpe_ratio']:.3f}", 
             f"{results['performance_metrics']['profit_factor']:.2f}"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch, 1.5*inch, 1.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.2, 0.3, 0.5)),  # Azul escuro moderno
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, 1), 14),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.97, 0.97, 0.97)),  # Cinza muito claro
            ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.8, 0.8))  # Cinza claro para bordas
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 30))
        
        # Alertas de Risco - igual ao Streamlit
        story.append(Paragraph("Alertas de Risco", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 15))
        
        alerts = analyzer.get_risk_alerts()
        if alerts:
            for alert in alerts:
                alert_text = f"ALERTA: {alert['message']}"
                story.append(Paragraph(alert_text, self.styles['AlertStyle']))
        else:
            story.append(Paragraph("Todos os parâmetros estão dentro dos limites recomendados", self.styles['Normal']))
        
        return story
    
    def _create_parameters_section(self, analyzer) -> list:
        """Cria seção de parâmetros exatamente como no Streamlit"""
        story = []
        
        story.append(Paragraph("Parâmetros da Simulação", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        # Tabela de parâmetros idêntica ao Streamlit
        params_data = [
            ['Parâmetro', 'Valor'],
            ['Capital Inicial', f"R$ {analyzer.params.capital_inicial:,.2f}"],
            ['Risco por Operação', f"{analyzer.params.porcentagem_risco:.1f}%"],
            ['Alavancagem', f"1:{analyzer.params.alavancagem}"],
            ['Win Rate', f"{analyzer.params.win_rate:.1f}%"],
            ['Risk/Reward Ratio', f"{analyzer.params.rr_ratio:.1f}"],
            ['Spread Médio', f"{analyzer.params.spread_pips:.1f} pips"],
            ['Comissão', f"{analyzer.params.comissao_pct:.3f}%"],
            ['Operações por Mês', f"{analyzer.params.operacoes_mes} trades"]
        ]
        
        params_table = Table(params_data, colWidths=[3*inch, 2.5*inch])
        params_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        
        story.append(params_table)
        
        return story
    
    def _create_performance_section(self, results: Dict) -> list:
        """Cria seção de resumo dos resultados exatamente como no Streamlit"""
        story = []
        
        story.append(Paragraph("Resumo dos Resultados", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        metrics = results['performance_metrics']
        
        # Texto do resumo idêntico ao Streamlit
        summary_text = f"""
        <b>Período de Simulação</b>: {len(results['monthly_results'])} meses<br/>
        <b>Capital Final</b>: R$ {results['final_capital']:,.2f}<br/>
        <b>Retorno Total</b>: {results['total_return']:.2f}%<br/>
        <b>Retorno Mensal Médio</b>: {results['total_return']/len(results['monthly_results']):.2f}%<br/>
        <br/>
        <b>Performance</b>:<br/>
        • Total de Trades: {metrics['total_trades']:,}<br/>
        • Win Rate Realizado: {metrics['win_rate']:.1f}%<br/>
        • Profit Factor: {metrics['profit_factor']:.2f}<br/>
        • Sharpe Ratio: {metrics['sharpe_ratio']:.3f}<br/>
        • Maximum Drawdown: R$ {metrics['max_drawdown']:,.2f}<br/>
        <br/>
        <b>Análise de Custos</b>:<br/>
        • Custos Operacionais Totais: R$ {sum([m['total_costs'] for m in results['monthly_results']]):,.2f}<br/>
        • Impostos Totais: R$ {sum([m['total_taxes'] for m in results['monthly_results']]):,.2f}<br/>
        • Margem Líquida: {(sum([m['net_profit'] for m in results['monthly_results']]) / sum([abs(m['gross_profit']) for m in results['monthly_results']]) * 100):.1f}%<br/>
        """
        
        story.append(Paragraph(summary_text, self.styles['Normal']))
        
        return story
    
    def _create_financial_section(self, results: Dict) -> list:
        """Cria seção de análise financeira exatamente como no Streamlit"""
        story = []
        
        story.append(Paragraph("Análise Financeira", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        monthly_df = pd.DataFrame(results['monthly_results'])
        
        # Análise de Lucros em formato de texto simples como no Streamlit
        total_gross_profit = sum([month['gross_profit'] for month in monthly_df.to_dict('records')])
        total_net_profit = sum([month['net_profit'] for month in monthly_df.to_dict('records')])
        total_costs = sum([month['total_costs'] for month in monthly_df.to_dict('records')])
        total_taxes = sum([month['total_taxes'] for month in monthly_df.to_dict('records')])
        margin = (total_net_profit / total_gross_profit * 100) if total_gross_profit > 0 else 0
        
        financial_text = f"""
        <b>Análise de Lucros</b><br/>
        • Lucro Bruto Total: R$ {total_gross_profit:,.2f}<br/>
        • Lucro Líquido Total: R$ {total_net_profit:,.2f}<br/>
        • Total de Custos: R$ {total_costs:,.2f}<br/>
        • Total de Impostos: R$ {total_taxes:,.2f}<br/>
        • Margem Líquida: {margin:.1f}%<br/>
        """
        
        story.append(Paragraph(financial_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Informações adicionais em formato simples
        additional_info = f"""
        <b>Resumo do Período</b><br/>
        • Período Total: {len(monthly_df)} meses<br/>
        • Média Mensal de Lucro: R$ {total_net_profit/len(monthly_df):,.2f}<br/>
        • Média Mensal de Custos: R$ {total_costs/len(monthly_df):,.2f}<br/>
        """
        
        story.append(Paragraph(additional_info, self.styles['Normal']))
        
        return story
    
    def _create_leverage_section(self, analyzer) -> list:
        """Cria seção de comparação de alavancagem em formato simples"""
        story = []
        
        story.append(Paragraph("Comparação de Alavancagens", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        # Comparar diferentes alavancagens
        leverage_scenarios = analyzer.compare_leverage_scenarios(
            leverage_list=[30, 50, 100, 200, 500],
            months=48
        )
        
        # Resumo em formato simples
        leverage_summary = "<b>Análise de Diferentes Alavancagens:</b><br/><br/>"
        
        for scenario_name, data in leverage_scenarios.items():
            leverage_summary += f"• <b>Alavancagem 1:{data['leverage']}</b>: Retorno {data['total_return']:.1f}%, Capital Final R$ {data['final_capital']:,.0f}<br/>"
        
        story.append(Paragraph(leverage_summary, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_metrics_section(self, results: Dict) -> list:
        """Cria seção de métricas em formato simples"""
        story = []
        
        story.append(Paragraph("Métricas de Performance", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        # Métricas principais em formato simples
        performance_metrics = results['performance_metrics']
        
        metrics_text = f"""
        <b>Métricas Principais:</b><br/>
        • Sharpe Ratio: {performance_metrics['sharpe_ratio']:.3f}<br/>
        • Profit Factor: {performance_metrics['profit_factor']:.2f}<br/>
        • Win Rate: {performance_metrics.get('win_rate', 0):.1f}%<br/>
        • Total de Trades: {performance_metrics.get('total_trades', 0)}<br/>
        • Max Drawdown: R$ {performance_metrics.get('max_drawdown', 0):,.2f}<br/>
        """
        
        story.append(Paragraph(metrics_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_alerts_section(self, analyzer) -> list:
        """Cria seção de alertas em formato simples"""
        story = []
        
        story.append(Paragraph("Alertas de Risco", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        # Obter alertas do sistema
        alerts = analyzer.get_risk_alerts()
        
        if alerts:
            alerts_text = "<b>Alertas Ativos:</b><br/><br/>"
            for alert in alerts:
                alerts_text += f"• {alert['message']}<br/>"
        else:
            alerts_text = "<b>Status:</b> Todos os parâmetros estão dentro dos limites recomendados."
        
        story.append(Paragraph(alerts_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        return story
    
    # Métodos auxiliares para classificação
    def _classify_win_rate(self, win_rate: float) -> str:
        if win_rate >= 60: return "Excelente"
        elif win_rate >= 50: return "Bom"
        elif win_rate >= 40: return "Regular"
        else: return "Ruim"
    
    def _classify_profit_factor(self, pf: float) -> str:
        if pf >= 2: return "Excelente"
        elif pf >= 1.5: return "Bom"
        elif pf >= 1.2: return "Regular"
        else: return "Ruim"
    
    def _classify_sharpe_ratio(self, sharpe: float) -> str:
        if sharpe >= 2: return "Excelente"
        elif sharpe >= 1: return "Bom"
        elif sharpe >= 0.5: return "Regular"
        else: return "Ruim"
    
    def _classify_calmar_ratio(self, calmar: float) -> str:
        if calmar >= 1: return "Excelente"
        elif calmar >= 0.5: return "Bom"
        elif calmar >= 0.2: return "Regular"
        else: return "Ruim"
    
    def _classify_drawdown(self, dd: float) -> str:
        if dd <= 5: return "Excelente"
        elif dd <= 10: return "Bom"
        elif dd <= 20: return "Regular"
        else: return "Ruim"
    
    def _classify_roi(self, roi: float) -> str:
        if roi >= 30: return "Excelente"
        elif roi >= 20: return "Bom"
        elif roi >= 10: return "Regular"
        else: return "Ruim"
    
    def _classify_roi_annual(self, total_roi: float) -> str:
        # Assumindo que total_roi é para o período completo
        annual_roi = total_roi  # Simplificação
        return self._classify_roi(annual_roi)
    
    def _classify_leverage_scenario(self, data: Dict) -> str:
        sharpe = data.get('sharpe_ratio', 0)
        drawdown = data.get('max_drawdown', 100)
        
        if sharpe > 1.5 and drawdown < 10:
            return "Ótimo"
        elif sharpe > 1 and drawdown < 15:
            return "Bom"
        elif sharpe > 0.5 and drawdown < 25:
            return "Regular"
        else:
            return "Arriscado"
    
    # Métodos para interpretações detalhadas
    def _get_sharpe_interpretation(self, sharpe: float) -> str:
        if sharpe >= 2:
            return "Excelente relação risco-retorno. A estratégia gera retornos consistentes com volatilidade controlada."
        elif sharpe >= 1:
            return "Boa relação risco-retorno. A estratégia é eficiente na geração de retornos ajustados ao risco."
        elif sharpe >= 0.5:
            return "Relação risco-retorno moderada. Há espaço para melhorias na consistência dos retornos."
        else:
            return "Relação risco-retorno baixa. A estratégia pode não estar compensando adequadamente o risco assumido."
    
    def _get_profit_factor_interpretation(self, pf: float) -> str:
        if pf >= 2:
            return "Excelente lucratividade. Os ganhos superam significativamente as perdas."
        elif pf >= 1.5:
            return "Boa lucratividade. A estratégia gera lucros consistentes."
        elif pf >= 1.2:
            return "Lucratividade moderada. A margem de lucro é pequena mas positiva."
        else:
            return "Lucratividade baixa ou negativa. A estratégia precisa de ajustes significativos."
    
    def _get_calmar_interpretation(self, calmar: float) -> str:
        if calmar >= 1:
            return "Excelente eficiência de retorno por unidade de drawdown. Estratégia muito robusta."
        elif calmar >= 0.5:
            return "Boa eficiência de retorno. A estratégia gerencia bem os períodos de perda."
        elif calmar >= 0.2:
            return "Eficiência moderada. Há espaço para melhorar a gestão de drawdowns."
        else:
            return "Baixa eficiência. Os drawdowns são muito altos em relação aos retornos gerados."
    
    def _get_drawdown_interpretation(self, dd: float) -> str:
        if dd <= 5:
            return "Drawdown excelente. A estratégia mantém perdas muito controladas."
        elif dd <= 10:
            return "Drawdown bom. Perdas dentro de limites aceitáveis para a maioria dos traders."
        elif dd <= 20:
            return "Drawdown moderado. Requer disciplina emocional para suportar os períodos de perda."
        else:
            return "Drawdown alto. Pode ser psicologicamente difícil de suportar e indica alto risco."
    
    def _get_winrate_interpretation(self, winrate: float) -> str:
        if winrate >= 70:
            return "Win rate excelente. Alta consistência nas operações vencedoras."
        elif winrate >= 60:
            return "Win rate bom. Boa proporção de trades vencedores."
        elif winrate >= 50:
            return "Win rate moderado. Equilibrio entre ganhos e perdas."
        else:
            return "Win rate baixo. Necessário melhorar a precisão das entradas."
    
    def _get_expectancy_interpretation(self, expectancy: float) -> str:
        if expectancy >= 100:
            return "Expectativa excelente. Cada trade tem alto valor esperado positivo."
        elif expectancy >= 50:
            return "Expectativa boa. Valor esperado positivo consistente por trade."
        elif expectancy > 0:
            return "Expectativa positiva. Estratégia matematicamente lucrativa."
        else:
            return "Expectativa negativa. Estratégia não é matematicamente lucrativa."
    
    def _get_trades_interpretation(self, total_trades: int) -> str:
        if total_trades >= 100:
            return "Amostra estatisticamente significativa. Resultados confiáveis."
        elif total_trades >= 50:
            return "Amostra boa. Resultados representativos da estratégia."
        elif total_trades >= 20:
            return "Amostra moderada. Resultados indicativos mas limitados."
        else:
            return "Amostra pequena. Resultados podem não ser representativos."
    
    def _get_consecutive_losses_interpretation(self, losses: int) -> str:
        if losses <= 3:
            return "Sequência de perdas baixa. Boa consistência da estratégia."
        elif losses <= 5:
            return "Sequência de perdas moderada. Dentro do esperado."
        elif losses <= 8:
            return "Sequência de perdas alta. Requer disciplina emocional."
        else:
            return "Sequência de perdas muito alta. Pode indicar problemas na estratégia."