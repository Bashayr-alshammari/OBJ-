 Excellent — this is the **right moment** to upgrade the repository into a **Q1-journal-grade, reviewer-proof research artifact**.

Below is a **ready-to-paste, journal-grade `README.md`**, written in **academic tone**, aligned with **WoS Q1 expectations**, and consistent with **Objective 1 (HECC + ASCON)**.

You can paste it **directly** into `README.md` and commit.

---

# 🔐 HECC–ASCON Lightweight Security Framework

**Formal Verification and Performance Evaluation (Objective 1)**

---

## 📌 Overview

This repository contains the **complete research artifacts** for **Objective 1** of the PhD project:

> **Design and validation of a lightweight authentication and session-key establishment framework combining HECC and ASCON for resource-constrained IoT/RFID systems.**

The framework targets **pharmaceutical IoT supply-chain environments**, where **low latency**, **low energy consumption**, and **strong cryptographic guarantees** are simultaneously required.

The repository supports **full reproducibility** of:

* Formal security verification
* Performance evaluation
* Experimental benchmarking

---

## 🎯 Research Contributions (Objective 1)

This work makes the following **original contributions**:

1. **Lightweight HECC–ASCON Protocol**

   * Combines **Homomorphic Elliptic Curve Cryptography (HECC)** with **ASCON AEAD**
   * Optimized for **RFID / IoT / edge devices**

2. **Formally Verified Security Properties**

   * Session key secrecy
   * Mutual authentication
   * Agreement and correspondence properties
   * Verified under the **Dolev–Yao adversary model**

3. **Dual Formal Verification**

   * **Tamarin Prover** (symbolic trace-based analysis)
   * **ProVerif** (event-based correspondence and secrecy)

4. **Experimental Performance Evaluation**

   * Computational cost
   * Communication overhead
   * Energy-aware benchmarking
   * Comparative baselines included

---

## 🧠 Threat Model

* **Adversary:** Dolev–Yao attacker
* Full control over the public channel
* Capable of replay, interception, and message injection
* Cannot break cryptographic primitives (symbolic model)

---

## 📂 Repository Structure

```text
hecc-ascon-phd-objective1/
│
├── formal/
│   ├── tamarin/                 # Tamarin Prover models (.spthy)
│   └── proverif/                # ProVerif models (.pv)
│
├── code/
│   └── runner/                  # Protocol simulation / helper scripts
│
├── performance/
│   ├── run_experiment_obj1.py   # Performance experiment driver
│   └── metrics.py               # Time / energy / communication metrics
│
├── data/                        # Raw experiment outputs (CSV)
├── results/                     # Aggregated results and plots
├── scripts/                     # Automation and helper scripts
│
├── tamarin_out.txt              # Formal verification logs
├── requirements.txt             # Python dependencies
├── LICENSE
└── README.md
```

---

## 🔎 Formal Verification

### 1️⃣ Tamarin Prover

* Location: `formal/tamarin/`
* Model: `hecc_ascon_protocol.spthy`

**Verified properties:**

* Session key secrecy
* Authentication (Tag ↔ Reader)
* Freshness and agreement
* Resistance to replay and impersonation

**Run:**

```bash
tamarin-prover formal/tamarin/hecc_ascon_protocol.spthy --bound=5
```

---

### 2️⃣ ProVerif

* Location: `formal/proverif/`
* Model: `hecc_ascon.pv`

**Verified properties:**

* Event-based secrecy of session keys
* Authentication correspondence
* Agreement between Reader and Trusted Authority

**Run:**

```bash
proverif formal/proverif/hecc_ascon.pv
```

---

## ⚙️ Performance Evaluation

### Environment

* Python 3.9+
* Ubuntu 22.04 (WSL2 compatible)
* Resource-constrained simulation settings

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run experiments

```bash
python performance/run_experiment_obj1.py
```

### Metrics collected

* Cryptographic computation time
* Communication overhead (bytes)
* Energy estimation (analytical model)
* Scalability across number of tags

---

## 📊 Reproducibility

All results reported in the associated manuscript can be **fully reproduced** using the scripts provided in this repository.

* No proprietary software required
* No hidden parameters
* Deterministic experiment setup

---

## 🧪 Supported Use Cases

* RFID-based pharmaceutical supply chains
* Lightweight IoT authentication
* Edge-enabled security architectures
* Academic benchmarking and comparison

---

## 📄 Associated Publication

> *Manuscript under preparation / submission to a WoS Q1 journal.*

When published, citation details will be updated here.

---

## 👩‍🎓 Author

**Bashayr Alshammari**
Lecturer at Northern Border University & Ph.D candidate at University Sains Malaysia


Research Areas:

* Lightweight Cryptography
* IoT / RFID Security
* Formal Verification
* Blockchain-enabled Supply Chains

---

## 📜 License

This project is licensed under the **MIT License**.
See `LICENSE` for details.

---



### ✅ Reviewer-Ready Checklist

* ✔ Formal proofs included
* ✔ Performance code provided
* ✔ Reproducible experiments
* ✔ Clear threat model
* ✔ Clean repository structure



