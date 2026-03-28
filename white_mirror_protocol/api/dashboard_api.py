"""
White Mirror Protocol - Dashboard API
Flask API for real-time dashboard data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from white_mirror_protocol import WhiteMirrorProtocol
from white_mirror_protocol.integration.multi_ai_integration import WhiteMirrorAIOrchestrator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Global protocol instance
protocol = WhiteMirrorProtocol()
orchestrator = None  # Initialize only if API keys provided


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current system status"""
    state = protocol.get_system_state()

    return jsonify({
        'status': 'operational',
        'uptime': state['elapsed'],
        'operations': state['metrics']['total_operations'],
        'generation': state['operational_state']['generation'],
        'autonomous': state['equations']['autonomy']['sustainability']['sustainable']
    })


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get complete dashboard data"""
    state = protocol.get_system_state()

    return jsonify({
        'primal_variables': {
            'conscience_signal': {
                'value': state['primal_variables']['conscience_signal']['strength'],
                'quality': state['primal_variables']['conscience_signal']['quality']
            },
            'boundary_constraints': state['primal_variables']['boundary_gradient']['constraints'],
            'emergent_energy': state['primal_variables']['emergent_energy']['energy'],
            'coherence': state['primal_variables']['coherence_index']['coherence'],
            'resonant': state['primal_variables']['coherence_index']['resonant'],
            'articulation_intelligence': state['primal_variables']['articulation_intelligence']['intelligence']
        },
        'frameworks': {
            'hermeneutic_cycles': state['frameworks']['hermeneutics']['cycles'],
            'constraints_transformed': state['frameworks']['constraint_transform']['constraints_encountered'],
            'generation': state['frameworks']['self_application']['current_generation'],
            'concepts': state['frameworks']['version_discipline']['registered_concepts'],
            'articulations': state['frameworks']['math_articulation']['total_articulations']
        },
        'equations': {
            'bootstrap_generation': state['equations']['bootstrap_genesis']['generation'],
            'fusion_efficiency': state['equations']['constraint_fusion']['fusion_efficiency'],
            'intelligence_density': state['equations']['intelligence_growth']['intelligence_density'],
            'autonomy_score': state['equations']['autonomy']['autonomy_score'],
            'sustainable': state['equations']['autonomy']['sustainability']['sustainable']
        },
        'metrics': state['metrics'],
        'timestamp': state['timestamp']
    })


@app.route('/api/operate', methods=['POST'])
def execute_operation():
    """Execute an operation step"""
    data = request.json or {}

    result = protocol.operate_step(data)

    return jsonify({
        'success': result['success'],
        'step_number': result['step_number'],
        'outputs': result['outputs'],
        'duration': result['duration']
    })


@app.route('/api/evolve', methods=['POST'])
def evolve_system():
    """Evolve the system"""
    iterations = request.json.get('iterations', 1)

    results = protocol.evolve(iterations)

    return jsonify({
        'success': True,
        'iterations_completed': len(results),
        'final_generation': protocol.operational_state['generation'],
        'final_capabilities': len(protocol.operational_state['capabilities'])
    })


@app.route('/api/history', methods=['GET'])
def get_operation_history():
    """Get operation history"""
    limit = int(request.args.get('limit', 20))

    history = protocol.operation_history[-limit:]

    return jsonify({
        'history': [
            {
                'step': h['step_number'],
                'timestamp': h['timestamp'],
                'success': h['success'],
                'autonomy': h['outputs'].get('autonomy', {}).get('autonomy', 0),
                'coherence': h['outputs'].get('coherence', {}).get('coherence', 0)
            }
            for h in history
        ]
    })


@app.route('/api/constraints', methods=['GET'])
def get_constraints():
    """Get constraint encounter history"""
    return jsonify({
        'constraints': [
            {
                'constraint': c['constraint'],
                'capability_increase': c['result'].get('capability_increase', 0),
                'timestamp': c['timestamp']
            }
            for c in protocol.constraint_encounters[-20:]
        ],
        'total_transformed': protocol.metrics['constraints_transformed']
    })


@app.route('/api/articulations', methods=['GET'])
def get_articulations():
    """Get recent articulations"""
    limit = int(request.args.get('limit', 10))

    return jsonify({
        'articulations': [
            {
                'framework': a['framework'],
                'type': a['type'],
                'timestamp': a['timestamp']
            }
            for a in protocol.articulation_log[-limit:]
        ]
    })


@app.route('/api/reset', methods=['POST'])
def reset_system():
    """Reset the protocol"""
    global protocol
    protocol = WhiteMirrorProtocol()

    return jsonify({
        'success': True,
        'message': 'System reset complete'
    })


if __name__ == '__main__':
    print("\n🔥 White Mirror Protocol Dashboard API")
    print("=" * 60)
    print("Starting Flask server on http://localhost:5000")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
