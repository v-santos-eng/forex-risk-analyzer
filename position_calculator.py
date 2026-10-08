import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    """Níveis de risco predefinidos"""
    CONSERVADOR = 1.0
    MODERADO = 2.0
    AGRESSIVO = 3.0
    ESPECULATIVO = 5.0

class CurrencyPair(Enum):
    """Principais pares de moedas forex"""
    EURUSD = "EUR/USD"
    GBPUSD = "GBP/USD"
    USDJPY = "USD/JPY"
    USDCHF = "USD/CHF"
    AUDUSD = "AUD/USD"
    USDCAD = "USD/CAD"
    NZDUSD = "NZD/USD"
    EURJPY = "EUR/JPY"
    GBPJPY = "GBP/JPY"
    EURGBP = "EUR/GBP"

@dataclass
class MarketConditions:
    """Condições de mercado para cálculos mais precisos"""
    volatility: float = 1.0  # Multiplicador de volatilidade
    spread_multiplier: float = 1.0  # Multiplicador do spread
    liquidity_factor: float = 1.0  # Fator de liquidez
    session_type: str = "london"  # london, new_york, tokyo, sydney

class AdvancedPositionCalculator:
    """Calculadora avançada de posições com múltiplas estratégias"""
    
    # Valores de pip por par de moedas (para conta em USD)
    PIP_VALUES = {
        CurrencyPair.EURUSD: 10.0,
        CurrencyPair.GBPUSD: 10.0,
        CurrencyPair.USDJPY: 9.09,  # Aproximado para USD/JPY
        CurrencyPair.USDCHF: 10.0,
        CurrencyPair.AUDUSD: 10.0,
        CurrencyPair.USDCAD: 7.69,  # Aproximado
        CurrencyPair.NZDUSD: 10.0,
        CurrencyPair.EURJPY: 9.09,
        CurrencyPair.GBPJPY: 9.09,
        CurrencyPair.EURGBP: 12.82   # Aproximado
    }
    
    # Spreads típicos por par (em pips)
    TYPICAL_SPREADS = {
        CurrencyPair.EURUSD: 1.5,
        CurrencyPair.GBPUSD: 2.0,
        CurrencyPair.USDJPY: 1.8,
        CurrencyPair.USDCHF: 2.5,
        CurrencyPair.AUDUSD: 2.2,
        CurrencyPair.USDCAD: 2.8,
        CurrencyPair.NZDUSD: 3.0,
        CurrencyPair.EURJPY: 2.5,
        CurrencyPair.GBPJPY: 3.5,
        CurrencyPair.EURGBP: 2.8
    }
    
    def __init__(self, account_currency: str = "USD"):
        self.account_currency = account_currency
    
    def calculate_position_size_fixed_risk(self, 
                                         account_balance: float,
                                         risk_percentage: float,
                                         stop_loss_pips: float,
                                         currency_pair: CurrencyPair,
                                         market_conditions: MarketConditions = None) -> Dict[str, float]:
        """Calcula tamanho da posição baseado em risco fixo"""
        
        if market_conditions is None:
            market_conditions = MarketConditions()
        
        # Valor em risco
        risk_amount = account_balance * (risk_percentage / 100)
        
        # Valor do pip ajustado pelas condições de mercado
        base_pip_value = self.PIP_VALUES.get(currency_pair, 10.0)
        adjusted_pip_value = base_pip_value * market_conditions.volatility
        
        # Risco por pip
        risk_per_pip = stop_loss_pips * adjusted_pip_value
        
        if risk_per_pip <= 0:
            raise ValueError("Stop loss deve ser positivo")
        
        # Tamanho da posição em lotes
        position_size_lots = risk_amount / risk_per_pip
        
        # Valor nocional da posição
        notional_value = position_size_lots * 100000
        
        return {
            'position_size_lots': position_size_lots,
            'position_size_units': position_size_lots * 100000,
            'risk_amount': risk_amount,
            'risk_per_pip': risk_per_pip,
            'notional_value': notional_value,
            'pip_value': adjusted_pip_value,
            'max_loss': risk_amount
        }
    
    def calculate_position_size_kelly_criterion(self,
                                              account_balance: float,
                                              win_rate: float,
                                              avg_win: float,
                                              avg_loss: float,
                                              max_risk_pct: float = 10.0) -> Dict[str, float]:
        """Calcula tamanho da posição usando Critério de Kelly"""
        
        # Fórmula de Kelly: f = (bp - q) / b
        # onde: b = avg_win/avg_loss, p = win_rate, q = 1-win_rate
        
        if avg_loss <= 0:
            raise ValueError("Perda média deve ser positiva")
        
        b = avg_win / avg_loss  # Razão ganho/perda
        p = win_rate / 100      # Probabilidade de ganho
        q = 1 - p               # Probabilidade de perda
        
        # Fração de Kelly
        kelly_fraction = (b * p - q) / b
        
        # Limitar o risco máximo
        optimal_risk_pct = min(kelly_fraction * 100, max_risk_pct)
        optimal_risk_pct = max(optimal_risk_pct, 0)  # Não permitir valores negativos
        
        # Valor em risco
        risk_amount = account_balance * (optimal_risk_pct / 100)
        
        return {
            'kelly_fraction': kelly_fraction,
            'optimal_risk_percentage': optimal_risk_pct,
            'risk_amount': risk_amount,
            'expected_growth_rate': kelly_fraction * (p * avg_win - q * avg_loss),
            'recommendation': self._get_kelly_recommendation(kelly_fraction)
        }
    
    def _get_kelly_recommendation(self, kelly_fraction: float) -> str:
        """Fornece recomendação baseada na fração de Kelly"""
        if kelly_fraction <= 0:
            return "Sistema não lucrativo - não operar"
        elif kelly_fraction < 0.05:
            return "Risco muito baixo - considerar aumentar"
        elif kelly_fraction < 0.15:
            return "Risco adequado para trading conservador"
        elif kelly_fraction < 0.25:
            return "Risco moderado - monitorar drawdown"
        else:
            return "Risco alto - considerar reduzir posição"
    
    def calculate_position_size_volatility_adjusted(self,
                                                  account_balance: float,
                                                  base_risk_pct: float,
                                                  current_volatility: float,
                                                  average_volatility: float,
                                                  stop_loss_pips: float,
                                                  currency_pair: CurrencyPair) -> Dict[str, float]:
        """Calcula posição ajustada pela volatilidade atual"""
        
        # Fator de ajuste de volatilidade
        volatility_ratio = current_volatility / average_volatility
        
        # Ajustar risco baseado na volatilidade
        # Se volatilidade alta, reduzir posição; se baixa, aumentar
        adjusted_risk_pct = base_risk_pct / volatility_ratio
        
        # Limitar o risco ajustado
        adjusted_risk_pct = min(adjusted_risk_pct, base_risk_pct * 2)  # Máximo 2x o risco base
        adjusted_risk_pct = max(adjusted_risk_pct, base_risk_pct * 0.5)  # Mínimo 0.5x o risco base
        
        # Calcular posição com risco ajustado
        market_conditions = MarketConditions(volatility=volatility_ratio)
        position_info = self.calculate_position_size_fixed_risk(
            account_balance, adjusted_risk_pct, stop_loss_pips, currency_pair, market_conditions
        )
        
        position_info.update({
            'volatility_ratio': volatility_ratio,
            'base_risk_pct': base_risk_pct,
            'adjusted_risk_pct': adjusted_risk_pct,
            'volatility_adjustment': 'REDUCED' if volatility_ratio > 1 else 'INCREASED'
        })
        
        return position_info
    
    def calculate_correlation_adjusted_position(self,
                                              positions: List[Dict],
                                              new_position: Dict,
                                              correlation_matrix: Dict[str, Dict[str, float]],
                                              max_portfolio_risk: float = 10.0) -> Dict[str, float]:
        """Calcula posição ajustada considerando correlação do portfólio"""
        
        # Calcular risco atual do portfólio
        current_portfolio_risk = 0
        
        for pos in positions:
            current_portfolio_risk += pos.get('risk_amount', 0)
        
        # Calcular correlação média com posições existentes
        avg_correlation = 0
        if positions:
            correlations = []
            new_pair = new_position.get('currency_pair')
            
            for pos in positions:
                existing_pair = pos.get('currency_pair')
                if new_pair in correlation_matrix and existing_pair in correlation_matrix[new_pair]:
                    correlations.append(abs(correlation_matrix[new_pair][existing_pair]))
            
            avg_correlation = np.mean(correlations) if correlations else 0
        
        # Ajustar posição baseado na correlação
        # Alta correlação = reduzir posição
        correlation_adjustment = 1 - (avg_correlation * 0.5)  # Reduzir até 50% se correlação = 1
        
        # Verificar se nova posição excede risco máximo do portfólio
        new_risk_amount = new_position.get('risk_amount', 0) * correlation_adjustment
        total_risk = current_portfolio_risk + new_risk_amount
        
        account_balance = new_position.get('account_balance', 10000)
        portfolio_risk_pct = (total_risk / account_balance) * 100
        
        # Ajustar se exceder risco máximo
        if portfolio_risk_pct > max_portfolio_risk:
            risk_reduction = max_portfolio_risk / portfolio_risk_pct
            correlation_adjustment *= risk_reduction
        
        return {
            'correlation_adjustment': correlation_adjustment,
            'avg_correlation': avg_correlation,
            'adjusted_risk_amount': new_risk_amount,
            'portfolio_risk_pct': portfolio_risk_pct,
            'recommendation': self._get_correlation_recommendation(avg_correlation, portfolio_risk_pct)
        }
    
    def _get_correlation_recommendation(self, correlation: float, portfolio_risk: float) -> str:
        """Recomendação baseada em correlação e risco do portfólio"""
        if correlation > 0.8:
            return "Alta correlação - considerar diversificar"
        elif correlation > 0.5:
            return "Correlação moderada - monitorar exposição"
        elif portfolio_risk > 15:
            return "Risco de portfólio alto - reduzir posições"
        else:
            return "Correlação aceitável para nova posição"
    
    def calculate_optimal_stop_loss(self,
                                  currency_pair: CurrencyPair,
                                  timeframe: str,
                                  volatility_period: int = 14,
                                  atr_multiplier: float = 2.0) -> Dict[str, float]:
        """Calcula stop loss ótimo baseado em ATR e volatilidade"""
        
        # Valores típicos de ATR por timeframe (em pips)
        atr_values = {
            'M1': {'EURUSD': 8, 'GBPUSD': 12, 'USDJPY': 10},
            'M5': {'EURUSD': 15, 'GBPUSD': 20, 'USDJPY': 18},
            'M15': {'EURUSD': 25, 'GBPUSD': 35, 'USDJPY': 30},
            'H1': {'EURUSD': 45, 'GBPUSD': 60, 'USDJPY': 55},
            'H4': {'EURUSD': 80, 'GBPUSD': 110, 'USDJPY': 95},
            'D1': {'EURUSD': 120, 'GBPUSD': 160, 'USDJPY': 140}
        }
        
        # Obter ATR base
        pair_name = currency_pair.value.replace('/', '')
        base_atr = atr_values.get(timeframe, {}).get(pair_name, 50)
        
        # Calcular stop loss baseado em ATR
        optimal_stop_pips = base_atr * atr_multiplier
        
        # Ajustar por spread
        spread = self.TYPICAL_SPREADS.get(currency_pair, 2.0)
        adjusted_stop_pips = optimal_stop_pips + spread
        
        return {
            'base_atr_pips': base_atr,
            'optimal_stop_pips': optimal_stop_pips,
            'adjusted_stop_pips': adjusted_stop_pips,
            'spread_pips': spread,
            'atr_multiplier': atr_multiplier,
            'recommendation': f"Stop loss recomendado: {adjusted_stop_pips:.1f} pips"
        }
    
    def calculate_take_profit_levels(self,
                                   stop_loss_pips: float,
                                   risk_reward_ratios: List[float] = [1.0, 1.5, 2.0, 3.0]) -> Dict[str, List[float]]:
        """Calcula múltiplos níveis de take profit"""
        
        take_profit_levels = []
        
        for rr_ratio in risk_reward_ratios:
            tp_pips = stop_loss_pips * rr_ratio
            take_profit_levels.append({
                'rr_ratio': rr_ratio,
                'take_profit_pips': tp_pips,
                'partial_close_pct': 25 if rr_ratio == 1.0 else (50 if rr_ratio == 1.5 else 25)
            })
        
        return {
            'take_profit_levels': take_profit_levels,
            'strategy': 'Fechamento parcial em múltiplos níveis',
            'total_levels': len(take_profit_levels)
        }
    
    def generate_position_summary(self, position_data: Dict) -> str:
        """Gera resumo detalhado da posição calculada"""
        
        summary = f"""
=== RESUMO DA POSIÇÃO ===
Tamanho: {position_data.get('position_size_lots', 0):.4f} lotes
Valor Nocional: ${position_data.get('notional_value', 0):,.2f}
Risco: ${position_data.get('risk_amount', 0):,.2f}
Valor por Pip: ${position_data.get('pip_value', 0):.2f}
Perda Máxima: ${position_data.get('max_loss', 0):,.2f}
"""
        
        if 'kelly_fraction' in position_data:
            summary += f"\nFração de Kelly: {position_data['kelly_fraction']:.3f}"
            summary += f"\nRisco Ótimo: {position_data['optimal_risk_percentage']:.2f}%"
        
        if 'volatility_adjustment' in position_data:
            summary += f"\nAjuste de Volatilidade: {position_data['volatility_adjustment']}"
            summary += f"\nRatio de Volatilidade: {position_data['volatility_ratio']:.2f}"
        
        return summary

