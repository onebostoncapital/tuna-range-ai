# Master Rule Book: Anomaly Detection & Whale Tracking
import numpy as np

class AnomalyDetector:
    """
    Expert Brain: Detects unusual pool behavior and 'Smart Money' movements.
    Satisfies Requirement: Whale tracking and pool anomaly detection.
    """
    def __init__(self, threshold=2.5):
        self.z_threshold = threshold # Sensitivity for 'weird' movements

    def analyze_flow(self, current_volume, volume_history, whale_threshold_usd=100000):
        """
        Detects if current volume is an anomaly or if a Whale is active.
        """
        alerts = []
        is_anomaly = False
        
        # 1. Whale Tracking: Check if volume exceeds a major threshold
        if current_volume > whale_threshold_usd:
            alerts.append(f"WHALE ALERT: Large movement of ${current_volume} detected.")
            is_anomaly = True

        # 2. Statistical Anomaly: Is this volume 'weird' compared to the past?
        if len(volume_history) > 10:
            mean_vol = np.mean(volume_history)
            std_vol = np.std(volume_history)
            
            # Calculate Z-Score (how many 'standard deviations' away from normal)
            z_score = (current_volume - mean_vol) / (std_vol if std_vol > 0 else 1)
            
            if abs(z_score) > self.z_threshold:
                alerts.append(f"ANOMALY: Volume is {round(z_score, 1)}x outside normal range.")
                is_anomaly = True

        return {
            "is_anomaly": is_anomaly,
            "alerts": alerts,
            "anomaly_score": round(abs(z_score), 2) if 'z_score' in locals() else 0.0
        }

    def check_systemic_correlation(self, sol_price_change, btc_price_change):
        """
        Requirement: Systemic correlation analysis.
        Checks if the whole market is crashing together.
        """
        # If SOL and BTC both drop > 3%, it's a systemic risk
        if sol_price_change < -0.03 and btc_price_change < -0.03:
            return "High Systemic Risk: Market-wide selloff"
        return "Normal Correlation"
