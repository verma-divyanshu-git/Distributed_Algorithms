# Suzuki-Kasami Broadcast Algorithm for Mutual Exclusion in Python
class SuzukiKasami:
    def __init__(self, num_sites):
        self.num_sites = num_sites
        self.RN = [0] * num_sites  # Request number array for each site
        self.LN = [0] * num_sites  # Last executed request number for each site
        self.token = {'LN': [0] * num_sites, 'queue': []}  # Token data structure
        self.has_token = False  # Indicates if the site has the token

    def request_critical_section(self, site_id):
        if self.has_token:
            print(f"Site {site_id} already has the token and can enter the critical section.")
            self.enter_critical_section(site_id)
        else:
            # Increment request number and send request to all other sites
            self.RN[site_id] += 1
            print(f"Site {site_id} requests access to critical section with request number {self.RN[site_id]}.")
            for i in range(self.num_sites):
                if i != site_id:
                    print(f"Site {site_id} sends REQUEST({site_id}, {self.RN[site_id]}) to Site {i}.")
            # Simulate receiving the token if the conditions are met
            if self.check_token_condition(site_id):
                self.receive_token(site_id)

    def receive_request(self, from_site, request_number):
        self.RN[from_site] = max(self.RN[from_site], request_number)
        print(f"Site receives REQUEST({from_site}, {request_number}). Updated RN[{from_site}] to {self.RN[from_site]}.")
        # If site has the token and the request is pending, send the token
        if self.has_token and self.RN[from_site] == self.token['LN'][from_site] + 1:
            self.send_token(from_site)

    def check_token_condition(self, site_id):
        # This function checks if the site can receive the token
        return all(self.RN[i] <= self.token['LN'][i] + 1 for i in range(self.num_sites))

    def receive_token(self, site_id):
        print(f"Site {site_id} receives the token.")
        self.has_token = True
        self.enter_critical_section(site_id)

    def enter_critical_section(self, site_id):
        print(f"Site {site_id} is entering the critical section.")
        # Execute the critical section
        print(f"Site {site_id} is executing the critical section.")
        # Exit the critical section
        self.exit_critical_section(site_id)

    def exit_critical_section(self, site_id):
        print(f"Site {site_id} is exiting the critical section.")
        self.token['LN'][site_id] = self.RN[site_id]
        print(f"Updated LN[{site_id}] to {self.token['LN'][site_id]}.")
        # Send the token to the next waiting site if any
        if self.token['queue']:
            next_site = self.token['queue'].pop(0)
            self.send_token(next_site)
        else:
            print(f"Site {site_id} retains the token.")

    def send_token(self, to_site):
        print(f"Sending token to Site {to_site}.")
        self.has_token = False
        # Transfer token to the requested site
        self.receive_token(to_site)

# Example Usage
num_sites = 3
suzuki_kasami = SuzukiKasami(num_sites)

# Simulate requests from different sites
suzuki_kasami.request_critical_section(0)
suzuki_kasami.receive_request(1, 1)
suzuki_kasami.request_critical_section(1)
suzuki_kasami.receive_request(2, 1)
suzuki_kasami.request_critical_section(2)