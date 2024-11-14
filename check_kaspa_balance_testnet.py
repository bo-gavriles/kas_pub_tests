import requests

def check_kaspa_balance(address):
    """Checks the balance of a given Kaspa testnet address."""
    url = f"https://api-tn11.kaspa.org/addresses/{address}/balance"
    
    try:
        response = requests.get(url)
        
        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            balance = data.get('balance', 0)
            print(f"Balance for address {address}: {balance} TKAS")
        elif response.status_code == 404:
            print(f"Address {address} has no transactions or does not exist in the blockchain.")
        else:
            print(f"Error fetching balance for address {address}: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Network error: {e}")

# Example Kaspa testnet prefix
kaspa_address = "kaspatest:"address)"

# Check balance
check_kaspa_balance(kaspa_address)
