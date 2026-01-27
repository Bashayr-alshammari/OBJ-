import os, time, csv, uuid, random, json, threading, subprocess
from pathlib import Path
import psutil

# ---- Placeholder crypto API (you will plug your ASCON + HECC here) ----
# For now, we simulate crypto cost with small sleep; replace with real calls.
def hecc_key_exchange():
    t0 = time.perf_counter()
    # TODO: replace with real HECC E-E exchange
    time.sleep(0.003)  # ~3ms placeholder
    return (time.perf_counter() - t0) * 1000.0, os.urandom(16)

def ascon_encrypt(key: bytes, nonce: bytes, aad: bytes, msg: bytes):
    t0 = time.perf_counter()
    # TODO: replace with real ASCON-128a AEAD
    time.sleep(0.001)  # ~1ms placeholder
    ct = msg  # placeholder
    tag = b"\x00"*16
    return (time.perf_counter() - t0) * 1000.0, ct, tag

def ascon_decrypt(key: bytes, nonce: bytes, aad: bytes, ct: bytes, tag: bytes):
    t0 = time.perf_counter()
    # TODO: replace with real ASCON-128a AEAD
    time.sleep(0.001)  # ~1ms placeholder
    ok = True
    msg = ct
    return (time.perf_counter() - t0) * 1000.0, ok, msg
# ---------------------------------------------------------------------

def cpu_mem():
    return psutil.cpu_percent(interval=None), psutil.virtual_memory().used / (1024*1024)

def monotonic_nonce(counter: int) -> bytes:
    return counter.to_bytes(16, "big")

def random_nonce() -> bytes:
    return os.urandom(16)

def list_payloads(payload_dir: Path, kb: int):
    return sorted(payload_dir.glob(f"payload_{kb}kb_*.json"))

def worker(thread_id, jobs, out_rows, scenario, nonce_policy, tag_uid, reader_id):
    # 1 HECC exchange per "session"
    kx_ms, key = hecc_key_exchange()
    nonce_ctr = 0

    for payload_path in jobs:
        msg = payload_path.read_bytes()
        aad = f"{tag_uid}|{reader_id}".encode()

        if nonce_policy == "counter":
            nonce = monotonic_nonce(nonce_ctr); nonce_ctr += 1
        else:
            nonce = random_nonce()

        t0 = time.perf_counter()
        enc_ms, ct, tag = ascon_encrypt(key, nonce, aad, msg)
        dec_ms, ok, _ = ascon_decrypt(key, nonce, aad, ct, tag)
        e2e_ms = (time.perf_counter() - t0) * 1000.0

        cpu_pct, mem_mb = cpu_mem()

        out_rows.append({
            "file_id": str(uuid.uuid4())[:8],
            "device_id": "D-GW01",
            "reader_id": reader_id,
            "tag_uid": tag_uid,
            "attack_scenario": scenario,
            "enc_algo": "HECC+ASCON-128a",
            "hecc_kx_ms": round(kx_ms, 3),
            "enc_latency_ms": round(enc_ms, 3),
            "dec_latency_ms": round(dec_ms, 3),
            "e2e_latency_ms": round(e2e_ms, 3),
            "cpu_pct": round(cpu_pct, 2),
            "mem_mb": round(mem_mb, 2),
            "encryption_success": "Yes" if ok else "No",
            "ts_scan": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        })

def run_cell(sizes_kb, scenario, concurrency, runs_per_cell, nonce_policy, out_csv):
    payload_dir = Path("data/payloads")
    tag_uid = "T-0001"          # replace with real tag UID if available
    reader_id = "RDR-ISO15693"  # replace with your reader id

    rows = []
    for kb in sizes_kb:
        payloads = list_payloads(payload_dir, kb)
        if not payloads:
            raise RuntimeError(f"No payloads for {kb}KB")

        # Build job list for this cell (sample with replacement)
        jobs = [random.choice(payloads) for _ in range(runs_per_cell)]
        # Split jobs across threads
        chunks = [jobs[i::concurrency] for i in range(concurrency)]
        threads = []
        shared = []
        lock = threading.Lock()

        def runner(chunk, tid):
            local = []
            worker(tid, chunk, local, scenario, nonce_policy, tag_uid, reader_id)
            with lock:
                shared.extend(local)

        for tid, chunk in enumerate(chunks):
            t = threading.Thread(target=runner, args=(chunk, tid), daemon=True)
            threads.append(t); t.start()
        for t in threads:
            t.join()

        rows.extend(shared)

    # Write CSV
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

if __name__ == "__main__":
    import yaml
    cfg = yaml.safe_load(Path("configs/experiment.yaml").read_text())
    out_dir = Path(cfg["output_dir"])

    for scenario in cfg["scenarios"]:
        for conc in cfg["concurrency"]:
            out_csv = out_dir / f"rfid_events_{scenario}_c{conc}.csv"
            run_cell(cfg["sizes_kb"], scenario, conc, cfg["runs_per_cell"], cfg["nonce_policy"], out_csv)
            print("Wrote:", out_csv)
