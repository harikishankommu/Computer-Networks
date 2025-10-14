import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def simulate_tcp_congestion_control(total_rounds, initial_ssthresh, loss_round):
    """
    Simulates TCP's cwnd growth and reduction.
    """
    cwnd = 1  # Congestion window starts at 1 MSS
    ssthresh = initial_ssthresh  # Slow Start Threshold
    
    cwnd_history = []
    
    print("Round |   Phase            | CWND | SSTHRESH")
    print("------------------------------------------------")

    for round_num in range(1, total_rounds + 1):
        cwnd_history.append(cwnd)
        
        # --- Check for packet loss ---
        if round_num == loss_round:
            phase = "Packet Loss!"
            print(f"{round_num:<5} | {phase:<18} | {cwnd:<4} | {ssthresh:<8}")
            # Multiplicative Decrease
            ssthresh = cwnd // 2
            cwnd = 1
            continue

        # --- Determine current phase ---
        if cwnd < ssthresh:
            phase = "Slow Start"
            # Exponential Growth: double cwnd for successful ACKs
            cwnd *= 2
        else:
            phase = "Congestion Avoidance"
            # Linear Growth: increment cwnd by 1
            cwnd += 1
            
        print(f"{round_num:<5} | {phase:<18} | {cwnd:<4} | {ssthresh:<8}")
        
    return cwnd_history

def plot_cwnd(rounds, cwnd_data):
    """
    Plots the cwnd size vs. transmission rounds.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(rounds, cwnd_data, marker='o', linestyle='-', label='cwnd')
    plt.title('TCP Congestion Window (cwnd) Simulation')
    plt.xlabel('Transmission Round')
    plt.ylabel('Congestion Window Size (MSS)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rounds)
    
    # Save the plot to a file
    plt.savefig('cwnd_plot.png')
    print("\nPlot saved to cwnd_plot.png")


if __name__ == "__main__":
    # -- Simulation Parameters --
    TOTAL_ROUNDS = 20
    INITIAL_SSTHRESH = 16
    PACKET_LOSS_ROUND = 12 # Simulate packet loss at this round

    # --- Start Simulation ---
    history = simulate_tcp_congestion_control(TOTAL_ROUNDS, INITIAL_SSTHRESH, PACKET_LOSS_ROUND)
    
    # --- Generate Plot ---
    rounds = list(range(1, TOTAL_ROUNDS + 1))
    plot_cwnd(rounds, history)