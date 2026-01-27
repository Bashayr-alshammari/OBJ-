#!/usr/bin/env bash
set -euo pipefail
SANDBOX="${1:-data/sandbox}"
mkdir -p "$SANDBOX"

# Create files
for i in $(seq 1 2000); do
  head -c 2048 </dev/urandom > "$SANDBOX/f_$i.bin"
done

# Chaos loop (rename/copy/delete) - SAFE
for r in $(seq 1 200); do
  for i in $(seq 1 2000); do
    mv "$SANDBOX/f_$i.bin" "$SANDBOX/f_$i.$r.bin" 2>/dev/null || true
    cp "$SANDBOX/f_$i.$r.bin" "$SANDBOX/c_$i.$r.bin" 2>/dev/null || true
    rm -f "$SANDBOX/c_$i.$r.bin" 2>/dev/null || true
  done
done
