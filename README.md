# dotenvx-ops

CLI tool for syncing encrypted `.env` files across teams using dotenvx.

## Why dotenvx-ops?

[dotenvx](https://dotenvx.com/) is a great tool for encrypting `.env` files. It's designed to run apps with encrypted env files directly (`dotenvx run`), but sometimes you need **plaintext** `.env` files:

- Your framework reads `.env` directly
- You want to keep existing workflows
- You need to inspect values during debugging

### The problem with plaintext workflows

When decrypting `.env` files manually, operational risks emerge:

- **Path mistakes** - Typing paths manually every time leads to errors
- **OS differences** - Path separators and behaviors vary across systems
- **Multi-environment chaos** - Managing dev/staging/production separately is tedious
- **Accidental commits** - Easy to forget gitignore and leak secrets

### How dotenvx-ops helps

| Problem | Solution |
|---------|----------|
| Path mistakes | Config file manages all paths centrally |
| OS differences | Consistent interface across platforms |
| Multi-environment | Just specify env name: `dotenvx-ops encrypt development` |
| Accidental commits | Auto-configures gitignore, validates env paths are protected |
| Overwriting team values | Append-only encryption preserves existing keys |
| Losing local changes | Non-destructive decrypt outputs to `latest/`, not your working file |
| Over-sharing keys | Separate key files per environment |

## Prerequisites

- Python 3.11+
- [dotenvx](https://dotenvx.com/docs/install):

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
pip install dotenvx-ops
```

## Quick Start

```bash
# 1. Initialize in your project
cd your-project
dotenvx-ops init

# 2. Create your plaintext env file
echo "API_KEY=secret123" > envs/.env.development

# 3. Encrypt it
dotenvx-ops encrypt development
# → Creates enc/.env.development.enc and envs/keys/development.keys

# 4. Share envs/keys/development.keys with your team securely

# 5. Commit the encrypted file
git add enc/.env.development.enc
git commit -m "Add encrypted development env"
```

## Directory Structure

After `dotenvx-ops init`:

```
your-project/
├── dotenvx-ops.json        # Configuration
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
└── .gitignore              # Updated automatically
```

## Usage

### Encrypt

Add or update keys in your plaintext file, then encrypt:

```bash
dotenvx-ops encrypt development
```

- First run: generates key file and `.enc`
- Subsequent runs: **adds** new keys to existing `.enc` (doesn't overwrite existing values)

### Update existing values

To update values that already exist in the encrypted file:

```bash
dotenvx-ops encrypt development --update
```

This will:
1. Compare your plaintext file with the encrypted file
2. Show a diff of changes (new keys and updated values)
3. Ask for confirmation before applying

```
=== Changes to be applied ===

[NEW]
  + NEW_API_KEY

[UPDATE]
  ~ DATABASE_URL
  ~ SECRET_KEY

Apply these changes? [y/N]:
```

### Decrypt

Decrypt to `latest/` directory (safe, doesn't overwrite your working file):

```bash
dotenvx-ops decrypt development
# → Output: envs/latest/.env.development
```

### Pull

Decrypt and apply directly to your working file in one step:

```bash
dotenvx-ops pull development
# → Decrypts and copies to envs/.env.development
```

## Configuration

Edit `dotenvx-ops.json`:

```json
{
  "env_dir": "envs",
  "envs": {
    "development": "envs/.env.development",
    "staging": "envs/.env.staging",
    "production": "envs/.env.production"
  },
  "enc_dir": "enc",
  "work_dir": "tmp/dotenvx-ops"
}
```

Or use `pyproject.toml`:

```toml
[tool.dotenvx-ops]
env_dir = "envs"
enc_dir = "enc"

[tool.dotenvx-ops.envs]
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

**Note:** All env paths must be under `env_dir`. This is enforced to ensure gitignore protection.

## Design Principles

- **Safe by default** - `encrypt` only adds new keys, use `--update` to modify existing values
- **Non-destructive** - `decrypt` outputs to `latest/`, use `pull` to apply to working file
- **Validated** - Checks that all values are encrypted, env paths are protected
- **Confirmed** - Updates require explicit `y/N` confirmation

## License

MIT

## References

- [dotenvx Documentation](https://dotenvx.com/docs)
