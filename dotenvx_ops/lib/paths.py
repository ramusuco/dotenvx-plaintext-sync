import os
from dataclasses import dataclass
from dotenvx_ops.config import get_config
from dotenvx_ops.lib.io_utils import ensure_dirs


@dataclass(frozen=True)
class EnvPaths:
    enc: str
    plain: str
    latest: str
    work: str
    key: str


def prepare_paths(target_env: str) -> EnvPaths:
    cfg = get_config()
    plain_path = cfg.get_env_path(target_env)
    plain_dir = os.path.dirname(plain_path)

    # Ensure directories exist (plain_dir may be empty if file is in root)
    dirs_to_create = [cfg.work_dir, cfg.latest_dir, cfg.enc_dir, cfg.keys_dir]
    if plain_dir:
        dirs_to_create.append(plain_dir)
    ensure_dirs(dirs_to_create)

    return EnvPaths(
        enc=os.path.join(cfg.enc_dir, f".env.{target_env}.enc"),
        plain=plain_path,
        latest=os.path.join(cfg.latest_dir, f".env.{target_env}"),
        work=os.path.join(cfg.work_dir, f".env.{target_env}.enc"),
        key=os.path.join(cfg.keys_dir, f"{target_env}.keys"),
    )
