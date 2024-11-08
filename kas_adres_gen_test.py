import ecdsa
import os
import requests
import bech32  # Ensure you have installed bech32: pip install bech32

def generate_private_key():
    """Generates a new ECDSA private key for secp256k1."""
    return os.urandom(32)

def private_key_to_public_key_ecds(signature_type, private_key):
    """Generates a compressed ECDSA public key (33 bytes) from the private key."""
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    
    # ECDSA: Compress the public key to 33 bytes with parity flag
    if signature_type == 'ecdsa':
        public_key = b'\x02' + vk.to_string()[:32] if vk.to_string()[32] < 128 else b'\x03' + vk.to_string()[:32]
    # Schnorr: Compress to 32 bytes (no parity flag)
    elif signature_type == 'schnorr':
        public_key = vk.to_string()[:32]  # No parity flag for Schnorr
    else:
        raise ValueError("Invalid signature type. Use 'ecdsa' or 'schnorr'.")
    
    return public_key

def convert_bits(data, from_bits, to_bits, pad=True):
    """Converts byte array from one bit size to another (for Bech32 encoding)."""
    acc = 0
    bits = 0
    result = []
    maxv = (1 << to_bits) - 1
    max_acc = (1 << (from_bits + to_bits - 1)) - 1
    for value in data:
        if (value < 0) or (value >> from_bits):
            return None
        acc = ((acc << from_bits) | value) & max_acc
        bits += from_bits
        while bits >= to_bits:
            bits -= to_bits
            result.append((acc >> bits) & maxv)
    if pad:
        if bits:
            result.append((acc << (to_bits - bits)) & maxv)
    elif bits >= from_bits or ((acc << (to_bits - bits)) & maxv):
        return None
    return result

def public_key_to_address(public_key):
    """Generates a Kaspa address from the public key using Bech32 encoding."""
    # Convert public key bytes to 5-bit array for Bech32 encoding
    public_key_5bit = convert_bits(public_key, 8, 5)
    if public_key_5bit is None:
        raise ValueError("Error converting public key to 5-bit format for Bech32 encoding.")
    
    # Encode with Bech32 using 'kaspatest' prefix
    address = bech32.bech32_encode('kaspatest', public_key_5bit)
    
    # Fix address format to start with 'kaspatest:' instead of 'kaspatest1'
    address = address.replace('kaspatest1', 'kaspatest:', 1)
    
    return address

def get_balance(kaspa_address):
    """Check the balance of a given Kaspa address."""
    url = f"https://api-tn11.kaspa.org/v2/address/{kaspa_address}/balance"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        balance = data.get('balance', 0)
        print(f"Balance for address {kaspa_address}: {balance} TKAS")
    elif response.status_code == 404:
        print(f"Address {kaspa_address} has no transactions or does not exist in the blockchain.")
    else:
        print(f"Error fetching balance for address {kaspa_address}: {response.status_code}")

def generate_kaspa_address(signature_type='ecdsa'):
    """Generates and prints a new Kaspa address and private key, and checks the balance."""
    private_key = generate_private_key()
    public_key = private_key_to_public_key_ecds(signature_type, private_key)
    
    # Convert private key to hexadecimal format for readability
    private_key_hex = private_key.hex()
    kaspa_address = public_key_to_address(public_key)
    
    # Output the private key and address
    print("Generated Private Key (Hex):", private_key_hex)
    print(f"New Kaspa Testnet Address (Signature type: {signature_type}):", kaspa_address)
    
    # Check the balance of the generated address
    get_balance(kaspa_address)

# Generate a new Kaspa testnet address and private key on each run and check balance
# You can call it like generate_kaspa_address('ecdsa') or generate_kaspa_address('schnorr')
generate_kaspa_address('ecdsa')  # or 'schnorr' depending on the desired signature type
