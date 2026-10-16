# RailGov Enterprise Dataset Card & Provenance Specification

## 1. Dataset Overview & Scope
This Data Card provides exhaustive provenance, schema definitions, statistical distributions, synthetic generation methodology, and ethical constraints for all datasets utilized across the RailGov Enterprise AI ecosystem.

| Dataset Identifier | Physical Path | Primary File Format | Record Count | Primary Consumer Microservices |
|---|---|---|---|---|
| **Fare History Ledger** | `datasets/historical_fares.csv` | CSV | 6,000 rows | `fare-predictor` |
| **Railway Trunk Network** | `datasets/trains.json` | JSON | 8 Primary Trains | `planner-agent`, `recommender` |
| **Station Master Catalog** | `datasets/stations.json` | JSON | 10 Major Junctions | `delay-predictor`, `health-monitor` |
| **Waitlist Confirmation Ledger** | `datasets/waitlist_training.csv` | CSV | 2,500 rows | `wl-predictor`, `lifecycle-manager` |
| **Support Policy Corpus** | `services/support-assistant/rag.py` | Embedded Document JSON | 6 Master Policies | `support-assistant` |

---

## 2. Dataset Specifics & Provenance

### A. Historical Fares (`datasets/historical_fares.csv`)
- **Origin & Purpose**: Generated to model Indian Railways dynamic pricing (Premium Tatkal and Dynamic Surge Pricing schemes) across 6 trunk routes and 6 travel classes.
- **Record Volume**: 6,000 records.
- **Corridors Covered**:
  1. Pune Junction (`PUNE`) $\leftrightarrow$ Delhi Hazrat Nizamuddin (`DLI` / `NZM`) [1,520 km]
  2. Mumbai Central (`BCT`) $\leftrightarrow$ New Delhi (`NDLS`) [1,384 km]
  3. Patna Junction (`PNBE`) $\leftrightarrow$ New Delhi (`NDLS`) [998 km]
  4. New Delhi (`NDLS`) $\leftrightarrow$ Varanasi Junction (`BSB`) [757 km]
  5. Chennai Central (`MAS`) $\leftrightarrow$ Bengaluru City (`SBC`) [362 km]
  6. Howrah Junction (`HWH`) $\leftrightarrow$ New Delhi (`NDLS`) [1,447 km]
- **Classes**: `SL` (Sleeper), `CC` (AC Chair Car), `3A` (AC 3 Tier), `2A` (AC 2 Tier), `1A` (AC 1st Class), `EC` (Executive Chair Car).
- **Features**: `origin`, `destination`, `travel_class`, `days_to_departure` (0 to 120), `base_fare`, `final_fare`, `demand_index` (0.2 to 2.8), `tatkal_flag`.
- **Validation Split**: 80% Training (4,800 rows), 20% Held-Out Out-of-Time Test (1,200 rows).

### B. Waitlist Confirmation History (`datasets/waitlist_training.csv`)
- **Origin & Purpose**: Real-world calibrated waitlist progression and chart preparation outcomes based on IRCTC historical charting distributions.
- **Features**: `train_no`, `travel_class`, `quota` (`GN`, `TQ`, `LD`, `DF`), `wl_position` (1 to 150), `days_to_departure` (1 to 60), `cancellation_rate`, `historical_confirmation_rate`, `confirmed` (binary ground truth: 0 or 1).
- **Class Balance**: 63.8% Confirmed, 36.2% Waitlisted/Dropped.

### C. Station Master & Congestion Catalog (`datasets/stations.json`)
- **Origin & Purpose**: Models physical terminal constraints across major Indian Railway hubs.
- **Attributes**: Station code, name, platform count, base congestion index, terminal throughput limits, connecting railway zones (CR, NR, WR, ECR, ER, SR, SWR).

---

## 3. Synthetic Data Realism & Mitigation of Artefacts
1. **Physical Railway Invariant Enforcement**:
   - Class ordering invariant: Fare($\text{SL}$) < Fare($\text{3A}$) < Fare($\text{2A}$) < Fare($\text{1A}$).
   - Distance scaling: Fare increases monotonically with corridor distance.
   - Surge dynamics: Surges strictly follow the official IRCTC Dynamic Fare Rules (maximum 1.50x cap on base fare for AC classes, zero surge for Sleeper non-tatkal).
2. **Deterministic Seed Control**:
   - Random state fixed at `SEED = 42` for all data generation scripts to guarantee bit-for-bit reproducible evaluation.
3. **Absence of Synthetic Hallucinations**:
   - No imaginary station codes (only verified IR codes: `PUNE`, `DLI`, `NDLS`, `BCT`, `PNBE`, `BSB`, `MAS`, `SBC`, `HWH`, `CNB`, `MMR`).
   - Train numbers correspond to real Indian Railways superfast and express services (e.g. 12149 Pune-Danapur Superfast Express).

---

## 4. Ethical & Fair AI Considerations
- **PII Compliance**: Zero real passenger names, phone numbers, or Aadhaar identities are stored. Any sample references use standardized masking (`R**** S****`, `******4521`).
- **Quota Equality**: Model predictions are audited using the Four-Fifths Disparate Impact rule across quota dimensions (`GN`, `TQ`, `LD`) to ensure algorithmic fairness.

---

## 5. Licensing & Permitted Use
- **License**: Apache 2.0 Enterprise Open Source.
- **Intended Use**: Academic benchmarks, architectural evaluation, system integration, and production readiness audits.
