# scheduler.py

from dataclasses import dataclass
from typing import List


# -----------------------------------------------------
# 1️⃣ Packet Class
# -----------------------------------------------------
@dataclass
class Packet:
    source_ip: str
    dest_ip: str
    payload: str
    priority: int  # 0=High, 1=Medium, 2=Low


# -----------------------------------------------------
# 2️⃣ FIFO Scheduler
# -----------------------------------------------------
def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    Simulate First-Come, First-Served scheduling.
    Packets are sent in the order they arrived.
    """
    print("\n FIFO (First-Come-First-Served) Scheduling Simulation ")
    print("-" * 55)
    print("Arrival Order:")
    for i, pkt in enumerate(packet_list, start=1):
        print(f"{i}. {pkt.payload} (Priority: {pkt.priority})")

    print("\nTransmission Order (Same as Arrival):")
    for i, pkt in enumerate(packet_list, start=1):
        print(f"{i}. {pkt.payload} -> Sent")

    print("-" * 55)
    return packet_list


# -----------------------------------------------------
# 3️⃣ Priority Scheduler
# -----------------------------------------------------
def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    Simulate Priority Scheduling.
    Packets with lower priority number are sent first.
    """
    print("\n Priority Scheduling Simulation ")
    print("-" * 55)
    print("Before Scheduling:")
    for i, pkt in enumerate(packet_list, start=1):
        print(f"{i}. {pkt.payload} (Priority: {pkt.priority})")

    # Sort packets based on priority (0 first)
    sorted_packets = sorted(packet_list, key=lambda pkt: pkt.priority)

    print("\nTransmission Order (High -> Low Priority):")
    for i, pkt in enumerate(sorted_packets, start=1):
        priority_name = ["High", "Medium", "Low"][pkt.priority]
        print(f"{i}. {pkt.payload} -> Sent ({priority_name} Priority)")

    print("-" * 55)
    return sorted_packets


# -----------------------------------------------------
# 4️⃣ Test the schedulers
# -----------------------------------------------------
if __name__ == "__main__":
    packets = [
        Packet("10.0.0.1", "10.0.0.2", "Data Packet 1", 2),
        Packet("10.0.0.3", "10.0.0.4", "Data Packet 2", 2),
        Packet("10.0.0.5", "10.0.0.6", "VOIP Packet 1", 0),
        Packet("10.0.0.7", "10.0.0.8", "Video Packet 1", 1),
        Packet("10.0.0.9", "10.0.0.10", "VOIP Packet 2", 0),
    ]

    fifo_result = fifo_scheduler(packets)
    priority_result = priority_scheduler(packets)

    # ✅ For verification
    print("\n FIFO Result Order:", [p.payload for p in fifo_result])
    print(" Priority Result Order:", [p.payload for p in priority_result])
