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

```
Virtualization (VMware vCenter Server): v7.0.0
Logging Library (Apache Log4j): v2.14.1
VPN Gateway (Fortinet FortiOS): v7.0.5
Web Application (Atlassian Confluence): v8.0.0
Load Balancer (Citrix ADC): v13.0-58.30
```

### 2. CVEs List (`cve_list.txt`)
The list of CVEs extracted from a Local Vulnerability Database
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
### 1. Negativ: (True) 
<img width="655" height="485" alt="image" src="https://github.com/user-attachments/assets/a924dcfd-f15f-4cb0-b67c-20b267fd1cc2" />


### 2. Positive: 
- Case 1: (True) 
<img width="507" height="418" alt="image" src="https://github.com/user-attachments/assets/82d943e2-0b30-4078-ae62-4af73e748f14" />

- Case 2: (True)
<img width="580" height="410" alt="image" src="https://github.com/user-attachments/assets/d1eb583d-5512-4ae7-af48-74485674579d" />


