import os
from typing import TextIO


def open_file(path: str, mode: str) -> TextIO:
    if mode == "w":
        return open(path, mode, encoding="utf-8", newline="")
    return open(path, mode, encoding="utf-8")


def load_kv_file(file_path: str) -> dict:
    kv_data: dict[str, str] = {}
    with open_file(file_path, "r") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            key, value = s.split("=", 1)
            kv_data[key.strip()] = value.strip()
    return kv_data


load_env_file = load_kv_file
load_enc_file = load_kv_file


def cleanup_tmp(paths: list[str]) -> None:
    for file_path in paths:
        if os.path.isfile(file_path):
            os.remove(file_path)


def ensure_dirs(dirs) -> None:
    for d in dirs:
        os.makedirs(d, exist_ok=True)
