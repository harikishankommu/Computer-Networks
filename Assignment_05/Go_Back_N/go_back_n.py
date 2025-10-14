import random

def go_back_n(total_frames, window_size, loss_prob):
    """Simulates the Go-Back-N protocol."""
    base = 0
    next_frame = 0
    
    while base < total_frames:
        # Send frames in the current window
        end = min(base + window_size, total_frames)
        print(f"Sending frames {list(range(next_frame, end))}")
        
        # Simulate a random frame loss
        lost_frame = None
        for f in range(next_frame, end):
            if random.random() < loss_prob and lost_frame is None:
                lost_frame = f
                print(f"❌ Frame {f} lost, retransmitting from frame {f}")
                break
        
        # If a frame was lost, we go back
        if lost_frame is not None:
            next_frame = lost_frame
        # Otherwise, the transmission was successful
        else:
            print(f"✅ ACK for frame {end - 1} received")
            base = end
            next_frame = base
            print(f"➡️ Window slides to {list(range(base, min(base + window_size, total_frames)))}\n")

if __name__ == "__main__":
    # Get input from the user
    try:
        total_frames_input = int(input("Enter total number of frames to send: "))
        window_size_input = int(input("Enter window size: "))
        loss_prob_input = float(input("Enter frame loss probability (e.g., 0.2 for 20%): "))

        # Run the simulation with user-provided values
        go_back_n(total_frames_input, window_size_input, loss_prob_input)

    except ValueError:
        print("Invalid input. Please enter valid numbers.")