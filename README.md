# CVEs Matching

A security utility designed to cross-reference a project's **Asset List** (dependencies) against a **CVE List** sourced from a Local Vulnerability Database.

The tool parses current dependency versions and compares them against vulnerable version ranges to determine if an asset is **Safe** or **Vulnerable** using a specific time-based verification strategy.

## 🚀 Features

- **Asset Mapping:** Ingests a list of software dependencies and their installed versions.
- **CVE Correlation:** Cross-references assets against a provided CVE dataset.
- **Time-Based Verification:** Validates safety by dynamically searching for release dates (via Google Search) rather than relying solely on semantic version string parsing.
- **Safety Reporting:** Outputs a clear status for each dependency (Safe/Unsafe).

## ⚙️ How It Works (Logic)

The core comparison engine follows this specific decision tree:

1. **Ingest Asset:** The tool reads an item from the input asset list.
2. **CVE Lookup:** It checks if the asset exists in the local CVE list.
   - **Condition A:** If the asset is **NOT** in the CVE list → **SAFE**.
   - **Condition B:** If the asset **IS** in the CVE list, the tool proceeds to verification.
3. **Verification Steps:**
   - **Fetch Date:** The tool performs a Google search to find the exact **release date** of the current asset version.
   - **Analyze Date:**
     1. If the release date falls within the `vulnerable_range` → **UNSAFE**.
     2. If the release date is `>=` the release date of the `safe_min_version` → **SAFE**.

## 📂 Input Data Structure

To ensure accurate version checking, input files should follow the schemas below.

### 1. Asset List (`assets.txt`)
The list of current dependencies.

Eg:
```
Virtualization (VMware vCenter Server): v7.0.0
Logging Library (Apache Log4j): v2.14.1
VPN Gateway (Fortinet FortiOS): v7.0.5
Web Application (Atlassian Confluence): v8.0.0
Load Balancer (Citrix ADC): v13.0-58.30
```

### 2. CVEs List (`cve_list.txt`)
The list of CVEs extracted from a Local Vulnerability Database.

Eg:
```
CVE-2021-44228 (Log4Shell)
Description: A critical Remote Code Execution (RCE) vulnerability in Apache Log4j's JNDI lookup feature.
Affected Versions (Unsafe): 2.0-beta9 through 2.14.1
Fixed Version: 2.15.0

CVE-2023-22515 (Privilege Escalation)
Description: A broken access control vulnerability in Atlassian Confluence Data Center & Server allowing attacker to create unauthorized admin accounts.
Affected Versions (Unsafe): 8.0.0 through 8.5.1
Fixed Version: 8.5.2

CVE-2023-3519 (Citrix Unauthenticated RCE)
Description: A vulnerability allowing code execution on Citrix ADC appliances configured as a Gateway (VPN) without requiring a password.
Affected Versions (Unsafe): NetScaler ADC and NetScaler Gateway 13.0 before 13.0-91.13
Fixed Version: 13.0-91.13

CVE-2023-27997 (FortiOS Heap Overflow)
Description: A heap-based buffer overflow in FortiOS SSL-VPN that allows arbitrary code execution.
Affected Versions (Unsafe): FortiOS 7.0.0 through 7.0.11
Fixed Version: 7.0.12
```

## Result 
### 1. Negative: (True) 
Input Assets:
```
WebServer (Nginx): v1.18.0
Cache (Redis): v7.0.5
Message bus (Apache Kafka): v3.6.1
PostgreSQL: v16
Zabbix App: v6.0
K8S (Kubernetes): v1.27.8
```
<img width="655" height="485" alt="image" src="https://github.com/user-attachments/assets/a924dcfd-f15f-4cb0-b67c-20b267fd1cc2" />


### 2. Positive: 
- Case 1: (True)
                          
