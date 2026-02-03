import logging
import os
from dotenvx_ops.config import get_config, GITIGNORE_PATH
from dotenvx_ops.lib.io_utils import open_file

logger = logging.getLogger(__name__)


def validate_files(files: list[str]) -> None:
    for file_path in files:
        file_existence_confirmation(file_path)


def file_existence_confirmation(file_path: str) -> None:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.info(f"File exists: {file_path}")


def ensure_encrypted_values(enc_file: str) -> None:
    cfg = get_config()
    with open_file(enc_file, "r") as f:
        for line in f:
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.strip().split("=", 1)
            if key.startswith("DOTENV_"):
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            if not value.startswith(cfg.encrypted_prefix):
                raise RuntimeError(
                    f"unencrypted value detected in {enc_file}: {line.strip()}"
                )


def ensure_gitignore() -> None:
    cfg = get_config()
    required = cfg.gitignore_required
    if not os.path.isfile(GITIGNORE_PATH):
        raise FileNotFoundError(f".gitignore not found: {GITIGNORE_PATH}")

    with open_file(GITIGNORE_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    norm_lines = {line.rstrip("/") for line in lines}

    missing = []
    for entry in required:
        if entry.rstrip("/") not in norm_lines:
            missing.append(entry)

    if missing:
        raise RuntimeError(f".gitignore lacks entries: {', '.join(missing)}")


def validate_environment(env: str) -> None:
    cfg = get_config()
    env = env.strip()
    if not env:
        raise ValueError("Environment is not set")
    if "/" in env or "\\" in env:
        raise ValueError("Environment format is invalid")
    if env not in cfg.envs:
        raise ValueError(
            f"Environment '{env}' is not recognized. Valid environments: {', '.join(cfg.env_names)}")
