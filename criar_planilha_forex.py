import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.chart import LineChart, Reference, BarChart, PieChart
from openpyxl.worksheet.datavalidation import DataValidation

def criar_planilha_forex():
    # Criar workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Análise Forex"
    
    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    input_fill = PatternFill(start_color="E7F3FF", end_color="E7F3FF", fill_type="solid")
    calc_fill = PatternFill(start_color="F0F8E7", end_color="F0F8E7", fill_type="solid")
    
    # SEÇÃO 1: PARÂMETROS DE ENTRADA
    ws['A1'] = "ANÁLISE DE RISCO/RETORNO - FOREX TRADING"
    ws['A1'].font = Font(bold=True, size=16)
    ws.merge_cells('A1:E1')
    
    ws['A3'] = "PARÂMETROS DE ENTRADA"
    ws['A3'].font = header_font
    ws['A3'].fill = header_fill
    ws.merge_cells('A3:B3')
    
    # Parâmetros configuráveis - valores realistas para forex Brasil
    parametros = [
        ("Capital Inicial (R$)", 10000),
        ("Alavancagem", 30),  # Mais conservador para Brasil
        ("Risco por Operação (%)", 1.5),  # Mais conservador
        ("Objetivo Retorno Mensal (%)", 3),  # Meta realista
        ("Taxa de Acerto (%)", 55),  # Taxa realista
        ("Spread Médio (pips)", 1.8),  # EUR/USD típico
        ("Comissão por Lote (R$)", 12),  # Corretoras brasileiras
        ("Taxa Swap Diária (%)", 0.02),  # Custo overnight
        ("IR sobre Ganhos (%)", 15),  # Imposto de Renda
        ("IOF (%)", 0.38)  # IOF sobre operações
    ]
    
    for i, (param, valor) in enumerate(parametros, 4):
        ws[f'A{i}'] = param
        ws[f'B{i}'] = valor
        ws[f'B{i}'].fill = input_fill
    
    # Dropdown para alavancagem - limitado para Brasil
    alavancagens = "1,5,10,20,30,50,100"
    dv = DataValidation(type="list", formula1=f'"{alavancagens}"')
    dv.add(ws['B5'])
    ws.add_data_validation(dv)
    
    # SEÇÃO 2: CÁLCULOS PRINCIPAIS
    ws['A12'] = "CÁLCULOS PRINCIPAIS"
    ws['A12'].font = header_font
    ws['A12'].fill = header_fill
    ws.merge_cells('A12:C12')
    
    calculos = [
        ("Capital Alavancado (R$)", "=B4*B5"),
        ("Risco por Operação (R$)", "=B4*B6/100"),
        ("Custo Spread por Op (R$)", "=B8*B10*0.1"),  # Spread em R$
        ("Custo Swap Diário (R$)", "=B4*B9/100"),  # Custo overnight
        ("Retorno Bruto/Op (R$)", "=B14*((B7/100*B5)+1)"),  # Retorno antes custos
        ("Retorno Líquido/Op (R$)", "=B17-B15-B16"),  # Após custos
        ("Tamanho Ideal Posição", "=B14/0.0001"),
        ("Stop Loss Recomendado (pips)", "=B14*10000/B19"),
        ("Take Profit (pips)", "=B20*1.5"),  # R/R mais conservador
        ("Risco/Retorno Ratio", "=B20/B21")
    ]
    
    for i, (desc, formula) in enumerate(calculos, 13):
        ws[f'A{i}'] = desc
        ws[f'B{i}'] = formula
        ws[f'B{i}'].fill = calc_fill
    
    # SEÇÃO 3: ANÁLISE DE CENÁRIOS
    ws['A21'] = "ANÁLISE DE CENÁRIOS"
    ws['A21'].font = header_font
    ws['A21'].fill = header_fill
    ws.merge_cells('A21:D21')
    
    ws['A22'] = "Cenário"
    ws['B22'] = "Retorno Mensal (%)"
    ws['C22'] = "Capital Final (R$)"
    ws['D22'] = "Drawdown Máximo (%)"
    
    for cell in ['A22', 'B22', 'C22', 'D22']:
        ws[cell].font = header_font
        ws[cell].fill = header_fill
    
    cenarios = [
        ("Otimista", "=B7*1.5", "=B4*(1+B23/100)^12", "=B6*0.5"),
        ("Realista", "=B7", "=B4*(1+B24/100)^12", "=B6"),
        ("Pessimista", "=B7*0.3", "=B4*(1+B25/100)^12", "=B6*2")
    ]
    
    for i, (cenario, ret, cap, dd) in enumerate(cenarios, 23):
        ws[f'A{i}'] = cenario
        ws[f'B{i}'] = ret
        ws[f'C{i}'] = cap
        ws[f'D{i}'] = dd
    
    # SEÇÃO 4: LUCRO BRUTO E LÍQUIDO (BRASIL)
    ws['A27'] = "LUCRO BRUTO E LÍQUIDO - BRASIL"
    ws['A27'].font = header_font
    ws['A27'].fill = header_fill
    ws.merge_cells('A27:C27')
    
    lucro_brasil = [
        ("Lucro Bruto Mensal (R$)", "=B17*B34*(B7/100)"),  # Baseado em ops/mês
        ("Custo Total Operações (R$)", "=(B15+B16+B10)*B34"),  # Spread+Swap+Comissão
        ("IOF sobre Operações (R$)", "=B28*B11/100"),  # 0.38% IOF
        ("Base Cálculo IR (R$)", "=MAX(0,B28-B29-B30)"),  # Lucro tributável
        ("IR a Pagar (R$)", "=B31*B9/100"),  # 15% IR
        ("Lucro Líquido Mensal (R$)", "=B28-B29-B30-B32"),  # Lucro final
        ("Margem Líquida (%)", "=B33/B28*100"),  # % líquida
        ("Operações por Mês", 20)  # Parâmetro operacional
    ]
    
    for i, (desc, valor) in enumerate(lucro_brasil, 28):
        ws[f'A{i}'] = desc
        ws[f'B{i}'] = valor
        if isinstance(valor, str):
            ws[f'B{i}'].fill = calc_fill
        else:
            ws[f'B{i}'].fill = input_fill
    
    # SEÇÃO 5: GESTÃO DE CAPITAL
    ws['A37'] = "GESTÃO DE CAPITAL"
    ws['A37'].font = header_font
    ws['A37'].fill = header_fill
    ws.merge_cells('A37:C37')
    
    gestao = [
        ("Capital por Operação (R$)", "=B4/B35"),
        ("Risco Total Mensal (%)", "=B6*B35"),
        ("Break-even (operações)", "=1/(B7/100-1)"),
        ("ROI Líquido Mensal (%)", "=B33/B4*100")
    ]
    
    for i, (desc, valor) in enumerate(gestao, 38):
        ws[f'A{i}'] = desc
        ws[f'B{i}'] = valor
        if isinstance(valor, str):
            ws[f'B{i}'].fill = calc_fill
        else:
            ws[f'B{i}'].fill = input_fill
    
    # SEÇÃO 6: SIMULAÇÃO DE ESTRATÉGIAS
    ws['A43'] = "SIMULAÇÃO DE ESTRATÉGIAS"
    ws['A43'].font = header_font
    ws['A43'].fill = header_fill
    ws.merge_cells('A43:D43')
    
    ws['A44'] = "Estratégia"
    ws['B44'] = "Alavancagem"
    ws['C44'] = "Risco/Op (%)"
    ws['D44'] = "Lucro Líq. Esperado (%)"
    
    for cell in ['A44', 'B44', 'C44', 'D44']:
        ws[cell].font = header_font
        ws[cell].fill = header_fill
    
    estrategias = [
        ("Conservadora", 10, 1, "=C45*B45*(B7/100)*0.85"),  # 85% após custos
        ("Moderada", 30, 1.5, "=C46*B46*(B7/100)*0.80"),  # 80% após custos
        ("Agressiva", 50, 2.5, "=C47*B47*(B7/100)*0.75"),  # 75% após custos
        ("Especulativa", 100, 4, "=C48*B48*(B7/100)*0.70")  # 70% após custos
    ]
    
    for i, (est, alav, risco, ret) in enumerate(estrategias, 45):
        ws[f'A{i}'] = est
        ws[f'B{i}'] = alav
        ws[f'C{i}'] = risco
        ws[f'D{i}'] = ret
    
    # SEÇÃO 7: MÉTRICAS DE PERFORMANCE
    ws['A50'] = "MÉTRICAS DE PERFORMANCE"
    ws['A50'].font = header_font
    ws['A50'].fill = header_fill
    ws.merge_cells('A50:C50')
    
    metricas = [
        ("Sharpe Ratio", "=(B41*12-5)/(SQRT(12)*B41*0.15)"),  # (Ret anual - RF) / Vol anual
        ("Profit Factor", "=(B7/100*B18)/((1-B7/100)*B14)"),  # Ganho médio / Perda média
        ("Win Rate (%)", "=B7"),  # Taxa de acerto
        ("Expectativa Matemática (R$)", "=B7/100*B18-(1-B7/100)*B14"),  # E = p*W - (1-p)*L
        ("ROI Líquido Anual (%)", "=B41*12"),  # ROI mensal * 12
        ("Drawdown Máximo (%)", "=B6*3"),  # Estimativa conservadora
        ("Calmar Ratio", "=B54/B55")  # ROI anual / Max Drawdown
    ]
    
    for i, (desc, formula) in enumerate(metricas, 51):
        ws[f'A{i}'] = desc
        ws[f'B{i}'] = formula
        ws[f'B{i}'].fill = calc_fill
    
    # SEÇÃO 8: PROJEÇÃO MENSAL
    ws['E3'] = "PROJEÇÃO MENSAL"
    ws['E3'].font = header_font
    ws['E3'].fill = header_fill
    ws.merge_cells('E3:I3')
    
    ws['E4'] = "Mês"
    ws['F4'] = "Capital Inicial"
    ws['G4'] = "Lucro Bruto"
    ws['H4'] = "Lucro Líquido"
    ws['I4'] = "Capital Final"
    
    for cell in ['E4', 'F4', 'G4', 'H4', 'I4']:
        ws[cell].font = header_font
        ws[cell].fill = header_fill
    
    # Projeção para 12 meses
    for mes in range(1, 13):
        row = mes + 4
        ws[f'E{row}'] = mes
        if mes == 1:
            ws[f'F{row}'] = "=B4"
        else:
            ws[f'F{row}'] = f"=I{row-1}"
        # Lucro bruto mensal
        ws[f'G{row}'] = "=B28"
        # Lucro líquido mensal (após impostos)
        ws[f'H{row}'] = "=B33"
        # Capital final acumulado
        ws[f'I{row}'] = f"=F{row}+H{row}"
    
    # Formatação de números
    for row in range(5, 17):
        for col in ['F', 'G', 'H', 'I']:
            ws[f'{col}{row}'].number_format = 'R$ #,##0.00'
    
    # SEÇÃO 9: ALERTAS E VALIDAÇÕES BRASIL
    ws['E18'] = "ALERTAS DE RISCO - BRASIL"
    ws['E18'].font = header_font
    ws['E18'].fill = header_fill
    ws.merge_cells('E18:I18')
    
    alertas = [
        ("Risco Total Mensal", '=IF(B39>15,"ALTO RISCO","CONTROLADO")'),
        ("Alavancagem", '=IF(B5>50,"MUITO ALTA","ADEQUADA")'),
        ("Margem Líquida", '=IF(B34<50,"BAIXA MARGEM","BOA MARGEM")'),
        ("Carga Tributária", '=IF((B30+B32)/B28>0.25,"ALTA CARGA","CONTROLADA")'),
        ("Expectativa Matemática", '=IF(B53<0,"NEGATIVA","POSITIVA")')
    ]
    
    for i, (desc, formula) in enumerate(alertas, 19):
        ws[f'E{i}'] = desc
        ws[f'F{i}'] = formula
    
    # Ajustar largura das colunas
    column_widths = {'A': 25, 'B': 15, 'C': 15, 'D': 15, 'E': 15, 'F': 15, 'G': 12, 'H': 15, 'I': 15}
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # GRÁFICO 1: Projeção de Capital (Linha)
    chart1 = LineChart()
    chart1.title = "Evolução do Capital - Bruto vs Líquido"
    chart1.style = 10
    chart1.x_axis.title = 'Mês'
    chart1.y_axis.title = 'Capital (R$)'
    chart1.width = 15
    chart1.height = 10
    
    # Dados para capital inicial, bruto e líquido
    data1 = Reference(ws, min_col=6, min_row=4, max_row=16, max_col=9)  # F:I
    cats1 = Reference(ws, min_col=5, min_row=5, max_row=16)  # Meses
    chart1.add_data(data1, titles_from_data=True)
    chart1.set_categories(cats1)
    
    ws.add_chart(chart1, "K3")
    
    # GRÁFICO 2: Distribuição de Custos (Pizza)
    chart2 = PieChart()
    chart2.title = "Distribuição de Custos Mensais"
    chart2.width = 12
    chart2.height = 10
    
    # Dados dos custos
    ws['K25'] = "Custos Mensais"
    ws['K25'].font = header_font
    ws['K26'] = "Spread"
    ws['L26'] = "=B15*B35"  # Custo spread mensal
    ws['K27'] = "Swap"
    ws['L27'] = "=B16*B35"  # Custo swap mensal
    ws['K28'] = "Comissão"
    ws['L28'] = "=B10*B35"  # Comissão mensal
    ws['K29'] = "IOF"
    ws['L29'] = "=B30"  # IOF mensal
    ws['K30'] = "IR"
    ws['L30'] = "=B32"  # IR mensal
    
    data2 = Reference(ws, min_col=12, min_row=26, max_row=30)  # Valores
    labels2 = Reference(ws, min_col=11, min_row=26, max_row=30)  # Labels
    chart2.add_data(data2)
    chart2.set_categories(labels2)
    
    ws.add_chart(chart2, "K35")
    
    # GRÁFICO 3: Comparação Lucro Bruto vs Líquido (Barras)
    chart3 = BarChart()
    chart3.title = "Lucro Bruto vs Líquido - 12 Meses"
    chart3.style = 10
    chart3.x_axis.title = 'Mês'
    chart3.y_axis.title = 'Lucro (R$)'
    chart3.width = 15
    chart3.height = 10
    
    data3 = Reference(ws, min_col=7, min_row=4, max_row=16, max_col=8)  # G:H (Bruto e Líquido)
    cats3 = Reference(ws, min_col=5, min_row=5, max_row=16)  # Meses
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    
    ws.add_chart(chart3, "K50")
    
    # Salvar arquivo
    wb.save('analise_forex_completa.xlsx')
    print("Planilha criada com sucesso!")
    
    return "Planilha Excel criada com todas as funcionalidades solicitadas."

if __name__ == "__main__":
    resultado = criar_planilha_forex()
    print(resultado)