# RailGov Enterprise Architecture: 10M+ Daily Passenger Interactions Scaling Note

## 1. System Scale Target & Concurrency Profile
- **Daily Active Passengers**: 10,000,000+ interactions per day
- **Tatkal Surge Spike Window**: 10:00 AM – 10:15 AM (AC) & 11:00 AM – 11:15 AM (Non-AC)
- **Peak Throughput Target**: 45,000 to 60,000 requests per second (RPS)
- **Steady-State Throughput**: 1,200 to 2,500 RPS
- **P95 Latency SLA**: < 100 ms for tabular ML predictions, < 250 ms for RAG inquiries

---

## 2. Distributed Architecture Topology

```
[ Edge Tier: Cloudflare Anycast CDN + WAF + Geo-DNS ]
                           │
             [ Layer 7 Ingress Gateway / Envoy Proxy ]
             (Rate Limiting, mTLS, JWT & RBAC Auth, PII Sanitization)
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
[ Region 1: Mumbai ]  [ Region 2: Delhi ]  [ Region 3: Kolkata ]
 (Primary West)        (Primary North)      (Disaster Recovery East)
       │
   Kubernetes Cluster (EKS / GKE / On-Premise IR Cloud)
   ├── Horizontal Pod Autoscaler (HPA: CPU > 65%, Custom Metric: RPS)
   ├── Microservice Fleet:
   │   ├── WL Predictor Pods (ONNX Runtime / C++ Engine)
   │   ├── Fare Dynamic Engine Pods
   │   ├── Delay & Congestion Multi-Stage Pods
   │   ├── Semantic Multilingual Support Assistant Pods
   │   └── Travel Planner Agent (Bounded ReAct with Circuit Breaker)
   │
   ├── High-Speed Cache Tier: Redis Enterprise Cluster (32 Shards)
   │   ├── Route Base Fare & Schedule Caches (TTL: 1 hour)
   │   ├── Real-time Train Status Caches (TTL: 30 seconds)
   │   └── Top 100 Route WL Estimates (TTL: 60 seconds)
   │
   ├── Asynchronous Telemetry & Event Ingestion: Apache Kafka (3-AZ Replication)
   │   ├── Topic: `passenger.inferences` (Partitions: 64)
   │   ├── Topic: `governance.audit_events` (Partitions: 32)
   │   └── Topic: `model.drift_telemetry` (Partitions: 16)
   │
   └── Distributed Storage & Ledger Tier:
       ├── Immutable Cryptographic Audit Store: Append-only distributed object storage (S3/GCS) + QLDB
       ├── Primary Relational Data: CockroachDB / Distributed PostgreSQL
       └── Telemetry Time-Series: ClickHouse (100,000+ writes/sec ingestion)
```

---

## 3. Core Architectural Mechanisms for Massive Scale

### A. Peak Tatkal Surge Handling & Graceful Degradation
1. **Tiered Inference Degradation**:
   - Under normal load: Full Tree Path feature attribution (Saabas / TreeInterpreter decomposition) is computed in real-time.
   - Under critical load (CPU > 80% or RPS > 30,000): The API gateway activates a `Fast-Path Degradation Header`. Inference services bypass tree decomposition and return pre-computed cached feature importance baselines, dropping inference latency from 35ms to < 1.5ms.
2. **Read-Through Multi-Level Caching**:
   - High-cardinality routes (e.g., Pune–Delhi, Mumbai–Delhi, Howrah–Delhi) represent 42% of all queries.
   - Predictions for identical (Train, Class, WL_Position, Date) tuples are cached in Redis with a 45-second sliding TTL, absorbing over 70% of peak queries without hitting ML models.
3. **Queue-Backed Asynchronous Logging**:
   - All cryptographic audit ledger writes and governance telemetry are offloaded to Kafka partitions asynchronously with zero blocking on the user request path.

### B. Resilience & Fault Isolation
1. **Circuit Breakers**:
   - Configured via Envoy / Istio with 5 consecutive failures / 50% error threshold triggering 10-second open-circuit fallback to rule-based deterministic baselines.
2. **Canary Deployments with Automated Rollback**:
   - New model versions start at 5% traffic. If PSI drift > 0.25 or P95 latency > SLA within 10 minutes, the autonomous agent supervisor instantly rolls traffic back to the proven baseline.

---

## 4. Cost & Capacity Estimation (Peak 60k RPS)
- **Inference Nodes**: 48 nodes (c6i.4xlarge: 16 vCPU, 32 GB RAM each)
- **Redis Cluster**: 8 memory-optimized nodes (r6i.2xlarge: 64 GB RAM)
- **Kafka Cluster**: 6 storage-optimized brokers (i3en.2xlarge: 2.5 TB NVMe)
- **Database**: Multi-region CockroachDB cluster across 3 availability zones
