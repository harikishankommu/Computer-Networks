import random
import time

def sender(total_frames, window_size, loss_prob, timeout):
    
    base = 0
    next_seq_num = 0
    frames = [f"Frame-{i}" for i in range(total_frames)]
    
    while base < total_frames:
    
        while next_seq_num < base + window_size and next_seq_num < total_frames:
            print(f"Sending {frames[next_seq_num]} (Seq: {next_seq_num})...")
            
            next_seq_num += 1
        
  
        start_time = time.time()
        ack_received = -1 
        
        ack_received = receiver(base, next_seq_num - 1, frames, loss_prob)

        while time.time() - start_time < timeout:
            if ack_received >= base:
                print(f"Cumulative ACK {ack_received} received.")
                base = ack_received + 1
                break
        
        if ack_received < base:
            print(f"\nTimeout! Expected ACK for frame {base}. Retransmitting window.")
            next_seq_num = base
            time.sleep(1)

    print("\n\t\t\t\t\t\t\t\t--- All the frames have been successfully transmitted ---\n\n\t\t\t\t\t\t\t\t\t\tEND OF SIMULATION")


def receiver(base, last_sent, frames, loss_prob):

    expected_frame = base
    
    for i in range(base, last_sent + 1):

        if random.random() < loss_prob:
            print(f"NETWORK: {frames[i]} was lost!!!")

            return expected_frame - 1

        print(f"Receiver: Received {frames[i]} correctly...")
        expected_frame += 1

    return last_sent


if __name__ == "__main__":

    TOTAL_FRAMES = int(input("Enter number of Frames : "))
    WINDOW_SIZE = int(input("Enter Window Size : "))
    LOSS_PROBABILITY = 0.2  
    TIMEOUT = 2.0          

    sender(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROBABILITY, TIMEOUT)