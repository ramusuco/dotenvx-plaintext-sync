# dxsync

CLI tool for syncing encrypted `.env` files across teams using dotenvx.

## Features

- **Simple CLI** - `dxsync init`, `dxsync encrypt`, `dxsync decrypt`
- **Per-environment encryption** - Separate keys for development, staging, production
- **Non-destructive** - Never overwrites your local plaintext `.env` files
- **Flexible paths** - Configure env file locations via `dxsync.json`

## Prerequisites

- Python 3.11+
- [dotenvx](https://dotenvx.com/docs/install) - Install via your preferred method:

```bash
# npm
npm install -g @dotenvx/dotenvx

# brew
brew install dotenvx/brew/dotenvx

# curl
curl -sfS https://dotenvx.sh | sh
```

## Installation

```bash
pip install dxsync
```

## Quick Start

```bash
# 1. Initialize in your project
cd your-project
dxsync init

# 2. Create your plaintext env file
echo "API_KEY=secret123" > envs/.env.development

# 3. Encrypt it
dxsync encrypt development
# → Creates enc/.env.development.enc and envs/keys/development.keys

# 4. Share envs/keys/development.keys with your team securely

# 5. Commit the encrypted file
git add enc/.env.development.enc
git commit -m "Add encrypted development env"
```

## Directory Structure

After `dxsync init`:

```
your-project/
├── dxsync.json             # Configuration
├── enc/                    # Encrypted files (commit these)
│   └── .env.development.enc
├── envs/                   # Local files (gitignored)
│   ├── .env.development    # Plaintext source
│   ├── .env.staging
│   ├── .env.production
│   ├── keys/               # Key files
│   │   └── development.keys
│   └── latest/             # Decrypted output
│       └── .env.development
└── .gitignore              # Updated by dxsync init
```

## Usage

### Encrypt

Add or update keys in your plaintext file, then encrypt:

```bash
# Edit envs/.env.development with your values
dxsync encrypt development
```

- First run: auto-generates key file and `.enc`
- Subsequent runs: adds new keys to existing `.enc`

### Decrypt

Get the key file from your team, then:

```bash
dxsync decrypt development
# → Output: envs/latest/.env.development
```

### Change existing values

1. Remove the key from `enc/.env.development.enc`
2. Update value in `envs/.env.development`
3. Run `dxsync encrypt development`

## Configuration

Edit `dxsync.json` to customize:

```json
{
  "env_dir": "envs",
  "envs": {
    "development": "envs/.env.development",
    "staging": "envs/.env.staging",
    "production": "envs/.env.production"
  },
  "enc_dir": "enc",
  "work_dir": "tmp/dxsync"
}
```

Or use `pyproject.toml`:

```toml
[tool.dxsync]
env_dir = "envs"
enc_dir = "enc"

[tool.dxsync.envs]
development = "envs/.env.development"
staging = "envs/.env.staging"
production = "envs/.env.production"
```

### Custom paths example

```json
{
  "env_dir": "config/env",
  "envs": {
    "dev": "config/env/.env.dev",
    "prod": "config/env/.env.prod"
  }
}
```

Note: All env paths must be under `env_dir` for security (gitignore protection).

## Design Principles

- **Append-only** - Existing keys in `.enc` are never auto-overwritten
- **Non-destructive** - Decryption outputs to `latest/`, not your working `.env`
- **Explicit reset** - Delete `.enc` manually to regenerate

## License

MIT

## References

- [dotenvx Documentation](https://dotenvx.com/docs)
