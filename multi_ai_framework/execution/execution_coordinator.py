"""
Execution Coordination
Coordinates multi-front campaign execution across all channels
"""

from typing import Dict, Any
from ..core.ai_coordinator import AIJusticeLeague
from .complaint_generator import ComplaintGenerator
from .cowork_dispatcher import CoworkDispatcher
from .media_coordinator import MediaCoordinator
from .settlement_negotiator import SettlementNegotiator


class ExecutionCoordination:
    """Coordinates synchronized multi-front campaign execution"""

    def __init__(self, ai_league: AIJusticeLeague):
        self.ai_league = ai_league
        self.complaint_generator = ComplaintGenerator()
        self.cowork_dispatcher = CoworkDispatcher()
        self.media_coordinator = MediaCoordinator()
        self.settlement_negotiator = SettlementNegotiator()

    def coordinate_deployment(self, case_data: Dict[str, Any],
                             strategic_analysis: Dict[str, Any],
                             intelligence_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate complete campaign deployment

        Args:
            case_data: Case information
            strategic_analysis: Strategic analysis results
            intelligence_report: Intelligence gathering results

        Returns:
            Complete execution package with all deliverables
        """
        print("⚡ Coordinating campaign execution...")

        # Get AI-generated execution content
        print("  🤖 Generating AI execution content...")
        ai_execution = self.ai_league.distribute_execution(
            case_data,
            {}  # Populated with analysis results
        )

        # Extract AI-generated content
        ai_content = self._extract_ai_content(ai_execution)

        # Generate complaints
        print("  📄 Generating regulatory complaints...")
        complaints = self.complaint_generator.generate_complaints(
            case_data,
            strategic_analysis,
            ai_content.get('complaint', '')
        )

        # Prepare media strategy
        print("  📰 Preparing media strategy package...")
        media_package = self.media_coordinator.prepare_media_strategy(
            case_data,
            strategic_analysis,
            ai_content.get('media', '')
        )

        # Create negotiation framework
        print("  🤝 Creating settlement negotiation framework...")
        negotiation_framework = self.settlement_negotiator.create_negotiation_framework(
            case_data,
            strategic_analysis
        )

        # Create coordinated timeline
        print("  📅 Creating coordinated campaign timeline...")
        campaign_timeline = self._create_campaign_timeline(
            case_data,
            strategic_analysis,
            complaints,
            media_package,
            negotiation_framework
        )

        # Generate execution playbook
        print("  📋 Generating execution playbook...")
        execution_playbook = self._create_execution_playbook(
            case_data,
            strategic_analysis,
            complaints,
            media_package,
            negotiation_framework,
            campaign_timeline
        )

        result = {
            'complaints': [c.to_dict() for c in complaints],
            'media_package': media_package.to_dict(),
            'negotiation_framework': negotiation_framework.to_dict(),
            'campaign_timeline': campaign_timeline,
            'execution_playbook': execution_playbook,
            'ai_content': ai_content,
            'deployment_summary': self._create_deployment_summary(
                complaints,
                media_package,
                negotiation_framework
            )
        }

        # Optional: generate CoworkDispatch if case_data requests it
        if case_data.get('generate_dispatch'):
            print("  📋 Generating CoworkDispatch handoff document...")
            dispatch_doc = self.cowork_dispatcher.generate_dispatch(case_data)
            result['cowork_dispatch'] = dispatch_doc.to_dict()

        return result

    def _extract_ai_content(self, ai_execution: Dict[str, Any]) -> Dict[str, str]:
        """Extract AI-generated content for different purposes"""
        content = {}

        for model_name, result in ai_execution.items():
            if result.success:
                if model_name == 'claude':
                    content['complaint'] = result.response.content
                elif model_name == 'chatgpt':
                    content['media'] = result.response.content
                elif model_name == 'deepseek':
                    content['settlement'] = result.response.content
                elif model_name == 'gemini':
                    content['timeline'] = result.response.content

        return content

    def _create_campaign_timeline(self, case_data: Dict[str, Any],
                                 strategic_analysis: Dict[str, Any],
                                 complaints, media_package,
                                 negotiation_framework) -> Dict[str, Any]:
        """Create coordinated campaign timeline"""
        leverage = strategic_analysis.get('leverage_analysis', {})
        immediate_action = leverage.get('optimal_timing', {}).get('immediate_action', False)

        timeline = {
            'phase_1_opening': {
                'timeframe': 'Day 1-2',
                'actions': [
                    'Finalize all documents and packages',
                    'Prepare evidence packages',
                    'Coordinate with attorneys',
                    'Review all materials for accuracy'
                ],
                'deliverables': [
                    'Verified complaint packages',
                    'Evidence compilation',
                    'Settlement demand letter'
                ]
            },
            'phase_2_launch': {
                'timeframe': 'Day 3' if immediate_action else 'Day 3-7',
                'actions': [
                    'Deliver settlement demand via certified mail and email',
                    'Set 21-day response deadline',
                    'Prepare regulatory complaints for filing',
                    'Alert media contacts (hold for now)'
                ],
                'deliverables': [
                    'Settlement demand delivered',
                    'Complaints ready to file',
                    'Media package prepared'
                ]
            },
            'phase_3_pressure': {
                'timeframe': 'Day 8-14',
                'actions': [
                    'Monitor for settlement response',
                    'If no response by day 10: send follow-up',
                    'If inadequate response: file regulatory complaints',
                    'Prepare media outreach if needed'
                ],
                'deliverables': [
                    'Response tracking',
                    'Regulatory complaints filed (if needed)',
                    'Media outreach initiated (if needed)'
                ]
            },
            'phase_4_negotiation': {
                'timeframe': 'Day 15-45',
                'actions': [
                    'Active settlement negotiations',
                    'Follow negotiation framework',
                    'Strategic concessions per schedule',
                    'Coordinate regulatory and media pressure'
                ],
                'deliverables': [
                    'Negotiation position updates',
                    'Counter-offers and responses',
                    'Ongoing pressure maintenance'
                ]
            },
            'phase_5_resolution': {
                'timeframe': 'Day 46-60',
                'actions': [
                    'Finalize settlement terms',
                    'Draft settlement agreement',
                    'Execute agreement',
                    'Close regulatory matters (if settled)'
                ],
                'deliverables': [
                    'Executed settlement agreement',
                    'Payment received',
                    'Case resolution'
                ]
            },
            'contingency_litigation': {
                'timeframe': 'If settlement fails - Day 60+',
                'actions': [
                    'File civil lawsuit',
                    'Pursue regulatory investigations',
                    'Execute media strategy',
                    'Begin discovery process'
                ],
                'deliverables': [
                    'Lawsuit filed',
                    'Public awareness campaign',
                    'Litigation strategy'
                ]
            }
        }

        return timeline

    def _create_execution_playbook(self, case_data: Dict[str, Any],
                                  strategic_analysis: Dict[str, Any],
                                  complaints, media_package,
                                  negotiation_framework,
                                  timeline: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive execution playbook"""
        leverage_score = strategic_analysis.get('leverage_analysis', {}).get('overall_leverage_score', 0)

        playbook = {
            'executive_summary': {
                'case_strength': f"{leverage_score:.1f}/100",
                'primary_strategy': strategic_analysis.get('strategic_recommendations', {}).get('primary_strategy', ''),
                'expected_timeline': '30-60 days to settlement',
                'key_leverage_points': [
                    pp['factor'] for pp in
                    strategic_analysis.get('leverage_analysis', {}).get('pressure_points', [])[:3]
                ]
            },
            'priority_actions': {
                'immediate': [
                    'Deliver settlement demand',
                    'Set response deadline (21 days)',
                    'Prepare regulatory complaints'
                ],
                'short_term': [
                    'Monitor opponent response',
                    'File complaints if no response',
                    'Initiate media strategy if needed'
                ],
                'ongoing': [
                    'Maintain negotiation pressure',
                    'Coordinate multi-front campaign',
                    'Adapt tactics based on responses'
                ]
            },
            'decision_trees': {
                'opponent_responds_positively': {
                    'action': 'Engage in good faith negotiation',
                    'follow': 'Negotiation framework phases',
                    'maintain': 'Professional pressure, hold regulatory/media in reserve'
                },
                'opponent_responds_with_lowball': {
                    'action': 'Reiterate evidence and comparables',
                    'escalate': 'File regulatory complaints',
                    'deadline': '7 days for serious counter-offer'
                },
                'opponent_denies_liability': {
                    'action': 'Present key evidence package',
                    'escalate': 'File all regulatory complaints',
                    'prepare': 'Litigation and media strategy'
                },
                'no_response_by_deadline': {
                    'action': 'File all regulatory complaints immediately',
                    'escalate': 'Initiate media outreach',
                    'prepare': 'Litigation filing'
                },
                'negotiations_stall': {
                    'action': 'Apply pressure via regulatory updates',
                    'consider': 'Mediation or litigation',
                    'maintain': 'Communication but with firm deadlines'
                }
            },
            'communication_protocols': {
                'with_opponent': 'All communications in writing, professional tone',
                'with_agencies': 'Responsive, provide requested information promptly',
                'with_media': 'Coordinated through media package, stick to talking points',
                'internal': 'Regular updates to client, strategic decision coordination'
            },
            'success_metrics': {
                'primary': 'Settlement at or above target amount',
                'secondary': [
                    'Favorable non-monetary terms',
                    'Timely resolution',
                    'Regulatory validation of claims',
                    'Professional relationship maintained (if possible)'
                ]
            },
            'risk_management': {
                'legal_risks': 'Verify all facts, coordinate with counsel',
                'reputational_risks': 'Maintain professional tone, fact-based communication',
                'tactical_risks': 'Don\'t overplay hand, be prepared to follow through on threats',
                'timeline_risks': 'Monitor deadlines, maintain pressure without appearing desperate'
            }
        }

        return playbook

    def _create_deployment_summary(self, complaints, media_package,
                                  negotiation_framework) -> Dict[str, Any]:
        """Create deployment summary"""
        return {
            'total_complaints': len(complaints),
            'complaint_types': [c.complaint_type for c in complaints],
            'settlement_demand': f"${negotiation_framework.opening_position['monetary_demand']:,.0f}",
            'settlement_target': f"${negotiation_framework.target_settlement['monetary_target']:,.0f}",
            'settlement_floor': f"${negotiation_framework.walkaway_point['minimum_acceptable']:,.0f}",
            'media_approach': media_package.metadata.get('recommended_approach', ''),
            'ready_to_deploy': True,
            'deployment_checklist': [
                '✓ Settlement demand prepared',
                '✓ Regulatory complaints ready',
                '✓ Media strategy developed',
                '✓ Negotiation framework created',
                '✓ Timeline established',
                '✓ Playbook complete'
            ]
        }

    def export_execution_package(self, execution_results: Dict[str, Any],
                                output_dir: str):
        """Export complete execution package"""
        from pathlib import Path
        import json

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Export complaints
        complaint_dir = f"{output_dir}/complaints"
        Path(complaint_dir).mkdir(parents=True, exist_ok=True)

        from .complaint_generator import ComplaintPackage
        complaints = [ComplaintPackage(**c) for c in execution_results.get('complaints', [])]
        for complaint in complaints:
            self.complaint_generator.export_complaint(
                complaint,
                f"{complaint_dir}/{complaint.complaint_type}_complaint.txt"
            )

        # Export media package
        media_dir = f"{output_dir}/media"
        from .media_coordinator import MediaPackage
        media_pkg = MediaPackage(**execution_results.get('media_package', {}))
        self.media_coordinator.export_media_package(media_pkg, media_dir)

        # Export negotiation framework
        from .settlement_negotiator import NegotiationFramework
        neg_framework = NegotiationFramework(**execution_results.get('negotiation_framework', {}))
        self.settlement_negotiator.export_negotiation_framework(
            neg_framework,
            f"{output_dir}/negotiation_framework.json"
        )

        # Export timeline
        with open(f"{output_dir}/campaign_timeline.json", 'w') as f:
            json.dump(execution_results.get('campaign_timeline', {}), f, indent=2)

        # Export playbook
        with open(f"{output_dir}/execution_playbook.json", 'w') as f:
            json.dump(execution_results.get('execution_playbook', {}), f, indent=2)

        # Create master summary
        with open(f"{output_dir}/DEPLOYMENT_SUMMARY.txt", 'w') as f:
            summary = execution_results.get('deployment_summary', {})
            f.write("CAMPAIGN DEPLOYMENT SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total Complaints: {summary.get('total_complaints', 0)}\n")
            f.write(f"Settlement Demand: {summary.get('settlement_demand', '')}\n")
            f.write(f"Target Settlement: {summary.get('settlement_target', '')}\n")
            f.write(f"Settlement Floor: {summary.get('settlement_floor', '')}\n")
            f.write(f"Media Approach: {summary.get('media_approach', '')}\n\n")
            f.write("DEPLOYMENT CHECKLIST:\n")
            for item in summary.get('deployment_checklist', []):
                f.write(f"{item}\n")
