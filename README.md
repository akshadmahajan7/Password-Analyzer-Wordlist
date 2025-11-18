# 🔒 Password Strength Analyzer & Custom Wordlist Generator

## Project Overview

This tool combines a **Password Strength Analyzer** with a powerful **Custom Wordlist Generator** specifically designed for security testing and educational purposes. It allows users to quickly assess the resilience of their passwords using industry-standard metrics (like `zxcvbn`) and generate highly targeted wordlists based on known user-specific information (like name, pet, dates) and common attack patterns (leetspeak, appending years).

---

## ✨ Features

* **Password Strength Analysis:** Uses the `zxcvbn` library (the same logic used by Dropbox and others) to provide a realistic assessment of a password's crack time.
* **Custom Wordlist Generation:** Generates attack-specific wordlists from user-provided inputs (e.g., "John", "2005", "Max").
* **Pattern Inclusion:** Automatically incorporates common password attack patterns:
    * **Leetspeak:** e.g., 'a' -> '4', 's' -> '5', 'o' -> '0'.
    * **Year Appending:** Adds common years/dates to base words.
    * **Capitalization/Reversal:** Various casing permutations.
* **Export:** Exports the generated wordlist to a standard **`.txt`** file format, compatible with tools like **Hashcat** and **John the Ripper**.
* **Graphical User Interface (GUI):** A user-friendly desktop application built with `tkinter` for easy interaction. 

---

## 🚀 Getting Started

### 🛠️ Project Structure and Files
Here's a suggested structure for your Password Strength Analyzer and Custom Wordlist Generator project:
```
password-analyzer-wordlist/
├── src/
│   ├── strength_analyzer.py      # Core logic for password analysis (using zxcvbn)
│   ├── wordlist_generator.py     # Core logic for generating custom wordlists
│   └── gui.py                    # Tkinter-based GUI implementation
├── requirements.txt              # List of required Python packages
├── README.md                     # Project documentation (the main file for GitHub)
├── LICENSE                       # (Optional but recommended) e.g., MIT License
└── .gitignore                    # (Recommended) For excluding temporary/compiled files
```

### Prerequisites

You need **Python 3.x** installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/password-analyzer-wordlist.git](https://github.com/YOUR_GITHUB_USERNAME/password-analyzer-wordlist.git)
    cd password-analyzer-wordlist
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download NLTK Data (if necessary for wordlist generation):**
    Open a Python interpreter and run:
    ```python
    import nltk
    nltk.download('punkt')
    # You may need other corpora depending on your final implementation, e.g., 'words'
    ```

### Usage

#### 1. Running the GUI

The easiest way to use the tool is via the graphical interface.

```bash
python src/gui.py
```
#### 2. Wordlist Generation (Command Line)
For power users, the wordlist_generator.py can be executed directly (if you implement an argparse interface).

```bash
python src/wordlist_generator.py --name "Alice" --date "1990" --pet "Mittens" --output wordlist.txt
```

---

## ⚙️ Core Logic Breakdown (For Developers)
**Password Strength Analysis (`strength_analyzer.py`)**
The script takes a password string and known user details (context) as input. It utilizes the zxcvbn library, which returns a dictionary containing:
* `score`: From 0 (worst) to 4 (best).
* `crack_time_seconds`: Estimated time to crack.
* `feedback`: Suggestions for improving the password.

**Custom Wordlist Generation (`wordlist_generator.py`)**
This module is responsible for the following steps:
1. **Base Inputs**: Collects user-provided strings (name, date, pet, etc.).
2. **Permutations**: Creates variations of the base inputs (e.g., capitalization, reversals, substrings).
3. **Pattern Application**: Applies Leetspeak substitutions and Year Appending to the permutations.
4. **Export**: Writes all generated strings, one per line, to the specified output file (.txt).

---

## 🤝 Contributing
Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

---

## ⚖️ License
Distributed under the MIT License. See LICENSE for more information.
