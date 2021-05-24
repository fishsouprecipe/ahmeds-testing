# Botpark
## Pre-requirements
- python3.7 with setuptools and pip
- playwright with chromium installed
- git
- curl

## Installation
### One line
```bash
curl https://raw.githubusercontent.com/fishsouprecipe/ahmeds-testing/primary/install.sh | sh
```

### Manual
```bash
git clone https://github.com/fishsouprecipe/ahmeds-testing.git \
    && python3 -m pip install playwright \
    && playwright install chromium \
    && python3 -m pip install ./ahmeds-testing
```

## Commands
### Adding telegram accounts
```bash
botpark add

# Pass your telegram credentials
```

### Remove telegram accounts
```bash
botpark remove

# Pass phone number to delete from list
```

### Listing telegram accounts
```bash
botpark list
```

### Run
```bash
botpark run
```
