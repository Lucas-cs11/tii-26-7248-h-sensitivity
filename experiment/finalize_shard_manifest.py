import hashlib, json, os, sys
from pathlib import Path
shard = int(sys.argv[1])
mf = Path(f"results/shard_manifest_{shard:03d}.json")
out = Path(f"results/complete_fullcov_{shard:03d}.csv.gz")
meta = json.loads(mf.read_text())
if out.exists():
    meta["output_sha256"] = hashlib.sha256(out.read_bytes()).hexdigest()
    meta["output_bytes"] = out.stat().st_size
import csv, gzip
if out.exists():
    rows = list(csv.DictReader(gzip.open(out, "rt")))
    meta["actual_records"] = len(rows)
    meta["timeout_records"] = sum(1 for r in rows if r.get("execution_status") == "TIMEOUT")
    meta["completed_records"] = sum(1 for r in rows if r.get("execution_status") == "COMPLETED")
    keys = [(r["model_id"], r["relative_H_level"]) for r in rows]
    meta["duplicate_combinations"] = len(keys) - len(set(keys))
mf.write_text(json.dumps(meta, indent=1))
print("finalized", shard, meta.get("actual_records"))
