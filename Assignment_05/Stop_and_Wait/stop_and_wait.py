import random
import time

def stop_and_wait(total_frames, loss_prob, timeout):
    """Simulates the Stop-and-Wait protocol."""
    frame = 0
    while frame < total_frames:
        print(f"Sending Frame {frame}...")
        time.sleep(1)

        # Simulate a random frame loss
        if random.random() < loss_prob:
            print(f"❌ Frame {frame} lost! Timeout started...")
            time.sleep(timeout)
            print(f"⏰ Timeout over. Retransmitting Frame {frame}.\n")
            continue # Go back to the start of the loop to resend the same frame

        # If no loss, ACK is received
        print(f"✅ ACK for frame {frame} received.\n")
        frame += 1 # Move to the next frame

if __name__ == "__main__":
    # Get input from the user
    try:
        total_frames_input = int(input("Enter total number of frames to send: "))
        loss_prob_input = float(input("Enter frame loss probability (e.g., 0.3 for 30%): "))
        timeout_input = int(input("Enter timeout duration in seconds (e.g., 2): "))

        print("\n--- Starting Stop-and-Wait Simulation ---\n")
        # Run the simulation with user-provided values
        stop_and_wait(total_frames_input, loss_prob_input, timeout_input)
        print("\n--- Simulation Complete ---")

    except ValueError:
        print("\nError: Invalid input. Please enter valid numbers.")