Input Assets:
```
Virtualization (VMware vCenter Server): v7.0.0
Logging Library (Apache Log4j): v2.14.1
VPN Gateway (Fortinet FortiOS): v7.0.5
Web Application (Atlassian Confluence): v8.0.0
Load Balancer (Citrix ADC): v13.0-58.30
```
<img width="507" height="418" alt="image" src="https://github.com/user-attachments/assets/82d943e2-0b30-4078-ae62-4af73e748f14" />

- Case 2: (True)

Input Assets:
```
Hypervisor (VMware ESXi): v6.7U2c
Management (VMware vCenter): v6.5U3f
Cryptography Lib (OpenSSL): v1.0.2k
Network OS (Cisco IOS XE): v16.6.1
Database Proxy (Envoy): v1.14.0-dev
```
<img width="580" height="410" alt="image" src="https://github.com/user-attachments/assets/d1eb583d-5512-4ae7-af48-74485674579d" />

- Case 3: (True)

Input Assets:
```
react: v16.6.1
lodash: v4.17.15
axios: v0.21.0
openssl: v1.0.2k
django: v3.1.2
spring-framework: v5.2.8
fastapi: v0.63.0
log4j: v2.14.1
vmware_esxi: 6.7.0
```

<img width="545" height="699" alt="image" src="https://github.com/user-attachments/assets/619ecd51-dae5-4dcf-9922-72799ec6406c" />

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Lad1411/CVEs-matching.git
    cd CVEs-matching
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration (API Keys)

This tool requires access to the **Google Custom Search API** [or whatever service you use] to fetch release dates dynamically.

1.  **Get your API Key:**
    * Go to the [Google AI STUDIO](https://aistudio.google.com/api-keys/).
    * Create a project and enable the **Custom Search API**.
    * Generate an **API Key**.

2.  **Set up the environment:**
    Create a file named `.env` in the root folder of the project.

3.  **Add your keys:**
    Open the `.env` file and paste your keys like this:
    ```ini
    API_KEY=your_api_key_here
    ```

## Usage

1.  **Prepare your data:**
    You need two input files to run the scanner.

**A. Asset List (`assets.txt`)**
Create a text file listing your software assets and their versions.
*Format:* `library_name: version`

*Example `assets.txt`:*
```text
react: v16.6.1
lodash: v4.17.15
axios: v0.21.0
django: v3.1.2
```

**B. CVE List (`cve_list.txt`)**
Create a text file listing all CVEs (descriptions and affected verisons/fixed version)

*Example `cve_list.txt`:*
```text
CVE-2021-44228 (Log4Shell)
Description: A critical Remote Code Execution (RCE) vulnerability in Apache Log4j's JNDI lookup feature.
Affected Versions (Unsafe): 2.0-beta9 through 2.14.1

CVE-2023-22515 (Privilege Escalation)
Description: A broken access control vulnerability in Atlassian Confluence Data Center & Server allowing attacker to create unauthorized admin accounts.
Affected Versions (Unsafe): 8.0.0 through 8.5.1
Fixed Version: 8.5.2

CVE-2023-3519 (Citrix Unauthenticated RCE)
Description: A vulnerability allowing code execution on Citrix ADC appliances configured as a Gateway (VPN) without requiring a password.
Affected Versions (Unsafe): NetScaler ADC and NetScaler Gateway 13.0 before 13.0-91.13
Fixed Version: 13.0-91.13

CVE-2023-27997 (FortiOS Heap Overflow)
Description: A heap-based buffer overflow in FortiOS SSL-VPN that allows arbitrary code execution.
Affected Versions (Unsafe): FortiOS 7.0.0 through 7.0.11
Fixed Version: 7.0.12
```


2.  **Run the scanner:**
    ```bash
    python CVEs_matching.py -c <path_to_cve_list> -a <path_to_asset_list> -s <path_to_save_result>
    ```

Eg:
   ```bash
    python CVEs_matching.py -c data/cve_list.txt -a data/assets.txt -s results/output.json
   ```
   
## Output
The results will be saved to the specified path (e.g., results/output.json or similar) containing the detailed safety analysis.

