import { PrivateKeyGenerator, PublicKeyGenerator } from 'kaspa-wasm';

// Example function to generate private keys from an XPrv
async function generatePrivateKeys(xprv: string, isMultisig: boolean, accountIndex: bigint, cosignerIndex?: number) {
  // Create PrivateKeyGenerator instance
  const privateKeyGen = new PrivateKeyGenerator(xprv, isMultisig, accountIndex, cosignerIndex);

  // Generate receive and change private keys
  const receiveKey = privateKeyGen.receiveKey(0);  // Using index 0 for receive key
  const changeKey = privateKeyGen.changeKey(0);    // Using index 0 for change key

  console.log('Receive Private Key:', receiveKey.toString());
  console.log('Change Private Key:', changeKey.toString());

  // Free up memory
  privateKeyGen.free();
}

// Example function to generate public keys from an XPub
async function generatePublicKeys(xpub: string, isMultisig: boolean, accountIndex: bigint, cosignerIndex?: number) {
  // Create PublicKeyGenerator instance from XPub
  const publicKeyGen = PublicKeyGenerator.fromXPub(xpub, cosignerIndex);

  // Generate receive and change public keys
  const receivePubkey = publicKeyGen.receivePubkey(0);  // Using index 0 for receive key
  const changePubkey = publicKeyGen.changePubkey(0);    // Using index 0 for change key

  console.log('Receive Public Key:', receivePubkey.toString());
  console.log('Change Public Key:', changePubkey.toString());

  // Free up memory
  publicKeyGen.free();
}

// Usage example
const xprv = 'kprv1...';  // Your extended private key here
const xpub = 'kpub1...';  // Your extended public key here
const accountIndex = BigInt(0);  // Use an appropriate account index for your case
const isMultisig = false;  // Set to true if you're using multisig
const cosignerIndex = 0;  // Set if needed for multisig

// Generate private and public keys
generatePrivateKeys(xprv, isMultisig, accountIndex, cosignerIndex);
generatePublicKeys(xpub, isMultisig, accountIndex, cosignerIndex);
