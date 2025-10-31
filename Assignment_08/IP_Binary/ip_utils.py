# ip_utils.py

def ip_to_binary(ip_address: str) -> str:
    """Convert dotted-decimal IP to 32-bit binary string with clear explanation."""
    print(f"\nConverting IP Address: {ip_address}")
    print("=" * 50)
    
    # Step 1: Split IP into octets
    octets = ip_address.split('.')
    print(f"Step 1: Split into octets -> {octets}")
    
    # Step 2: Convert each octet to 8-bit binary
    binary_octets = []
    for i, octet in enumerate(octets):
        binary_value = format(int(octet), '08b')
        binary_octets.append(binary_value)
        print(f"  Octet {i+1}: {octet} -> {binary_value}")
    
    # Step 3: Join them into a 32-bit binary string
    binary_ip = ''.join(binary_octets)
    print(f"\nStep 3: Combined 32-bit Binary -> {binary_ip}")
    print("=" * 50)
    return binary_ip


def get_network_prefix(ip_cidr: str) -> str:
    """Extract binary network prefix from CIDR notation, showing prefix length."""
    print(f"\nProcessing CIDR: {ip_cidr}")
    print("=" * 50)
    
    ip, prefix_length = ip_cidr.split('/')
    prefix_length = int(prefix_length)
    
    # Convert IP part to binary
    binary_ip = ip_to_binary(ip)
    
    # Get only the prefix bits
    prefix = binary_ip[:prefix_length]
    print(f"\nNetwork Prefix Length: /{prefix_length}")
    print(f"Binary Prefix (first {prefix_length} bits): {prefix}")
    print("=" * 50)
    return prefix


# Quick test
if __name__ == "__main__":
    print("\n--- Example 1 ---")
    ip_to_binary("192.168.1.1")

    print("\n--- Example 2 ---")
    get_network_prefix("200.23.16.0/23")
