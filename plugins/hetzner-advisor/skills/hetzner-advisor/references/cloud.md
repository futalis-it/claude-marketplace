# Cloud Servers

## Contents

- [Overview](#overview)
- [CX Series (Shared Intel/AMD)](#cx-series-shared-intelamd)
- [CAX Series (ARM64)](#cax-series-arm64)
- [CPX Series (Shared AMD)](#cpx-series-shared-amd)
- [CCX Series (Dedicated vCPU)](#ccx-series-dedicated-vcpu)
- [Pricing Add-ons](#pricing-add-ons)
- [Locations](#locations)

---

## Overview

| Category | Description | Best For |
|----------|-------------|----------|
| CX (Shared) | Cost-optimized, limited availability | Dev/test, low-traffic sites |
| CAX (ARM64) | Ampere ARM processors | ARM-native workloads, efficient compute |
| CPX (Shared) | Best price-performance | Low to medium CPU usage |
| CCX (Dedicated) | Unshared vCPUs | Critical production, consistent performance |

**Billing**: Hourly with monthly cap. Billed while server exists (even when off).

---

## CX Series (Shared Intel/AMD)

Cost-optimized, shared vCPU. Limited availability.

| Model | vCPU | RAM | NVMe | Price/mo |
|-------|------|-----|------|----------|
| CX23 | 2 | 4 GB | 40 GB | €3.49 |
| CX33 | 4 | 8 GB | 80 GB | €5.49 |
| CX43 | 8 | 16 GB | 160 GB | €9.49 |
| CX53 | 16 | 32 GB | 320 GB | €17.49 |

**Traffic**: 20 TB included (EU), 1 TB (US), 0.5 TB (Singapore)

**Best for**: Development, testing, low-traffic websites, small projects

---

## CAX Series (ARM64)

Ampere Altra ARM64 processors. Excellent efficiency.

| Model | vCPU | RAM | NVMe | Price/mo |
|-------|------|-----|------|----------|
| CAX11 | 2 | 4 GB | 40 GB | €3.79 |
| CAX21 | 4 | 8 GB | 80 GB | €6.49 |
| CAX31 | 8 | 16 GB | 160 GB | €12.49 |
| CAX41 | 16 | 32 GB | 320 GB | €24.49 |

**Traffic**: 20 TB included (EU)

**Best for**: ARM-native apps, Docker/Kubernetes, energy-efficient workloads, Go/Rust/Node.js

---

## CPX Series (Shared AMD)

Best price-performance for variable workloads.

### CPX (Original)

| Model | vCPU | RAM | NVMe | Traffic | Price/mo |
|-------|------|-----|------|---------|----------|
| CPX11 | 2 | 2 GB | 40 GB | 1 TB (US) | €4.99 |
| CPX21 | 3 | 4 GB | 80 GB | 2 TB (US) | €9.49 |
| CPX31 | 4 | 8 GB | 160 GB | 3 TB (US) | €16.49 |
| CPX41 | 8 | 16 GB | 240 GB | 4 TB (US) | €30.49 |
| CPX51 | 16 | 32 GB | 360 GB | 5 TB (US) | €60.49 |

### CPX2 (Newer AMD)

| Model | vCPU | RAM | NVMe | Traffic | Price/mo |
|-------|------|-----|------|---------|----------|
| CPX12 | 1 | 2 GB | 40 GB | 0.5 TB | €6.49 |
| CPX22 | 2 | 4 GB | 80 GB | 1 TB | €6.49-12.49 |
| CPX32 | 4 | 8 GB | 160 GB | 2 TB | €10.99-25.49 |
| CPX42 | 8 | 16 GB | 320 GB | 3 TB | €19.99-43.49 |
| CPX52 | 12 | 24 GB | 480 GB | 4 TB | €28.49-60.49 |
| CPX62 | 16 | 32 GB | 640 GB | 5 TB | €38.99-77.49 |

**Best for**: Web apps, APIs, general-purpose compute, variable workloads

---

## CCX Series (Dedicated vCPU)

Dedicated (unshared) AMD vCPUs. Consistent, predictable performance.

| Model | vCPU | RAM | NVMe | Traffic (EU/US) | Price/mo |
|-------|------|-----|------|-----------------|----------|
| CCX13 | 2 | 8 GB | 80 GB | 20 TB / 1 TB | €12.49-21.50 |
| CCX23 | 4 | 16 GB | 160 GB | 20 TB / 2 TB | €24.49-39.90 |
| CCX33 | 8 | 32 GB | 240 GB | 30 TB / 3 TB | €48.49-74.90 |
| CCX43 | 16 | 64 GB | 360 GB | 40 TB / 4 TB | €96.49-137.50 |
| CCX53 | 32 | 128 GB | 600 GB | 50 TB / 6 TB | €192.49-294.50 |
| CCX63 | 48 | 192 GB | 960 GB | 60 TB / 8 TB | €288.49-482.50 |

**Best for**: Production workloads, databases, latency-sensitive apps, Kubernetes nodes, CI/CD runners

---

## Pricing Add-ons

### Network & Traffic
- **EU locations**: 20 TB+ included
- **US locations**: 1-8 TB included (varies by plan)
- **Singapore**: 0.5 TB included
- **Overage**: €1.00/TB (EU/US), €7.40/TB (Singapore)

### IPv4
- **Primary IPv4**: €0.50/month extra
- **IPv6-only**: No extra charge

### Block Storage
- **Price**: €0.044/GB/month
- **Max per volume**: 10 TB
- **Max volumes per server**: 16

### Backups
- **Price**: 20% of instance price
- **Retention**: Up to 7 automatic backups

### Snapshots
- **Price**: €0.011/GB/month

---

## Locations

| Region | Location | Code |
|--------|----------|------|
| Germany | Nuremberg | NBG1 |
| Germany | Falkenstein | FSN1 |
| Finland | Helsinki | HEL1 |
| USA | Ashburn, Virginia | ASH |
| USA | Hillsboro, Oregon | HIL |
| Singapore | Singapore | SIN |

**Note**: Pricing varies by location. EU locations generally cheapest.