# Exemplo de uso avançado
if __name__ == "__main__":
    calculator = AdvancedPositionCalculator()
    
    # Exemplo 1: Cálculo básico de posição
    position = calculator.calculate_position_size_fixed_risk(
        account_balance=10000,
        risk_percentage=2.0,
        stop_loss_pips=20,
        currency_pair=CurrencyPair.EURUSD
    )
    
    print("=== CÁLCULO BÁSICO DE POSIÇÃO ===")
    print(calculator.generate_position_summary(position))
    
    # Exemplo 2: Critério de Kelly
    kelly_result = calculator.calculate_position_size_kelly_criterion(
        account_balance=10000,
        win_rate=65,
        avg_win=150,
        avg_loss=100
    )
    
    print("\n=== CRITÉRIO DE KELLY ===")
    print(f"Fração de Kelly: {kelly_result['kelly_fraction']:.3f}")
    print(f"Risco Ótimo: {kelly_result['optimal_risk_percentage']:.2f}%")
    print(f"Recomendação: {kelly_result['recommendation']}")
    
    # Exemplo 3: Stop loss ótimo
    stop_loss = calculator.calculate_optimal_stop_loss(
        currency_pair=CurrencyPair.EURUSD,
        timeframe='H1',
        atr_multiplier=2.0
    )
    
    print("\n=== STOP LOSS ÓTIMO ===")
    print(f"ATR Base: {stop_loss['base_atr_pips']} pips")
    print(f"Stop Loss Recomendado: {stop_loss['adjusted_stop_pips']:.1f} pips")
    
    # Exemplo 4: Níveis de take profit
    tp_levels = calculator.calculate_take_profit_levels(stop_loss_pips=20)
    
    print("\n=== NÍVEIS DE TAKE PROFIT ===")
    for level in tp_levels['take_profit_levels']:
        print(f"R:R {level['rr_ratio']}: {level['take_profit_pips']:.1f} pips (Fechar {level['partial_close_pct']}%)")