# Dedicated Servers

## Contents

- [EX Line (Intel)](#ex-line-intel)
- [AX Line (AMD)](#ax-line-amd)
- [SX Line (Storage)](#sx-line-storage)
- [GPU Line](#gpu-line)
- [Dell Line (Enterprise)](#dell-line-enterprise)
- [Common Features](#common-features)

---

## EX Line (Intel)

### EX44
- **Price**: €39/mo (€0.0625/hr) | Setup: €79
- **CPU**: Intel Core i5-13500 (6P + 8E cores, Raptor Lake)
- **RAM**: 64 GB DDR4 (max 128 GB)
- **Storage**: 2x 512 GB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 25W idle / 118W max
- **Best for**: Entry-level dedicated, small apps, dev servers

### EX63
- **Price**: €66/mo (€0.1057/hr) | Setup: €79
- **CPU**: Intel Core Ultra 7 265 (8P + 12E cores, Arrow Lake)
- **RAM**: 64 GB DDR5 (max 192 GB DDR5 ECC)
- **Storage**: 2x 1 TB NVMe SSD Gen4
- **Network**: 1 Gbit/s (upgradeable to 10 Gbit/s), unlimited traffic
- **Power**: 32W idle / 140W max
- **Best for**: Production apps, medium workloads, modern DDR5 performance

### EX130-R (RAM-focused)
- **Price**: €134/mo (€0.2147/hr) | Setup: €159
- **CPU**: Intel Xeon Gold 5412U (24-core, Sapphire Rapids)
- **RAM**: 256 GB DDR5 ECC (max 768 GB)
- **Storage**: 2x 1.92 TB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 62W idle / 212W max
- **Best for**: Databases, in-memory caching, high-RAM workloads

### EX130-S (Storage-focused)
- **Price**: €134/mo (€0.2147/hr) | Setup: €159
- **CPU**: Intel Xeon Gold 5412U (24-core, Sapphire Rapids)
- **RAM**: 128 GB DDR5 ECC (max 768 GB)
- **Storage**: 2x 3.84 TB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 59W idle / 204W max
- **Best for**: Storage-heavy workloads, large databases

---

## AX Line (AMD)

### AX41-NVMe
- **Price**: €37-42/mo | Setup: €0
- **CPU**: AMD Ryzen 5 3600 (6-core, Zen 2)
- **RAM**: 64 GB DDR4
- **Storage**: 2x 512 GB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Best for**: Budget dedicated, small projects, no setup fee

### AX42
- **Price**: €46-52/mo | Setup: €79-88
- **CPU**: AMD Ryzen 7 PRO 8700GE (8-core, Zen 4)
- **RAM**: 64 GB DDR5 ECC (max 128 GB)
- **Storage**: 2x 512 GB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 26W idle / 83W max
- **Best for**: Modern AMD performance, efficient power usage

### AX102
- **Price**: €104-116/mo | Setup: €79-88
- **CPU**: AMD Ryzen 9 7950X3D (16-core, Zen 4, 3D V-Cache)
- **RAM**: 128 GB DDR5 ECC (max 192 GB)
- **Storage**: 2x 1.92 TB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 34W idle / 166W max
- **Best for**: Gaming servers, high single-thread performance, 3D V-Cache benefits

### AX162-R (RAM-focused)
- **Price**: €199-221/mo | Setup: €159-177
- **CPU**: AMD EPYC 9454P (48-core, Genoa Zen 4)
- **RAM**: 256 GB DDR5 ECC (max 1152 GB)
- **Storage**: 2x 3.84 TB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 63W idle / 408W max
- **Best for**: Heavy workloads, massive RAM capacity, virtualization

### AX162-S (Storage-focused)
- **Price**: €199-221/mo | Setup: €159-177
- **CPU**: AMD EPYC 9454P (48-core, Genoa Zen 4)
- **RAM**: 128 GB DDR5 ECC (max 1152 GB)
- **Storage**: 2x 3.84 TB NVMe SSD Gen4
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 61W idle / 349W max
- **Best for**: Storage + compute balance, large deployments

---

## SX Line (Storage)

Optimized for large storage capacity with HDD + NVMe combo.

### SX65
- **Price**: €104/mo (€0.1666/hr) | Setup: €79
- **CPU**: AMD Ryzen 7 3700X (8-core, Zen 2)
- **RAM**: 64 GB DDR4 ECC
- **NVMe**: 2x 1 TB Gen3
- **HDD**: 4x 22 TB SATA (88 TB raw)
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 47W idle / 166W max
- **Best for**: Backup server, file storage, media server

### SX135
- **Price**: €204/mo (€0.3269/hr) | Setup: €159
- **CPU**: AMD Ryzen 9 3900 (12-core, Zen 2)
- **RAM**: 128 GB DDR4 ECC
- **NVMe**: 2x 1.92 TB Gen3
- **HDD**: 8x 22 TB SATA (176 TB raw)
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 80W idle / 183W max
- **Best for**: Large storage, NAS replacement, archival

### SX295
- **Price**: €384/mo (€0.6154/hr) | Setup: €159
- **CPU**: AMD EPYC 7502P (32-core, Zen 2)
- **RAM**: 256 GB DDR4 ECC
- **NVMe**: 2x 7.68 TB Gen3
- **HDD**: 14x 22 TB SATA (308 TB raw)
- **Network**: 1 Gbit/s, unlimited traffic
- **Power**: 118W idle / 273W max
- **Best for**: Enterprise storage, data lakes, massive archives

---

## GPU Line

### GEX44 (AI Inference)
- **Price**: €184-205/mo | Setup: €159-177
- **CPU**: Intel Core i5-13500 (6P + 8E cores)
- **RAM**: 64 GB DDR4
- **GPU**: NVIDIA RTX 4000 SFF Ada Generation
  - 20 GB GDDR6 vRAM
  - 192 Tensor Cores
  - 306.8 TFLOPS tensor performance
- **Storage**: Configurable NVMe
- **Location**: Falkenstein (FSN1)
- **Best for**: AI inference, model serving, edge AI

### GEX131 (AI Training)
- **Price**: €889-988/mo | Setup: €159-177
- **CPU**: Intel Xeon Gold 5412U (24-core)
- **RAM**: 256 GB DDR5 ECC
- **GPU**: NVIDIA RTX PRO 6000 Blackwell Max-Q
  - 96 GB GDDR7 vRAM
  - 5th gen Tensor Cores
  - FP4 and DLSS 4 support
- **Storage**: Configurable NVMe
- **Location**: Nuremberg (NBG1), Falkenstein (FSN1)
- **Best for**: AI training, large models, ML research

**Note**: Single GPU only, multi-GPU not available.

---

## Dell Line (Enterprise)

Enterprise-grade servers with iDRAC, redundant PSU, hot-swap drives.

### DX153
- **Price**: €209/mo (€0.3349/hr) | Setup: €79
- **CPU**: 2x Intel Xeon Silver 4410Y (2x 12-core, Sapphire Rapids)
- **RAM**: 64 GB DDR5 ECC (max 2048 GB)
- **Storage**: Up to 10 hot-swap drives, PERC11 H755 RAID
- **Network**: 1 Gbit/s, unlimited traffic
- **Features**: iDRAC9 Enterprise, redundant Platinum PSU
- **Power**: 107W idle / 267W max
- **Best for**: Enterprise workloads, compliance requirements

### DX182
- **Price**: €259/mo (€0.4150/hr) | Setup: €79
- **CPU**: AMD EPYC 9454P (48-core, Genoa Zen 4)
- **RAM**: 128 GB DDR5 ECC (max 1152 GB)
- **Storage**: Up to 10 hot-swap drives, PERC11 H755 RAID
- **Network**: 1 Gbit/s, unlimited traffic
- **Features**: iDRAC9 Enterprise, redundant Platinum PSU
- **Power**: 86W idle / 421W max
- **Best for**: High-core-count enterprise workloads

### DX293
- **Price**: €299/mo (€0.4791/hr) | Setup: €79
- **CPU**: 2x Intel Xeon Gold 6438Y+ (2x 32-core, Sapphire Rapids)
- **RAM**: 64 GB DDR5 ECC (max 2048 GB)
- **Storage**: Up to 10 hot-swap drives, PERC11 H755 RAID
- **Network**: 1 Gbit/s, unlimited traffic
- **Features**: iDRAC9 Enterprise, redundant Platinum PSU
- **Power**: 110W idle / 540W max
- **Best for**: Dual-socket performance, maximum enterprise reliability

---

## Common Features

All dedicated servers include:

- **Traffic**: Unlimited (free)
- **IPv4**: 1 primary address
- **IPv6**: /64 subnet
- **DDoS Protection**: Included
- **Network Availability**: Min 99.9%
- **Contract**: No minimum period
- **Cancellation**: Immediate
- **Power**: 100% green electricity
- **OS**: Linux (various distros) or Windows Server (extra cost)
- **Root Access**: Full
- **Rescue System**: Available
