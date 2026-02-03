import json
import os
import logging

from dotenvx_ops.config import Config, CONFIG_FILE, GITIGNORE_PATH

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "env_dir": "envs",
    "envs": {
        "development": "envs/.env.development",
        "staging": "envs/.env.staging",
        "production": "envs/.env.production",
    },
    "enc_dir": "enc",
    "work_dir": "tmp/dotenvx-ops",
}


def run_init() -> None:
    create_config_file()
    create_directories()
    update_gitignore()
    logger.info("dotenvx-ops initialized successfully!")
    logger.info(f"Edit {CONFIG_FILE} to customize settings.")


def create_config_file() -> None:
    if os.path.isfile(CONFIG_FILE):
        logger.info(f"{CONFIG_FILE} already exists, skipping.")
        return

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
        f.write("\n")
    logger.info(f"Created {CONFIG_FILE}")


def create_directories() -> None:
    cfg = Config._from_dict(DEFAULT_CONFIG)
    dirs = [cfg.enc_dir]

    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
            logger.info(f"Created directory: {d}")
            gitkeep = os.path.join(d, ".gitkeep")
            if not os.path.isfile(gitkeep):
                with open(gitkeep, "w") as f:
                    pass


def update_gitignore() -> None:
    cfg = Config._from_dict(DEFAULT_CONFIG)
    required = cfg.gitignore_required

    existing_lines: set[str] = set()
    if os.path.isfile(GITIGNORE_PATH):
        with open(GITIGNORE_PATH, "r", encoding="utf-8") as f:
            existing_lines = {line.strip().rstrip("/") for line in f if line.strip()}

    to_add = [entry for entry in required if entry.rstrip("/") not in existing_lines]

    if not to_add:
        logger.info(".gitignore already has required entries.")
        return

    with open(GITIGNORE_PATH, "a", encoding="utf-8") as f:
        f.write("\n# dotenvx-ops\n")
        for entry in to_add:
            f.write(f"{entry}\n")
            logger.info(f"Added to .gitignore: {entry}")
