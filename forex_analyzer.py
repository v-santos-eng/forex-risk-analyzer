import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

@dataclass
class TradingParameters:
    """Parâmetros configuráveis para análise de trading forex"""
    capital_inicial: float = 10000.0
    porcentagem_risco: float = 2.0  # % do capital por operação
    alavancagem: int = 30  # 1:30
    win_rate: float = 65.0  # % de operações vencedoras
    rr_ratio: float = 1.5  # Risk/Reward ratio
    spread_pips: float = 2.0  # Spread médio em pips
    comissao_pct: float = 0.05  # Comissão por operação (%)
    swap_diario: float = 0.02  # Swap diário (%)
    ir_rate: float = 15.0  # Imposto de Renda (%)
    iof_rate: float = 0.38  # IOF (%)
    pip_value: float = 10.0  # Valor do pip em USD para lote padrão
    operacoes_mes: int = 20  # Número de operações por mês
    
class ForexAnalyzer:
    """Analisador quantitativo robusto para trading forex"""
    
    # Níveis de alavancagem disponíveis
    LEVERAGE_LEVELS = [1, 5, 25, 30, 50, 100, 200, 300, 400, 500, 1000]
    
    def __init__(self, params: TradingParameters):
        self.params = params
        self.results = {}
        self.historical_data = []
        
    def validate_parameters(self) -> bool:
        """Valida os parâmetros de entrada"""
        validations = [
            (self.params.capital_inicial > 0, "Capital inicial deve ser positivo"),
            (0 < self.params.porcentagem_risco <= 10, "Risco por operação deve estar entre 0-10%"),
            (self.params.alavancagem in self.LEVERAGE_LEVELS, f"Alavancagem deve ser uma das opções: {self.LEVERAGE_LEVELS}"),
            (0 < self.params.win_rate <= 100, "Win rate deve estar entre 0-100%"),
            (self.params.rr_ratio > 0, "Risk/Reward ratio deve ser positivo"),
            (self.params.spread_pips >= 0, "Spread deve ser não-negativo"),
            (self.params.comissao_pct >= 0, "Comissão deve ser não-negativa"),
            (self.params.operacoes_mes > 0, "Número de operações deve ser positivo")
        ]
        
        for condition, message in validations:
            if not condition:
                raise ValueError(f"Parâmetro inválido: {message}")
        return True
    
    def calculate_position_size(self, stop_loss_pips: float) -> Dict[str, float]:
        """Calcula o tamanho da posição baseado no risco definido"""
        risk_amount = self.params.capital_inicial * (self.params.porcentagem_risco / 100)
        pip_risk = stop_loss_pips * self.params.pip_value
        
        if pip_risk <= 0:
            raise ValueError("Stop loss deve ser positivo")
        
        # Tamanho da posição em lotes
        position_size_lots = risk_amount / pip_risk
        
        # Margem necessária
        margin_required = (position_size_lots * 100000) / self.params.alavancagem
        
        # Margem livre após a operação
        free_margin = self.params.capital_inicial - margin_required
        
        return {
            'position_size_lots': position_size_lots,
            'risk_amount': risk_amount,
            'margin_required': margin_required,
            'free_margin': free_margin,
            'margin_level': (self.params.capital_inicial / margin_required) * 100 if margin_required > 0 else float('inf')
        }
    
    def calculate_trade_costs(self, position_size_lots: float) -> Dict[str, float]:
        """Calcula todos os custos de uma operação"""
        # Custo do spread
        spread_cost = position_size_lots * self.params.spread_pips * self.params.pip_value
        
        # Comissão
        commission_cost = position_size_lots * 100000 * (self.params.comissao_pct / 100)
        
        # Swap diário (assumindo 1 dia)
        swap_cost = position_size_lots * 100000 * (self.params.swap_diario / 100)
        
        total_cost = spread_cost + commission_cost + swap_cost
        
        return {
            'spread_cost': spread_cost,
            'commission_cost': commission_cost,
            'swap_cost': swap_cost,
            'total_cost': total_cost
        }
    
    def calculate_profit_loss(self, position_size_lots: float, pips_result: float) -> Dict[str, float]:
        """Calcula lucro/prejuízo bruto e líquido de uma operação"""
        # Lucro/prejuízo bruto
        gross_pl = position_size_lots * pips_result * self.params.pip_value
        
        # Custos da operação
        costs = self.calculate_trade_costs(position_size_lots)
        
        # Lucro/prejuízo após custos operacionais
        net_pl_before_taxes = gross_pl - costs['total_cost']
        
        # Cálculo de impostos (apenas sobre lucros)
        iof_tax = 0
        ir_tax = 0
        
        if net_pl_before_taxes > 0:
            iof_tax = net_pl_before_taxes * (self.params.iof_rate / 100)
            ir_base = max(0, net_pl_before_taxes - iof_tax)
            ir_tax = ir_base * (self.params.ir_rate / 100)
        
        # Lucro/prejuízo líquido final
        net_pl = net_pl_before_taxes - iof_tax - ir_tax
        
        return {
            'gross_pl': gross_pl,
            'net_pl_before_taxes': net_pl_before_taxes,
            'iof_tax': iof_tax,
            'ir_tax': ir_tax,
            'net_pl': net_pl,
            'total_costs': costs['total_cost'],
            'total_taxes': iof_tax + ir_tax
        }
    
    def calculate_performance_metrics(self, trades_data: List[Dict]) -> Dict[str, float]:
        """Calcula métricas de performance baseadas em histórico de trades"""
        if not trades_data:
            return {}
        
        # Extrair dados dos trades
        returns = [trade['net_pl'] for trade in trades_data]
        gross_returns = [trade['gross_pl'] for trade in trades_data]
        
        # Métricas básicas
        total_trades = len(returns)
        winning_trades = len([r for r in returns if r > 0])
        losing_trades = len([r for r in returns if r < 0])
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # Lucros e prejuízos
        total_profit = sum([r for r in returns if r > 0])
        total_loss = abs(sum([r for r in returns if r < 0]))
        net_profit = sum(returns)
        
        # Profit Factor
        profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
        
        # Expectativa Matemática
        avg_win = total_profit / winning_trades if winning_trades > 0 else 0
        avg_loss = total_loss / losing_trades if losing_trades > 0 else 0
        
        mathematical_expectancy = (win_rate/100 * avg_win) - ((100-win_rate)/100 * avg_loss)
        
        # Sharpe Ratio (assumindo taxa livre de risco = 0)
        returns_array = np.array(returns)
        sharpe_ratio = np.mean(returns_array) / np.std(returns_array) if np.std(returns_array) > 0 else 0
        
        # Maximum Drawdown
        cumulative_returns = np.cumsum(returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = cumulative_returns - running_max
        max_drawdown = abs(np.min(drawdown)) if len(drawdown) > 0 else 0
        
        # ROI
        roi = (net_profit / self.params.capital_inicial) * 100
        
        # Calmar Ratio
        calmar_ratio = roi / max_drawdown if max_drawdown > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'net_profit': net_profit,
            'profit_factor': profit_factor,
            'mathematical_expectancy': mathematical_expectancy,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'roi': roi,
            'calmar_ratio': calmar_ratio,
            'avg_win': avg_win,
            'avg_loss': avg_loss
        }
    
    def simulate_trading_scenario(self, months: int = 48, stop_loss_pips: float = 20) -> Dict:
        """Simula um cenário de trading por período determinado"""
        self.validate_parameters()
        
        # Calcular tamanho da posição
        position_info = self.calculate_position_size(stop_loss_pips)
        
        # Simular trades mensais
        monthly_results = []
        trades_data = []
        current_capital = self.params.capital_inicial
        
        for month in range(months):
            month_trades = []
            month_profit = 0
            
            for trade in range(self.params.operacoes_mes):
                # Simular resultado do trade (win/loss baseado no win_rate)
                is_win = np.random.random() < (self.params.win_rate / 100)
                
                if is_win:
                    pips_result = stop_loss_pips * self.params.rr_ratio  # Take profit
                else:
                    pips_result = -stop_loss_pips  # Stop loss
                
                # Calcular P&L do trade
                trade_result = self.calculate_profit_loss(position_info['position_size_lots'], pips_result)
                trade_result['month'] = month + 1
                trade_result['trade_number'] = trade + 1
                trade_result['is_win'] = is_win
                trade_result['pips_result'] = pips_result
                
                month_trades.append(trade_result)
                trades_data.append(trade_result)
                month_profit += trade_result['net_pl']
            
            # Atualizar capital (simplificado - não considera compound)
            current_capital += month_profit
            
            monthly_results.append({
                'month': month + 1,
                'trades': len(month_trades),
                'gross_profit': sum([t['gross_pl'] for t in month_trades if t['gross_pl'] > 0]),
                'gross_loss': sum([t['gross_pl'] for t in month_trades if t['gross_pl'] < 0]),
                'net_profit': month_profit,
                'capital_end': current_capital,
                'total_costs': sum([t['total_costs'] for t in month_trades]),
                'total_taxes': sum([t['total_taxes'] for t in month_trades])
            })
        
        # Calcular métricas de performance
        performance_metrics = self.calculate_performance_metrics(trades_data)
        
        return {
            'position_info': position_info,
            'monthly_results': monthly_results,
            'trades_data': trades_data,
            'performance_metrics': performance_metrics,
            'final_capital': current_capital,
            'total_return': ((current_capital - self.params.capital_inicial) / self.params.capital_inicial) * 100
        }
    
    def compare_leverage_scenarios(self, leverage_list: List[int] = None, months: int = 48) -> Dict:
        """Compara diferentes cenários de alavancagem"""
        if leverage_list is None:
            leverage_list = [30, 50, 100, 200, 500]
        
        scenarios = {}
        original_leverage = self.params.alavancagem
        
        for leverage in leverage_list:
            if leverage not in self.LEVERAGE_LEVELS:
                continue
                
            # Atualizar alavancagem temporariamente
            self.params.alavancagem = leverage
            
            # Simular cenário
            scenario_result = self.simulate_trading_scenario(months)
            scenarios[f'Leverage_1_{leverage}'] = {
                'leverage': leverage,
                'final_capital': scenario_result['final_capital'],
                'total_return': scenario_result['total_return'],
                'max_drawdown': scenario_result['performance_metrics']['max_drawdown'],
                'sharpe_ratio': scenario_result['performance_metrics']['sharpe_ratio'],
                'profit_factor': scenario_result['performance_metrics']['profit_factor'],
                'margin_required': scenario_result['position_info']['margin_required'],
                'position_size': scenario_result['position_info']['position_size_lots']
            }
        
        # Restaurar alavancagem original
        self.params.alavancagem = original_leverage
        
        return scenarios
    
    def get_risk_alerts(self) -> List[Dict[str, str]]:
        """Gera alertas de risco baseados nos parâmetros atuais"""
        alerts = []
        
        # Alerta de risco por operação
        if self.params.porcentagem_risco > 5:
            alerts.append({
                'type': 'HIGH_RISK',
                'message': f'Risco por operação muito alto: {self.params.porcentagem_risco}% (recomendado: ≤5%)'
            })
        
        # Alerta de alavancagem
        if self.params.alavancagem > 100:
            alerts.append({
                'type': 'HIGH_LEVERAGE',
                'message': f'Alavancagem muito alta: 1:{self.params.alavancagem} (recomendado: ≤1:100 para iniciantes)'
            })
        
        # Alerta de win rate
        if self.params.win_rate < 50:
            alerts.append({
                'type': 'LOW_WIN_RATE',
                'message': f'Win rate baixo: {self.params.win_rate}% (verifique estratégia)'
            })
        
        # Alerta de R:R ratio
        if self.params.rr_ratio < 1:
            alerts.append({
                'type': 'POOR_RR_RATIO',
                'message': f'Risk/Reward ratio desfavorável: {self.params.rr_ratio} (recomendado: ≥1.5)'
            })
        
        return alerts

# Exemplo de uso
if __name__ == "__main__":
    # Configurar parâmetros
    params = TradingParameters(
        capital_inicial=10000,
        porcentagem_risco=2.0,
        alavancagem=30,
        win_rate=65,
        rr_ratio=1.5
    )
    
    # Criar analisador
    analyzer = ForexAnalyzer(params)
    
    # Simular cenário
    results = analyzer.simulate_trading_scenario(months=48, stop_loss_pips=20)
    
    print("=== RESULTADOS DA SIMULAÇÃO ===")
    print(f"Capital Final: R$ {results['final_capital']:,.2f}")
    print(f"Retorno Total: {results['total_return']:.2f}%")
    print(f"Sharpe Ratio: {results['performance_metrics']['sharpe_ratio']:.3f}")
    print(f"Profit Factor: {results['performance_metrics']['profit_factor']:.2f}")
    print(f"Win Rate: {results['performance_metrics']['win_rate']:.1f}%")
    
    # Verificar alertas
    alerts = analyzer.get_risk_alerts()
    if alerts:
        print("\n=== ALERTAS DE RISCO ===")
        for alert in alerts:
            print(f"ALERTA: {alert['message']}")