# DnD-character-sheet-creator

An aplication for creating DnD character sheets
...

## Installation

This project supports *two setup methods*:

- Using *Conda* (recommended)
- Using *pip* (for users without Conda)

All dependencies are provided in:
- environment.yml - full environment (Conda)
- requirements.txt - pip-only dependencies

---

## 1. Installation using Conda (recommended)

### 1.1 Create the environment
```bash
conda env create -f environment.yml
```

### 1.2 Activate the environment
```bash
conda activate DnD-creator
```

To deactivate an active environment, use

```bash
conda deactivate
```

---

## 2. Installation using pip (no conda required)

⚠️ Pip installation **might miss some Conda-only packages**, but works for most Python dependencies.


### 2.1 Create virtual environment (optional but recommended)
```bash
python -m venv venv
```

### 2.2 Activate it  
*Windows:*
```bash
venv\Scripts\activate
```

*Linux/Mac:*
```bash
source venv/bin/activate
```

### 2.3 Install dependencies
```bash
pip install -r requirements.txt
```

---

## 3. Running the project

Once your environment is ready, run the main script:

```bash
python main.py
```
