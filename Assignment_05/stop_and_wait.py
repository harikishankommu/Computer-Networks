import random, time

def simulate_network(packet, loss_prob):
    if random.random()<loss_prob:
        return None
    return packet

def receiver(recved_frame, exp_seq_num):
    if recved_frame['seq'] == exp_seq_num:
        print(f"Receiver : Frame {recved_frame['data']} (seq : {recved_frame['seq']}) accepted...")
        return {'ack_num' : exp_seq_num}
    else:
        print(f"Receiver : Duplicate Frame {recved_frame['data']} (seq : {recved_frame['seq']}) rejected.../nResending ACK {1-exp_seq_num}")
        return {'ack_num' :1-exp_seq_num}

def sender(frames, loss_prob, timeout):
    seq_num=0
    frame_ind=0
    
    while frame_ind<len(frames):
        frame_to_send={"seq" : seq_num, "data" : frames[frame_ind]}
        
        while True:
            print(f"\n--- Sending Frame {frame_ind} (seq : {seq_num}) ---")
            
            recv=simulate_network(frame_to_send, loss_prob)

            ack=None
            if recv:
                ack=receiver(recv, seq_num)
            
            if ack:
                ack=simulate_network(ack, loss_prob)
            
            time.sleep(timeout)
            
            if ack and ack['ack_num'] == seq_num:
                print(f"ACK {seq_num} received!! Moving to the next frame...")
                frame_ind+=1
                seq_num=1-seq_num
                break
            elif ack and ack['ack_num'] != seq_num:
                print(f"Received ACK {seq_num} is old/duplicate!!! Retransmitting...")
            else:
                print(f"Timeout has occured!!! Retransmitting...")

if __name__ == "__main__":
    f=int(input("Enter total number of frames :"))
    loss_prob=0.30
    timeout=1.0
    
    frames=[f"Data-{i}" for i in range(f)]
    sender(frames, loss_prob, timeout)
    print("\n\t\t\t\t\t\t\t\t--- All the frames have been successfully transmitted ---\n\n\t\t\t\t\t\t\t\t\t\tEND OF SIMULATION")