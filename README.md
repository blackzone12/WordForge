# ⚒️ WordForge: The Ultimate Targeted Wordlist Architect

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Platform](https://img.shields.io/badge/platform-Kali%20%7C%20Windows%20%7C%20Termux-green)
![Language](https://img.shields.io/badge/language-Python%203-yellow)

**WordForge** is a high-performance, context-aware password generator built for modern penetration testing. Unlike generic wordlists (like RockYou) that rely on sheer volume, WordForge builds **targeted intelligence** by forging passwords from the target's own life, hobbies, and history.

---

## 🌟 Why WordForge Matters (Importance)

In modern cybersecurity, humans still choose passwords based on familiarity. A 50MB targeted wordlist often outperforms a 10GB generic one because:
1. **Context is King**: Most people use names of pets, children, or favorite teams combined with significant years.
2. **Efficiency**: Targeted attacks are faster, quieter, and have a significantly higher success rate.
3. **Zero Waste**: No more wasting CPU cycles on `123456` if the target is a professional who uses `Company2024!`.

---

## 🚀 Core Features

- **🧠 Cognitive Intelligence**: Prompts for 15+ data categories including family, past locations, and critical years.
- **📂 Auto-Result Architecture**: Automatically creates a `results/` directory and names wordlists after your target for instant organization.
- **🔡 Multi-Layer Leet Speak**: Transforms "Password" into `@$$w0rd`, `P4ssw0rd`, and more using high-probability substitution matrices.
- **📅 Chronological Mapping**: Injects years (birth, anniversary, current) into base words in various permutations.
- **🧩 Smart Permutations**: Combines personal data with common terminal symbols (`!`, `@`, `#`, `$`) and number sequences.
- **⚡ Short Commands**: Zero-friction execution with native wrappers for Windows (`.bat`) and Linux/Termux (`.sh`).

---

## 🛠️ Setup & Installation

WordForge is designed to be portable and dependency-free.

### 1. Requirements
- **Python 3.6+** must be installed on your system.

### 2. Installation
```bash
# Clone the forge
git clone https://github.com/blackzone12/WordForge.git
cd WordForge
```

### 3. Quick Command Setup
No more typing `python wordforge.py`. Use the built-in short commands:

- **Windows**: Just type `.\wordforge`
- **Linux/Kali/Termux**: Run `chmod +x wordforge.sh` then `./wordforge.sh`

---

## 📖 How to Use

### A. The Interactive Forge (Recommended)
Simply run the tool and answer what you know. Leave blanks for unknown details.

```powershell
.\wordforge
```

### B. The CLI Strike (Fast Mode)
Generate a list instantly using flags for known primary details:

```powershell
.\wordforge --name "John Doe" --year 1992
```

### C. Piping to ripcrack
WordForge is the perfect companion for high-speed crackers.

```bash
./wordforge.sh | ./ripcrack crack -
```

---

## 📊 Performance Benchmark
| Target Profile | Total Keywords | Permutations | Time to Forge |
| :--- | :--- | :--- | :--- |
| Minimal (Name only) | 1 | ~4,500 | < 0.1s |
| Medium (Name, Pet, Year) | 3 | ~18,000 | < 0.2s |
| Complete (Full Profile) | 15+ | ~150,000+ | < 1.0s |

---

## 📂 Project Structure
- `wordforge.py` - The core Python engine.
- `wordforge.bat` - Windows command wrapper.
- `wordforge.sh` - Linux/Termux command wrapper.
- `results/` - Your targeted wordlists (created automatically).
- `README.md` - This documentation.

---

## 🛡️ Legal & Ethical Usage
**WordForge** is intended for authorized security auditing and educational purposes only. Unauthorized access to computer systems is illegal. The developers assume no liability for misuse of this tool. **Always obtain explicit permission before testing.**

---
*Forged with precision for the security elite.*
