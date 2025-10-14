import matplotlib.pyplot as plt
import random

def tcp_congestion_control(rounds, loss_prob):
    """Simulates TCP Congestion Control and plots cwnd vs. ssthresh."""
    cwnd = 1
    ssthresh = 16  # Initial threshold, you can make this a user input too
    
    # Lists to store values for plotting
    cwnd_values = []
    ssthresh_values = [] # New: list to track the threshold

    print("\n--- Starting TCP Congestion Control Simulation ---")
    
    for r in range(rounds):
        # Store current values before any changes
        cwnd_values.append(cwnd)
        ssthresh_values.append(ssthresh)

        # Simulate a random packet loss
        if random.random() < loss_prob:
            print(f"Round {r+1}: ❌ Packet loss occurred! (cwnd={cwnd})")
            # Multiplicative Decrease
            ssthresh = max(cwnd // 2, 1)  # ssthresh is halved
            cwnd = 1                      # cwnd resets to 1 (goes back to Slow Start)
            print(f"           -> ssthresh set to {ssthresh}, cwnd resets to {cwnd}\n")
            continue

        # If no loss, grow the congestion window
        if cwnd < ssthresh:
            # Slow Start phase: Exponential growth
            print(f"Round {r+1}: Slow Start (cwnd={cwnd} -> {cwnd*2})")
            cwnd *= 2
        else:
            # Congestion Avoidance phase: Linear growth
            print(f"Round {r+1}: Congestion Avoidance (cwnd={cwnd} -> {cwnd+1})")
            cwnd += 1
            
    # --- Plotting Section ---
    plt.figure(figsize=(12, 6))
    
    # Plot Congestion Window (cwnd)
    plt.plot(range(1, rounds + 1), cwnd_values, marker='o', linestyle='-', color='blue', label='Congestion Window (cwnd)')
    
    # New: Plot Threshold (ssthresh) in red
    plt.plot(range(1, rounds + 1), ssthresh_values, linestyle='--', color='red', label='Threshold (ssthresh)')
    
    plt.title("TCP Congestion Control Simulation")
    plt.xlabel("Transmission Round")
    plt.ylabel("Window Size")
    plt.xticks(range(1, rounds + 1))
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    try:
        rounds_input = int(input("Enter total number of transmission rounds: "))
        loss_prob_input = float(input("Enter packet loss probability (e.g., 0.1 for 10%): "))

        tcp_congestion_control(rounds_input, loss_prob_input)

    except ValueError:
        print("\nError: Invalid input. Please enter valid numbers.")