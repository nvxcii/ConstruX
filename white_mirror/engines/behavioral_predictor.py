"""
Behavioral Predictor - Pattern Recognition Engine (POC3)

The Behavioral Predictor uses pattern recognition to anticipate
future states and behaviors. It implements:
    - Historical pattern analysis
    - Drift trajectory prediction
    - Violation likelihood scoring
    - Intervention timing optimization

This is POC3 in the White Mirror research agenda.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import statistics
import math


class PredictionType(Enum):
    """Types of predictions"""
    STATE_TRANSITION = "state_transition"
    VIOLATION_LIKELIHOOD = "violation_likelihood"
    DRIFT_TRAJECTORY = "drift_trajectory"
    INTERVENTION_TIMING = "intervention_timing"
    ALIGNMENT_FORECAST = "alignment_forecast"


class TrendDirection(Enum):
    """Trend directions"""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    VOLATILE = "volatile"


@dataclass
class DataPoint:
    """A single data point for pattern analysis"""
    timestamp: datetime
    dimension: str  # What is being measured
    value: float
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Pattern:
    """A detected pattern in the data"""
    id: str
    pattern_type: str
    confidence: float
    description: str
    data_points_used: int
    trend: TrendDirection
    periodicity: Optional[float] = None  # If cyclical, the period

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "pattern_type": self.pattern_type,
            "confidence": self.confidence,
            "description": self.description,
            "data_points_used": self.data_points_used,
            "trend": self.trend.value,
            "periodicity": self.periodicity
        }


@dataclass
class Prediction:
    """A prediction about future state"""
    id: str
    prediction_type: PredictionType
    target_dimension: str
    predicted_value: float
    confidence: float
    time_horizon: timedelta
    supporting_patterns: List[str]
    recommendation: str
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "prediction_type": self.prediction_type.value,
            "target_dimension": self.target_dimension,
            "predicted_value": self.predicted_value,
            "confidence": self.confidence,
            "time_horizon_days": self.time_horizon.days,
            "supporting_patterns": self.supporting_patterns,
            "recommendation": self.recommendation,
            "timestamp": self.timestamp.isoformat()
        }


class BehavioralPredictor:
    """
    Behavioral Prediction Engine (POC3)

    Uses pattern recognition to predict future states and
    optimize intervention timing.
    """

    def __init__(self):
        self._data_points: Dict[str, List[DataPoint]] = {}
        self._patterns: Dict[str, Pattern] = {}
        self._predictions: List[Prediction] = []

        # Configuration
        self._min_data_points = 10
        self._confidence_threshold = 0.6
        self._pattern_window_days = 30

    def ingest_data(
        self,
        dimension: str,
        value: float,
        timestamp: Optional[datetime] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ingest a data point for pattern analysis.

        Args:
            dimension: What is being measured (e.g., "cil_conscience", "compliance_score")
            value: The measured value
            timestamp: When the measurement was taken
            context: Additional context

        Returns:
            Ingestion result with pattern detection status
        """
        if dimension not in self._data_points:
            self._data_points[dimension] = []

        data_point = DataPoint(
            timestamp=timestamp or datetime.utcnow(),
            dimension=dimension,
            value=value,
            context=context or {}
        )

        self._data_points[dimension].append(data_point)

        # Sort by timestamp
        self._data_points[dimension].sort(key=lambda dp: dp.timestamp)

        # Attempt pattern detection if enough data
        patterns_detected = []
        if len(self._data_points[dimension]) >= self._min_data_points:
            new_patterns = self._detect_patterns(dimension)
            patterns_detected = [p.to_dict() for p in new_patterns]

        return {
            "dimension": dimension,
            "value": value,
            "data_points_for_dimension": len(self._data_points[dimension]),
            "patterns_detected": patterns_detected,
            "ready_for_prediction": len(self._data_points[dimension]) >= self._min_data_points
        }

    def _detect_patterns(self, dimension: str) -> List[Pattern]:
        """Detect patterns in a dimension's data"""
        data = self._data_points.get(dimension, [])
        if len(data) < self._min_data_points:
            return []

        patterns = []
        values = [dp.value for dp in data]

        # Detect trend pattern
        trend_pattern = self._detect_trend(dimension, values)
        if trend_pattern:
            patterns.append(trend_pattern)
            self._patterns[trend_pattern.id] = trend_pattern

        # Detect volatility pattern
        volatility_pattern = self._detect_volatility(dimension, values)
        if volatility_pattern:
            patterns.append(volatility_pattern)
            self._patterns[volatility_pattern.id] = volatility_pattern

        # Detect cyclical pattern
        cyclical_pattern = self._detect_cyclical(dimension, data)
        if cyclical_pattern:
            patterns.append(cyclical_pattern)
            self._patterns[cyclical_pattern.id] = cyclical_pattern

        return patterns

    def _detect_trend(self, dimension: str, values: List[float]) -> Optional[Pattern]:
        """Detect linear trend in data"""
        if len(values) < 5:
            return None

        # Simple linear regression
        n = len(values)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n

        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return None

        slope = numerator / denominator

        # Determine trend direction
        if abs(slope) < 0.01:
            trend = TrendDirection.STABLE
        elif slope > 0:
            trend = TrendDirection.IMPROVING
        else:
            trend = TrendDirection.DECLINING

        # Calculate R-squared for confidence
        y_pred = [y_mean + slope * (x[i] - x_mean) for i in range(n)]
        ss_res = sum((values[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((values[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        pattern_id = hashlib.sha256(
            f"trend:{dimension}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12]

        return Pattern(
            id=pattern_id,
            pattern_type="trend",
            confidence=max(0, min(1, r_squared)),
            description=f"{trend.value.title()} trend detected in {dimension} (slope: {slope:.4f})",
            data_points_used=n,
            trend=trend
        )

    def _detect_volatility(self, dimension: str, values: List[float]) -> Optional[Pattern]:
        """Detect volatility pattern"""
        if len(values) < 5:
            return None

        mean = statistics.mean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0

        # Coefficient of variation
        cv = std / mean if mean != 0 else 0

        if cv > 0.3:
            trend = TrendDirection.VOLATILE
            confidence = min(1.0, cv)
        else:
            return None  # Not volatile enough to report

        pattern_id = hashlib.sha256(
            f"volatility:{dimension}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12]

        return Pattern(
            id=pattern_id,
            pattern_type="volatility",
            confidence=confidence,
            description=f"High volatility detected in {dimension} (CV: {cv:.2f})",
            data_points_used=len(values),
            trend=trend
        )

    def _detect_cyclical(
        self, dimension: str, data: List[DataPoint]
    ) -> Optional[Pattern]:
        """Detect cyclical patterns (simplified autocorrelation)"""
        if len(data) < 14:  # Need at least 2 weeks of data
            return None

        values = [dp.value for dp in data]
        n = len(values)

        # Check for weekly pattern (7 data points)
        if n >= 14:
            # Calculate autocorrelation at lag 7
            mean = statistics.mean(values)
            var = statistics.variance(values) if n > 1 else 1

            lag = 7
            if var > 0:
                autocorr = sum(
                    (values[i] - mean) * (values[i + lag] - mean)
                    for i in range(n - lag)
                ) / ((n - lag) * var)
            else:
                autocorr = 0

            if autocorr > 0.3:  # Significant autocorrelation
                pattern_id = hashlib.sha256(
                    f"cyclical:{dimension}:{datetime.utcnow().isoformat()}".encode()
                ).hexdigest()[:12]

                return Pattern(
                    id=pattern_id,
                    pattern_type="cyclical",
                    confidence=min(1.0, autocorr),
                    description=f"Weekly cyclical pattern detected in {dimension}",
                    data_points_used=n,
                    trend=TrendDirection.STABLE,
                    periodicity=7.0
                )

        return None

    def predict(
        self,
        dimension: str,
        prediction_type: str = "alignment_forecast",
        horizon_days: int = 7
    ) -> Dict[str, Any]:
        """
        Generate a prediction for a dimension.

        Args:
            dimension: The dimension to predict
            prediction_type: Type of prediction
            horizon_days: How far ahead to predict

        Returns:
            Prediction result
        """
        data = self._data_points.get(dimension, [])
        if len(data) < self._min_data_points:
            return {
                "error": "insufficient_data",
                "dimension": dimension,
                "data_points": len(data),
                "required": self._min_data_points
            }

        try:
            pred_type = PredictionType(prediction_type)
        except ValueError:
            pred_type = PredictionType.ALIGNMENT_FORECAST

        # Get relevant patterns
        relevant_patterns = [
            p for p in self._patterns.values()
            if dimension in p.description.lower()
        ]

        # Generate prediction based on patterns
        values = [dp.value for dp in data]
        current_value = values[-1]
        mean_value = statistics.mean(values)

        # Base prediction on trend
        trend_patterns = [p for p in relevant_patterns if p.pattern_type == "trend"]

        if trend_patterns:
            trend = trend_patterns[0]
            if trend.trend == TrendDirection.IMPROVING:
                predicted_value = min(1.0, current_value + 0.05 * horizon_days / 7)
            elif trend.trend == TrendDirection.DECLINING:
                predicted_value = max(0.0, current_value - 0.05 * horizon_days / 7)
            else:
                predicted_value = current_value
        else:
            # Revert to mean
            predicted_value = current_value + (mean_value - current_value) * 0.3

        # Calculate confidence
        base_confidence = 0.5
        if relevant_patterns:
            pattern_confidence = statistics.mean([p.confidence for p in relevant_patterns])
            base_confidence = (base_confidence + pattern_confidence) / 2

        # Decay confidence with time horizon
        confidence = base_confidence * math.exp(-0.1 * horizon_days / 7)

        # Generate recommendation
        recommendation = self._generate_recommendation(
            dimension, current_value, predicted_value, relevant_patterns
        )

        # Create prediction record
        prediction_id = hashlib.sha256(
            f"{datetime.utcnow().isoformat()}:{dimension}:{pred_type.value}".encode()
        ).hexdigest()[:12]

        prediction = Prediction(
            id=prediction_id,
            prediction_type=pred_type,
            target_dimension=dimension,
            predicted_value=predicted_value,
            confidence=confidence,
            time_horizon=timedelta(days=horizon_days),
            supporting_patterns=[p.id for p in relevant_patterns],
            recommendation=recommendation,
            timestamp=datetime.utcnow()
        )

        self._predictions.append(prediction)

        return {
            "prediction": prediction.to_dict(),
            "current_value": current_value,
            "change_expected": predicted_value - current_value,
            "patterns_used": [p.to_dict() for p in relevant_patterns]
        }

    def _generate_recommendation(
        self,
        dimension: str,
        current: float,
        predicted: float,
        patterns: List[Pattern]
    ) -> str:
        """Generate recommendation based on prediction"""
        change = predicted - current

        if abs(change) < 0.05:
            return f"Stable {dimension} expected. Maintain current practices."

        if change > 0:
            return f"Positive trend in {dimension}. Continue current trajectory."

        # Negative prediction
        volatile_patterns = [p for p in patterns if p.trend == TrendDirection.VOLATILE]
        if volatile_patterns:
            return f"Declining {dimension} with high volatility. Implement stabilization measures."

        return f"Declining {dimension} predicted. Consider intervention within {int(abs(change) * 30)} days."

    def predict_violation_likelihood(
        self,
        compliance_history: List[float],
        violation_history: List[int]
    ) -> Dict[str, Any]:
        """
        Predict likelihood of future violations.

        Args:
            compliance_history: Historical compliance scores
            violation_history: Historical violation counts

        Returns:
            Violation likelihood prediction
        """
        if not compliance_history:
            return {"error": "no_compliance_data"}

        current_compliance = compliance_history[-1]
        avg_compliance = statistics.mean(compliance_history)

        # Base likelihood inversely proportional to compliance
        base_likelihood = 1.0 - current_compliance

        # Adjust for trend
        if len(compliance_history) >= 3:
            recent_trend = compliance_history[-1] - compliance_history[-3]
            trend_adjustment = -recent_trend * 0.5  # Improving trend reduces likelihood
        else:
            trend_adjustment = 0

        # Adjust for violation history
        if violation_history:
            recent_violations = sum(violation_history[-5:]) if len(violation_history) >= 5 else sum(violation_history)
            history_adjustment = recent_violations * 0.05
        else:
            history_adjustment = 0

        likelihood = max(0, min(1, base_likelihood + trend_adjustment + history_adjustment))

        # Risk category
        if likelihood < 0.2:
            risk_category = "low"
        elif likelihood < 0.5:
            risk_category = "moderate"
        elif likelihood < 0.8:
            risk_category = "high"
        else:
            risk_category = "critical"

        return {
            "violation_likelihood": likelihood,
            "risk_category": risk_category,
            "current_compliance": current_compliance,
            "compliance_trend": "improving" if trend_adjustment < 0 else "declining" if trend_adjustment > 0 else "stable",
            "recommendation": self._violation_recommendation(likelihood, risk_category)
        }

    def _violation_recommendation(self, likelihood: float, category: str) -> str:
        """Generate recommendation based on violation likelihood"""
        recommendations = {
            "low": "Continue monitoring. Current practices are effective.",
            "moderate": "Increase monitoring frequency. Review recent changes.",
            "high": "Implement preventive measures immediately. Conduct system review.",
            "critical": "Emergency intervention required. Activate DPAP protocols."
        }
        return recommendations.get(category, "Assess current state.")

    def get_patterns(self) -> List[Dict[str, Any]]:
        """Get all detected patterns"""
        return [p.to_dict() for p in self._patterns.values()]

    def get_predictions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent predictions"""
        return [p.to_dict() for p in self._predictions[-limit:]]

    def get_dimension_summary(self, dimension: str) -> Dict[str, Any]:
        """Get summary for a specific dimension"""
        data = self._data_points.get(dimension, [])

        if not data:
            return {"error": "no_data", "dimension": dimension}

        values = [dp.value for dp in data]
        relevant_patterns = [
            p for p in self._patterns.values()
            if dimension in p.description.lower()
        ]

        return {
            "dimension": dimension,
            "data_points": len(data),
            "current_value": values[-1],
            "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "patterns": [p.to_dict() for p in relevant_patterns],
            "ready_for_prediction": len(data) >= self._min_data_points
        }
