# TOOLS DOCUMENTATION

## Network Tools

### 1. Port Scanner
**ID**: `port-scan`

Fast port scanner dengan multi-threading support.

**Usage**:
```bash
python aleo_pantest_cli.py run port-scan --host 192.168.1.1
python aleo_pantest_cli.py run port-scan --host example.com --port 80,443,3306,5432
```

**Parameters**:
- `--host`: Target host/IP (required)
- `--port`: Port specification (default: 1-1024)
  - Single: `80`
  - Range: `1-1024`
  - Multiple: `80,443,3306`

**Output**:
- Open ports
- Service names
- Response times

---

### 2. Packet Sniffer
**ID**: `sniffer`

Real-time network packet capture dan analysis.

**Usage**:
```bash
python aleo_pantest_cli.py run sniffer
```

**Features**:
- Packet capture
- Protocol analysis
- Traffic inspection

---

### 3. Ping Tool
**ID**: `ping`

ICMP ping untuk host reachability testing.

**Usage**:
```bash
python aleo_pantest_cli.py run ping --host 8.8.8.8
python aleo_pantest_cli.py run ping --host example.com --count 10
```

**Parameters**:
- `--host`: Target host/IP (required)
- `--count`: Number of packets (default: 4)
- `--timeout`: Timeout in seconds (default: 30)

---

### 4. DNS Lookup
**ID**: `dns`

DNS resolution dengan multiple record types.

**Usage**:
```bash
python aleo_pantest_cli.py run dns --domain example.com
```

**Features**:
- A records
- MX records
- NS records
- TXT records
- Reverse lookup

---

### 5. Traceroute
**ID**: `traceroute`

Network path analysis.

**Usage**:
```bash
python aleo_pantest_cli.py run traceroute --host 8.8.8.8
```

**Parameters**:
- `--host`: Target host/IP
- `--max-hops`: Maximum hops (default: 30)

---

## Wireless Tools

### 1. WiFi Deauthentication
**ID**: `deauth`

Memutuskan koneksi klien dari Access Point secara real-time menggunakan paket deauthentication.

**Usage**:
```bash
Aleocrophic run deauth --target 00:11:22:33:44:55 --iface wlan0mon
Aleocrophic run deauth --target 00:11:22:33:44:55 --client AA:BB:CC:DD:EE:FF --count 100
```

**Features**:
- **Real Hardware Support**: Menggunakan `scapy` untuk injeksi paket langsung ke hardware.
- **High Success Rate**: Mengirim paket dua arah (AP ke Client dan Client ke AP).
- **Fast Response**: Burst mode mengirimkan paket awal dalam < 2 detik.
- **Safety Built-in**: Batasan durasi maksimal 1 jam untuk mencegah penyalahgunaan.

**Parameters**:
- `--target`: BSSID/MAC Address dari Access Point (required).
- `--client`: MAC Address klien (default: `FF:FF:FF:FF:FF:FF` untuk semua klien).
- `--iface`: Interface nirkabel dalam monitor mode (default: `wlan0mon`).
- `--count`: Jumlah paket yang dikirim (default: 64).
- `--interval`: Interval antar paket dalam detik (default: 0.05).
- `--burst`: Aktifkan burst mode untuk respon cepat (default: True).

---

### 2. Beacon Flood
**ID**: `beacon-flood`

Membuat ribuan Access Point palsu untuk membanjiri daftar scan WiFi.

**Usage**:
```bash
Aleocrophic run beacon-flood --iface wlan0mon --count 100
```

**Parameters**:
- `--iface`: Monitor mode interface.
- `--count`: Jumlah SSID palsu yang akan dibuat.
- `--duration`: Durasi serangan (max 1 jam).

---

### 3. WiFi Scanner
**ID**: `wifi-scan`

Scan jaringan WiFi di sekitar dan menampilkan detail sinyal, enkripsi, dan BSSID.

**Usage**:
```bash
Aleocrophic run wifi-scan --iface wlan0mon
```
---

### 6. WHOIS Lookup
**ID**: `whois`

Domain ownership information.

**Usage**:
```bash
python aleo_pantest_cli.py run whois --domain example.com
```

**Parameters**:
- `--domain`: Target domain
- `--ip`: Target IP for IP ownership

---

### 7. SSL Checker
**ID**: `ssl-check`

SSL/TLS certificate analysis.

**Usage**:
```bash
python aleo_pantest_cli.py run ssl-check --host example.com --port 443
```

**Features**:
- Certificate validity
- Expiration dates
- Cipher suites
- Chain validation

---

### 8. IP Scanner
**ID**: `ip-scan`

Subnet scanning untuk host discovery.

**Usage**:
```bash
python aleo_pantest_cli.py run ip-scan --network 192.168.1.0/24
```

**Parameters**:
- `--network`: Network CIDR notation (required)

---

## Web Exploitation Tools

### 1. SQL Injector
**ID**: `sql-inject`

