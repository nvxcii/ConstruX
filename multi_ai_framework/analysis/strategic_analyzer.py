"""
Strategic Analysis Coordinator
Integrates leverage calculation, settlement modeling, and AI analysis
"""

from typing import Dict, Any, List
from ..core.ai_coordinator import AIJusticeLeague
from .leverage_calculator import LeverageCalculator
from .settlement_modeler import SettlementModeler


class StrategicAnalysis:
    """Coordinates comprehensive strategic analysis"""

    def __init__(self, ai_league: AIJusticeLeague):
        self.ai_league = ai_league
        self.leverage_calculator = LeverageCalculator()
        self.settlement_modeler = SettlementModeler()

    def coordinate_analysis(self, case_data: Dict[str, Any],
                          intelligence_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate comprehensive strategic analysis

        Args:
            case_data: Case information
            intelligence_report: Intelligence gathered from research phase

        Returns:
            Complete strategic analysis report
        """
        print("🧠 Conducting strategic analysis...")

        # Calculate leverage
        print("  📊 Calculating leverage points...")
        leverage_analysis = self.leverage_calculator.calculate_leverage(
            case_data,
            intelligence_report.get('summary', {})
        )

        # Model settlement
        print("  💰 Modeling settlement predictions...")
        settlement_prediction = self.settlement_modeler.model_settlement(
            case_data,
            leverage_analysis.to_dict()
        )

        # Get AI strategic insights
        print("  🤖 Getting AI strategic recommendations...")
        ai_analysis = self.ai_league.distribute_analysis(
            case_data,
            {}  # Will be populated with research results
        )

        # Synthesize strategic recommendations
        print("  ⚡ Synthesizing strategic recommendations...")
        strategic_recommendations = self._synthesize_strategy(
            leverage_analysis,
            settlement_prediction,
            ai_analysis
        )

        return {
            'leverage_analysis': leverage_analysis.to_dict(),
            'settlement_prediction': settlement_prediction.to_dict(),
            'ai_insights': self._extract_ai_insights(ai_analysis),
            'strategic_recommendations': strategic_recommendations,
            'executive_summary': self._create_executive_summary(
                leverage_analysis,
                settlement_prediction
            )
        }

    def _extract_ai_insights(self, ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key insights from AI analysis"""
        insights = {}

        for model_name, result in ai_analysis.items():
            if result.success:
                insights[model_name] = {
                    'summary': result.response.content[:500] + '...',
                    'full_analysis': result.response.content
                }
            else:
                insights[model_name] = {
                    'error': result.error
                }

        return insights

    def _synthesize_strategy(self, leverage_analysis, settlement_prediction,
                            ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize unified strategic recommendations"""
        return {
            'primary_strategy': self._determine_primary_strategy(
                leverage_analysis,
                settlement_prediction
            ),
            'negotiation_approach': settlement_prediction.negotiation_strategy,
            'key_leverage_points': [
                pp['factor'] for pp in leverage_analysis.pressure_points
            ],
            'recommended_actions': self._generate_action_plan(
                leverage_analysis,
                settlement_prediction
            ),
            'risk_mitigation': self._generate_risk_mitigation(leverage_analysis),
            'timeline_strategy': self._generate_timeline_strategy(
                leverage_analysis,
                settlement_prediction
            )
        }

    def _determine_primary_strategy(self, leverage_analysis,
                                    settlement_prediction) -> str:
        """Determine primary strategic approach"""
        leverage_score = leverage_analysis.overall_leverage_score
        settlement_prob = settlement_prediction.confidence_level

        if leverage_score > 75 and settlement_prob > 0.7:
            return "AGGRESSIVE SETTLEMENT: Maximum pressure for rapid resolution"
        elif leverage_score > 60:
            return "STRUCTURED NEGOTIATION: Systematic pressure application"
        elif leverage_score > 45:
            return "BALANCED APPROACH: Build leverage while negotiating"
        else:
            return "EVIDENCE BUILDING: Strengthen position before major demands"

    def _generate_action_plan(self, leverage_analysis,
                             settlement_prediction) -> List[Dict[str, str]]:
        """Generate prioritized action plan"""
        actions = []

        # Priority 1: Leverage highest pressure points
        for pressure_point in leverage_analysis.pressure_points[:2]:
            actions.append({
                'priority': 'IMMEDIATE',
                'action': f"Apply pressure via {pressure_point['factor']}",
                'rationale': pressure_point['recommendation']
            })

        # Priority 2: Present settlement demand
        actions.append({
            'priority': 'HIGH',
            'action': f"Present settlement demand of ${settlement_prediction.recommended_demand:,.0f}",
            'rationale': f"Based on {settlement_prediction.confidence_level*100:.0f}% confidence prediction"
        })

        # Priority 3: Prepare regulatory actions
        if leverage_analysis.leverage_factors.get('regulatory_risk', 0) > 50:
            actions.append({
                'priority': 'HIGH',
                'action': "File regulatory complaints with appropriate agencies",
                'rationale': "High regulatory leverage identified"
            })

        # Priority 4: Media strategy
        if leverage_analysis.leverage_factors.get('public_exposure', 0) > 50:
            actions.append({
                'priority': 'MEDIUM',
                'action': "Prepare media outreach strategy",
                'rationale': "Significant public interest potential"
            })

        return actions

    def _generate_risk_mitigation(self, leverage_analysis) -> List[str]:
        """Generate risk mitigation strategies"""
        mitigations = [
            "Document all communications and maintain detailed records",
            "Ensure all evidence is properly preserved and authenticated",
            "Monitor opponent's response patterns for counter-strategies"
        ]

        if leverage_analysis.overall_leverage_score < 60:
            mitigations.append(
                "Continue evidence gathering to strengthen position"
            )

        if leverage_analysis.settlement_probability < 0.6:
            mitigations.append(
                "Prepare for potential litigation while negotiating"
            )

        return mitigations

    def _generate_timeline_strategy(self, leverage_analysis,
                                   settlement_prediction) -> Dict[str, str]:
        """Generate strategic timeline recommendations"""
        optimal_timing = leverage_analysis.optimal_timing

        timeline = {
            'immediate': 'Present initial demand and evidence package',
            'week_1-2': 'Apply primary pressure points, monitor response',
            'week_3-4': 'Escalate with regulatory filings if needed',
            'week_5-8': 'Structured negotiation phases',
            'contingency': 'Prepare litigation filing if settlement stalls'
        }

        if optimal_timing.get('immediate_action'):
            timeline['immediate'] = 'URGENT: File complaints and present demand immediately'

        return timeline

    def _create_executive_summary(self, leverage_analysis,
                                  settlement_prediction) -> Dict[str, Any]:
        """Create executive summary of strategic analysis"""
        return {
            'overall_strength': self._rate_case_strength(
                leverage_analysis.overall_leverage_score
            ),
            'leverage_score': f"{leverage_analysis.overall_leverage_score:.1f}/100",
            'opponent_risk': leverage_analysis.risk_to_opponent,
            'settlement_probability': f"{leverage_analysis.settlement_probability*100:.0f}%",
            'predicted_settlement_range': {
                'low': f"${settlement_prediction.predicted_range['low']:,.0f}",
                'mid': f"${settlement_prediction.predicted_range['mid']:,.0f}",
                'high': f"${settlement_prediction.predicted_range['high']:,.0f}"
            },
            'recommended_demand': f"${settlement_prediction.recommended_demand:,.0f}",
            'settlement_floor': f"${settlement_prediction.recommended_floor:,.0f}",
            'top_pressure_points': [
                pp['factor'] for pp in leverage_analysis.pressure_points[:3]
            ],
            'strategic_posture': leverage_analysis.optimal_timing.get('recommended_phase', 'MEASURED')
        }

    def _rate_case_strength(self, leverage_score: float) -> str:
        """Rate overall case strength"""
        if leverage_score > 80:
            return "EXCELLENT - Very strong case with multiple leverage points"
        elif leverage_score > 65:
            return "STRONG - Solid case with significant leverage"
        elif leverage_score > 50:
            return "MODERATE - Reasonable case with some leverage"
        elif leverage_score > 35:
            return "DEVELOPING - Building case strength"
        else:
            return "WEAK - Requires significant evidence building"
