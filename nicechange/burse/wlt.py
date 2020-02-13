from ecdsa import SigningKey, SECP256k1
from bitcoin import *
import sha3
from rlp.utils import decode_hex
keccak = sha3.keccak_256()
priv = "a90670722f8a33dbcd6316866435744e001a0990e57834a86f1de28858a76f64"
pub = encode_pubkey(privtopub(priv), 'bin_electrum')
keccak.update(pub)
address = keccak.hexdigest()[24:]
print("Private key:", priv)
print("Public key: ", pub.hex())
print("Address:     0x" + address)
