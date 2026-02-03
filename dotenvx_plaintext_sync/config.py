import json
import os
from dataclasses import dataclass, field
from typing import Self

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


CONFIG_FILE = "dotenvx-ops.json"
PYPROJECT_FILE = "pyproject.toml"


DEFAULT_ENVS: dict[str, str] = {
    "development": "envs/.env.development",
    "staging": "envs/.env.staging",
    "production": "envs/.env.production",
}


@dataclass
class Config:
    env_dir: str = "envs"
    envs: dict[str, str] = field(default_factory=lambda: DEFAULT_ENVS.copy())
    enc_dir: str = "enc"
    work_dir: str = "tmp/dotenvx-ops"
    keys_dir: str = ""
    latest_dir: str = ""
    encrypted_prefix: str = "encrypted:"

    def __post_init__(self) -> None:
        # Set default keys_dir and latest_dir based on env_dir if not specified
        if not self.keys_dir:
            self.keys_dir = f"{self.env_dir}/keys"
        if not self.latest_dir:
            self.latest_dir = f"{self.env_dir}/latest"

    @classmethod
    def load(cls) -> Self:
        config: Self
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            config = cls._from_dict(data)
        elif os.path.isfile(PYPROJECT_FILE):
            with open(PYPROJECT_FILE, "rb") as f:
                pyproject = tomllib.load(f)
            if "tool" in pyproject and "dotenvx-ops" in pyproject["tool"]:
                config = cls._from_dict(pyproject["tool"]["dotenvx-ops"])
            else:
                config = cls()
        else:
            config = cls()

        config.validate_env_paths()
        return config

    @classmethod
    def _from_dict(cls, data: dict) -> Self:
        env_dir = data.get("env_dir", "envs")
        return cls(
            env_dir=env_dir,
            envs=data.get("envs", DEFAULT_ENVS.copy()),
            enc_dir=data.get("enc_dir", "enc"),
            work_dir=data.get("work_dir", "tmp/dotenvx-ops"),
            keys_dir=data.get("keys_dir", ""),
            latest_dir=data.get("latest_dir", ""),
            encrypted_prefix=data.get("encrypted_prefix", "encrypted:"),
        )

    @property
    def env_names(self) -> list[str]:
        """List of environment names (keys of envs dict)"""
        return list(self.envs.keys())

    def get_env_path(self, env: str) -> str:
        """Get the plain env file path for a given environment"""
        if env not in self.envs:
            raise ValueError(f"Environment '{env}' is not defined")
        return self.envs[env]

    def validate_env_paths(self) -> None:
        """Validate that all env paths are under env_dir"""
        env_dir_normalized = self.env_dir.replace("\\", "/").rstrip("/")
        invalid_paths = []
        for name, path in self.envs.items():
            path_normalized = path.replace("\\", "/")
            if not path_normalized.startswith(f"{env_dir_normalized}/"):
                invalid_paths.append(f'  "{name}": "{path}"')
        if invalid_paths:
            raise ValueError(
                f"All env paths must be under '{self.env_dir}/'.\n"
                f"Invalid paths:\n" + "\n".join(invalid_paths)
            )

    @property
    def gitignore_required(self) -> list[str]:
        return [f"{self.env_dir}/*", f"{self.work_dir}/*"]


_config: Config | None = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def reload_config() -> Config:
    global _config
    _config = Config.load()
    return _config


GITIGNORE_PATH = ".gitignore"
