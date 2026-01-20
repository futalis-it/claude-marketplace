# Managed Servers & Web Hosting

## Contents

- [Managed Servers](#managed-servers)
  - [MC Line (Virtual)](#mc-line-virtual)
  - [MA Line (Dedicated)](#ma-line-dedicated)
- [Web Hosting](#web-hosting)
- [When to Use What](#when-to-use-what)

---

## Managed Servers

Fully managed by Hetzner: OS updates, security, backups, 24/7 monitoring.

**Pre-installed Stack**:
- OS: Debian Linux
- Web: Apache
- Database: MariaDB, PostgreSQL
- Languages: PHP 5/7/8, Perl, Python
- Cache: Redis
- Email: Exim, Dovecot, spam filter, ClamAV
- FTP: ProFTPd
- Admin: konsoleH panel
- SSL: Let's Encrypt, SSL Manager

### MC Line (Virtual)

| Model | Price/mo | vCores | RAM | NVMe | Accounts | Traffic |
|-------|----------|--------|-----|------|----------|---------|
| MC30 | €34-38 | 4 | 16 GB | 200 GB | 5 | 20 TB |
| MC60 | €54-60 | 8 | 32 GB | 400 GB | 15 | 20 TB |

- **Setup fee**: €34-60
- **Backup retention**: 7 days
- **Traffic overage**: €1/TB

**Best for**: Small agencies, multiple small websites, need managed stack without admin work

### MA Line (Dedicated)

| Model | Price/mo | CPU | RAM | NVMe | Accounts | Traffic |
|-------|----------|-----|-----|------|----------|---------|
| MA80 | €79-88 | Ryzen 7 3700X (8-core) | 64 GB ECC | 2x 512 GB | Unlimited | Unlimited |
| MA130 | €139-155 | Ryzen 9 5950X (16-core) | 128 GB ECC | 2x 960 GB | Unlimited | Unlimited |
| MA200 | €199-221 | EPYC 7502P (32-core) | 256 GB ECC | 2x 1.92 TB | Unlimited | Unlimited |

- **Setup fee**: €79-221
- **Backup retention**: 14 days
- **RAID**: Software RAID 1

**Best for**: Agencies, high-traffic managed sites, need dedicated performance with managed convenience

---

## Web Hosting

Shared hosting with Varnish caching, ideal for simple websites.

| Plan | Price/mo | Storage | Databases | Cronjobs | PHP Processes | Memory |
|------|----------|---------|-----------|----------|---------------|--------|
| S | €1.60-2 | 10 GB | 1 | 1 | 2 | 192 MB |
| M | €4-5.12 | 50 GB | 5 | 5 | 5 | 256 MB |
| L | €8-10.32 | 100 GB | 20 | 10 | 10 | 384 MB |
| XL | €16-19.72 | 300 GB | 50 | 20 | 20 | 512 MB |

### Features by Plan

| Feature | S | M | L | XL |
|---------|---|---|---|---|
| Unlimited mailboxes | Yes | Yes | Yes | Yes |
| Varnish caching | Yes | Yes | Yes | Yes |
| Daily backups | Yes | Yes | Yes | Yes |
| SSL (Let's Encrypt) | Yes | Yes | Yes | Yes |
| SSH access | No | No | Yes | Yes |
| Redis caching | No | No | Yes | Yes |
| Node.js | No | No | Yes | Yes |
| Phone support | No | No | No | Yes |

**Setup fees**: €5-10 (sometimes waived)

**Note**: Domain NOT included, must order separately (from €4.90/year)

**Best for**: Static sites, WordPress blogs, small business sites, personal projects

---

## When to Use What

| Need | Recommendation |
|------|----------------|
| Simple WordPress blog | Web Hosting S/M (€1.60-5/mo) |
| Business WordPress site | Web Hosting L or Managed MC30 |
| Agency managing multiple sites | Managed MC60 or MA80 |
| High-traffic managed site | Managed MA130/MA200 |
| E-commerce (Shopware, WooCommerce) | Web Hosting XL or Managed MC/MA |
| Need SSH access | Web Hosting L+ or Managed |
| Need Redis | Web Hosting L+ or Managed |
| No admin skills, need database | Web Hosting or Managed |
| Full control (root access) | Use Cloud or Dedicated instead |

### Managed vs Cloud/Dedicated

| Factor | Managed | Cloud/Dedicated |
|--------|---------|-----------------|
| Root access | No | Yes |
| OS updates | Hetzner handles | You handle |
| Security patches | Hetzner handles | You handle |
| Backups | Automatic | Configure yourself |
| Software stack | Pre-installed | Install yourself |
| Flexibility | Limited | Full |
| Price | Higher | Lower |

**Choose Managed** if you want convenience and don't need root access.

**Choose Cloud/Dedicated** if you need custom software, containers, or specific configurations.
