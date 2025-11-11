import hashlib, time, json
from nacl.signing import SigningKey

signing_key = SigningKey.generate()

def generate_timestamp(data: bytes) -> str:
    entropy = str(time.time()).encode()
    payload = data + entropy
    digest = hashlib.sha3_512(payload).hexdigest()
    signature = signing_key.sign(digest.encode()).signature.hex()
    return f"{digest}:{signature}"

def compress_lineage(data: bytes, timestamp: str) -> str:
    return hashlib.blake2b(data + timestamp.encode()).hexdigest()

def opentimestamp_anchor(data_hash: str) -> dict:
    anchored_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    anchor_hash = hashlib.sha256((data_hash + anchored_time).encode()).hexdigest()
    return {"ots_anchor": anchor_hash, "anchored_at": anchored_time}

ledger = []

def anchor_artifact(data: bytes, timestamp: str, lineage: str):
    data_hash = hashlib.sha256(data).hexdigest()
    ots = opentimestamp_anchor(data_hash)
    entry = {
        "timestamp": timestamp,
        "lineage": lineage,
        "data_hash": data_hash,
        "ots_anchor": ots["ots_anchor"],
        "anchored_at": ots["anchored_at"]
    }
    ledger.append(entry)
    return entry

def license_artifact(entry: dict, license_id: str) -> dict:
    symbolic_signature = hashlib.sha3_256((entry["data_hash"] + license_id).encode()).hexdigest()
    entry["license_id"] = license_id
    entry["symbolic_signature"] = symbolic_signature
    return entry

def apply_symbolic_overlay(entry: dict, archetype: str):
    overlay_hash = hashlib.blake2b((entry["lineage"] + archetype).encode()).hexdigest()
    entry["symbolic_overlay"] = {"archetype": archetype, "overlay_hash": overlay_hash}
    return entry


