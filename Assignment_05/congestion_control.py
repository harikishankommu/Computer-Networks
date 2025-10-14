import matplotlib.pyplot as plt
import random

def tcp_congestion_control(rounds=30, loss_prob=0.2):
    cwnd = 1
    ssthresh = 8
    cwnd_values = []

    for r in range(rounds):
        cwnd_values.append(cwnd)
        
        # Simulate loss
        if random.random() < loss_prob:
            print(f"Packet loss at round {r}, cwnd={cwnd} → Multiplicative decrease")
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1
            continue

        # Slow Start phase
        if cwnd < ssthresh:
            cwnd *= 2
        else:
            cwnd += 1   # Congestion Avoidance

    # Plot results
    plt.plot(cwnd_values, marker="o")
    plt.title("TCP Congestion Control Simulation")
    plt.xlabel("Transmission Rounds")
    plt.ylabel("Congestion Window (cwnd)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    tcp_congestion_control(rounds=30, loss_prob=0.2)