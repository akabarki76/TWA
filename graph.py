# time_attack_game/graph.py
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Tuple

def plot_attack_results(
    timing_data: Dict[int, float],
    cracked_credentials: Tuple[int, str] = None,
    threshold: float = None
):
    """
    Visualizes timing attack results with enhanced annotations.
    
    Args:
        timing_data: Dictionary of {user_id: response_time}
        cracked_credentials: Tuple of (user_id, pin) if found
        threshold: Optional horizontal line showing detection threshold
    """
    plt.figure(figsize=(12, 6))
    
    # Convert to sorted lists
    user_ids = sorted(timing_data.keys())
    times = [timing_data[uid] for uid in user_ids]
    
    # Create bar plot
    bars = plt.bar(user_ids, times, width=20, alpha=0.7)
    
    # Highlight vulnerable users
    mean_time = np.mean(times)
    std_dev = np.std(times)
    vulnerable_color = '#ff7f0e'
    
    for i, (uid, t) in enumerate(zip(user_ids, times)):
        if t > mean_time + 2*std_dev:  # Statistical outlier
            bars[i].set_color(vulnerable_color)
    
    # Add annotations if credentials were cracked
    if cracked_credentials:
        user_id, pin = cracked_credentials
        plt.annotate(
            f'CRACKED\nUser: {user_id}\nPIN: {pin}',
            xy=(user_id, timing_data[user_id]),
            xytext=(10, 30),
            textcoords='offset points',
            arrowprops=dict(arrowstyle='->'),
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5)
        )
    
    # Add threshold line if provided
    if threshold:
        plt.axhline(
            y=threshold,
            color='r',
            linestyle='--',
            label=f'Detection Threshold ({threshold:.4f}s)'
        )
    
    # Customize plot
    plt.xlabel('User ID', fontsize=12)
    plt.ylabel('Response Time (seconds)', fontsize=12)
    plt.title('Timing Attack Analysis\n', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save and show
    plt.tight_layout()
    plt.savefig('timing_attack_results.png', dpi=300)
    plt.show()

def generate_sample_data():
    """Creates mock data for demonstration"""
    # Simulate normal response times (~0.1-0.3s)
    data = {uid: np.random.uniform(0.1, 0.3) for uid in range(1000, 1100)}
    
    # Add vulnerable user with longer response (~1.5s)
    vulnerable_id = 1057
    data[vulnerable_id] = 1.5 + np.random.uniform(-0.2, 0.2)
    
    return data, (vulnerable_id, "84637291")

if __name__ == "__main__":
    # Demo mode with sample data
    print("Generating sample timing attack visualization...")
    sample_data, sample_creds = generate_sample_data()
    plot_attack_results(
        timing_data=sample_data,
        cracked_credentials=sample_creds,
        threshold=0.5  # Example threshold
    )
