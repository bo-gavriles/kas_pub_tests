import os
import ecdsa
import bech32

class KaspaAddress:
    def __init__(self, network_prefix, version, public_key):
        self.network_prefix = network_prefix  # Префикс без двоеточия
        self.version = version
        self.public_key = public_key
        self.address_string = self._generate_address()

    def _convert_bits(self, data, from_bits, to_bits, pad=True):
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

    def _generate_checksum(self, data):
        """Generate a checksum for the Bech32 encoded address."""
        return bech32.bech32_create_checksum(self.network_prefix, data)

    def _generate_address(self):
        """Generates the Kaspa address in Bech32 format with checksum."""
        # Combine version and public key
        versioned_public_key = bytes([self.version]) + self.public_key
        payload_bits = self._convert_bits(versioned_public_key, 8, 5)

        if payload_bits is None:
            raise ValueError("Error converting public key and version to 5-bit format.")

        # Add checksum to payload
        checksum = self._generate_checksum(payload_bits)
        full_payload = payload_bits + checksum

        # Encode to Bech32 address
        address = bech32.bech32_encode(self.network_prefix, full_payload)

        return address

    @classmethod
    def generate(cls, network_prefix="kaspatest", version=0x01):
        """Generates a new Kaspa address with a new private key."""
        private_key = os.urandom(32)
        
        # Generate public key
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        
        # Compress public key (33 bytes) for ECDSA
        public_key = b'\x02' + vk.to_string()[:32] if vk.to_string()[32] < 128 else b'\x03' + vk.to_string()[:32]
        
        return cls(network_prefix, version, public_key), private_key.hex()

# Example usage:
address, private_key = KaspaAddress.generate()
print("Generated Kaspa Address:", address.address_string)
print("Private Key (Hex):", private_key)
