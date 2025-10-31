# router.py
import sys
import os
sys.path.append(os.path.abspath(".."))  # add parent folder to Python path

from IP_Binary.ip_utils import ip_to_binary, get_network_prefix

class Router:
    def __init__(self, routes):
        print("\n================= INITIALIZING ROUTER =================")
        self.forwarding_table = self.build_forwarding_table(routes)
        print("\nFinal Forwarding Table (sorted by prefix length):")
        print("-" * 60)
        for prefix, link in self.forwarding_table:
            print(f"Prefix (/{len(prefix)}): {prefix}  ->  {link}")
        print("========================================================\n")

    def build_forwarding_table(self, routes):
        """Convert human-readable routes into binary prefixes and sort them."""
        table = []
        print("\nBuilding Forwarding Table:")
        print("-" * 60)
        for cidr, link in routes:
            binary_prefix = get_network_prefix(cidr)
            print(f"Route: {cidr}  ->  Binary Prefix: {binary_prefix}  |  Link: {link}")
            table.append((binary_prefix, link))

        # Sort by prefix length (longest first)
        table.sort(key=lambda x: len(x[0]), reverse=True)
        return table

    def route_packet(self, dest_ip: str) -> str:
        """Perform Longest Prefix Match for a given destination IP."""
        print(f"\nRouting packet for destination IP: {dest_ip}")
        print("=" * 60)
        dest_binary = ip_to_binary(dest_ip)
        print(f"Binary of destination IP:\n{dest_binary}")
        print("-" * 60)

        for prefix, link in self.forwarding_table:
            print(f"Checking prefix /{len(prefix)} -> {prefix}")
            if dest_binary.startswith(prefix):
                print(f" Match found! Route through: {link}")
                print("=" * 60)
                return link

        print("No matching prefix found -> Using Default Gateway")
        print("=" * 60)
        return "Default Gateway"

if __name__ == "__main__":
    routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]

    # Initialize the router
    r = Router(routes)

    # Test routing different packets
    print("\n--- TEST 1 ---")
    r.route_packet("223.1.1.100")

    print("\n--- TEST 2 ---")
    r.route_packet("223.1.2.5")

    print("\n--- TEST 3 ---")
    r.route_packet("223.1.250.1")

    print("\n--- TEST 4 ---")
    r.route_packet("198.51.100.1")
