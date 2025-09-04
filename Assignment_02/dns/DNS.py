#  D. DNS
#  • Write a Python program to:
#  1. Resolve the IP address of a given domain name.
#  2. Retrieve different DNS records such as A, MX, and CNAME.
#  3. Log query results into a text file

# DNS query using Python
import dns.resolver

# 1. Input domain
domain = "google.com"

# 2. Open log file
with open("dns_results.txt", "w") as log_file:
    try:
        # A record
        a_records = dns.resolver.resolve(domain, 'A')
        log_file.write(f"A records for {domain}:\n")
        for ip in a_records:
            log_file.write(str(ip) + "\n")
        log_file.write("\n")

        # MX record
        mx_records = dns.resolver.resolve(domain, 'MX')
        log_file.write(f"MX records for {domain}:\n")
        for mx in mx_records:
            log_file.write(str(mx) + "\n")
        log_file.write("\n")

        # CNAME record
        try:
            cname_records = dns.resolver.resolve(domain, 'CNAME')
            log_file.write(f"CNAME records for {domain}:\n")
            for cname in cname_records:
                log_file.write(str(cname) + "\n")
            log_file.write("\n")
        except dns.resolver.NoAnswer:
            log_file.write("No CNAME record found.\n\n")

        print("✅ DNS query completed and results logged into dns_results.txt")

    except Exception as e:
        print("❌ Error:", e)