SQL injection vulnerability testing.

**Usage**:
```bash
python aleo_pantest_cli.py run sql-inject --url http://target.com/page.php?id=1
```

**Features**:
- Payload testing
- Error-based detection
- Vulnerability confirmation

---

### 2. XSS Detector
**ID**: `xss-detect`

Cross-site scripting vulnerability detection.

**Usage**:
```bash
python aleo_pantest_cli.py run xss-detect --url http://target.com
```

**Detects**:
- Reflected XSS
- DOM-based XSS
- Payload reflection

---

### 3. CSRF Detector
**ID**: `csrf-detect`

CSRF vulnerability analysis.

**Usage**:
```bash
python aleo_pantest_cli.py run csrf-detect --url http://target.com/form
```

**Checks**:
- CSRF tokens
- Token validation
- Form security

---

### 4. Web Crawler
**ID**: `crawler`

Website structure mapping.

**Usage**:
```bash
python aleo_pantest_cli.py run crawler --url http://target.com --depth 2
```

**Parameters**:
- `--url`: Target URL
- `--depth`: Crawling depth (default: 1)

---

### 5. Vulnerability Scanner
**ID**: `vuln-scan`

Common web vulnerability scanning.

**Usage**:
```bash
python aleo_pantest_cli.py run vuln-scan --url http://target.com
```

**Checks**:
- Security headers
- Exposed files
- Common vulnerabilities

---

### 6. Subdomain Finder
**ID**: `subdomain`

Subdomain enumeration.

**Usage**:
```bash
python aleo_pantest_cli.py run subdomain --domain example.com
```

**Features**:
- Brute force enumeration
- DNS resolution
- IP mapping

---

## OSINT Tools

### 1. Email Finder
**ID**: `email-find`

Email discovery from domain.

**Usage**:
```bash
python aleo_pantest_cli.py run email-find --domain example.com
```

**Features**:
- Email extraction
- Domain filtering
- Verification

---

### 2. Domain Info
**ID**: `domain-info`

Comprehensive domain information gathering.

**Usage**:
```bash
python aleo_pantest_cli.py run domain-info --domain example.com
```

**Gathers**:
- DNS records
- IP information
- HTTP headers
- Server information

---

### 3. IP Geolocation
**ID**: `ip-geo`

Geographical IP lookup.

**Usage**:
```bash
python aleo_pantest_cli.py run ip-geo --ip 8.8.8.8
```

**Information**:
- Country
- City
- Coordinates
- ISP info

---

### 4. Metadata Extractor
**ID**: `metadata`

File dan website metadata extraction.

**Usage**:
```bash
python aleo_pantest_cli.py run metadata --url http://target.com
python aleo_pantest_cli.py run metadata --file document.pdf
```

**Supports**:
- PDF metadata
- Image EXIF
- Web meta tags

---

### 5. Search Engine Dorking
**ID**: `dorking`

Advanced search engine queries.

**Usage**:
```bash
python aleo_pantest_cli.py run dorking --query "site:example.com filetype:pdf"
```

**Features**:
- Custom queries
- Dork templates
- Result analysis

---

## Utility Tools

### 1. Password Generator
**ID**: `passgen`

Secure password generation.

**Usage**:
```bash
python aleo_pantest_cli.py run passgen --length 16 --count 5
```

**Parameters**:
- `--length`: Password length
- `--count`: Number of passwords
- `--include-special`: Include special chars

---

### 2. Hash Tools
**ID**: `hash`

Multi-algorithm hashing.

**Usage**:
```bash
python aleo_pantest_cli.py run hash --text "password" --algorithm sha256
```

**Algorithms**:
- MD5
- SHA1
- SHA224
- SHA256
- SHA384
- SHA512

---

### 3. Proxy Manager
**ID**: `proxy`

Proxy testing dan management.

**Usage**:
```bash
python aleo_pantest_cli.py run proxy --get-free
```

**Features**:
- Proxy testing
- Working proxy detection
- Proxy rotation

---

### 4. URL Encoder/Decoder
**ID**: `encode`

Encoding transformations.

**Usage**:
```bash
python aleo_pantest_cli.py run encode --text "hello world" --operation encode
```

**Operations**:
- URL encode/decode
- Base64 encode/decode
- HTML entity encoding
- Double encoding

---

### 5. Reverse Shell Generator
**ID**: `revshell`

Reverse shell payload generation.

**Usage**:
```bash
python aleo_pantest_cli.py run revshell --host 10.0.0.1 --port 4444 --language bash
```

**Shells**:
- bash
- sh
- python
- python3
- perl
- php
- ruby
- powershell

---

## Usage Tips

1. **Export Results**: Semua tools mendukung `--output` untuk save results
2. **Custom Parameters**: Lihat help untuk parameters spesifik
3. **Error Handling**: Check logs untuk error details
4. **Testing**: Always test pada authorized systems

---

**Last Updated**: Desember 2024
