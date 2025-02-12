from collections import namedtuple
from typing import List
from .module.utils import utils
from .module.curves import ec
from .module.core.schemes import (PrivateKey, BasicSchemeMPL)

Keys = namedtuple('Keys', ['sk', 'pk'])

def keypair_gen_seed(seed: bytes) -> Keys:
    sk: PrivateKey = BasicSchemeMPL.key_gen(seed)
    pk: ec.G1Element = sk.get_g1()

    return Keys(sk, pk)

def keypair_gen_privatekey(private_key: str) -> Keys:
    sk: PrivateKey = utils.import_sk(private_key)
    pk: ec.G1Element = sk.get_g1()

    return Keys(sk, pk)

def sign(sk: PrivateKey, message: str) -> ec.G2Element:
    if not isinstance(sk, PrivateKey):
        raise TypeError("sk must be of type PrivateKey")
    message = utils.to_bytes(message)
    signature: ec.G2Element = BasicSchemeMPL.sign(sk, message)
    return signature

def aggregateKey(pubKey: List[ec.G1Element]) -> ec.G2Element:
    aggKeys: ec.G2Element = BasicSchemeMPL.aggregateKey(pubKey)
    return aggKeys

def aggregateSig(signatures: List[ec.G1Element]) -> ec.G2Element:
    aggKeys: ec.G2Element = BasicSchemeMPL.aggregateSig(signatures)
    return aggKeys

def verify(pk: ec.G1Element, message: str, signature: ec.G2Element) -> bool:
    if not isinstance(pk, ec.G1Element):
        raise TypeError("pk must be of type G1Element")

    if not isinstance(signature, ec.G2Element):
        raise TypeError("signature must be of type G2Element")

    message = utils.to_bytes(message)
    ok: bool = BasicSchemeMPL.verify(pk, message, signature)

    return ok