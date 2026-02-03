import os
import sys
import shutil
import logging
from dotenvx_ops.lib.paths import prepare_paths
from dotenvx_ops.lib.dotenvx_runner import run_decrypt, run_encrypt
from dotenvx_ops.lib.validation import ensure_encrypted_values, ensure_gitignore, validate_files, validate_environment
from dotenvx_ops.lib.io_utils import load_env_file, load_enc_file, open_file, cleanup_tmp

logger = logging.getLogger(__name__)


def main(target_env: str) -> None:
    logger.info(f"Extracting latest env for target environment: {target_env}")
    validate_environment(target_env)
    paths = prepare_paths(target_env)

    ensure_gitignore()
    created_new_enc = ensure_encrypted_file_exists(paths.enc)

    if not created_new_enc:
        validate_files([paths.key, paths.enc, paths.plain])
    else:
        validate_files([paths.enc, paths.plain])

    try:
        if created_new_enc:
            shutil.copy(paths.plain, paths.work)
        else:
            shutil.copy(paths.enc, paths.work)
            run_decrypt(paths.work, paths.key)

        updated = True if created_new_enc else embed_difference(paths.plain, paths.work)
        if not updated:
            logger.info("No missing keys. Skipped re-encrypt.")
            return

        run_encrypt(paths.work, paths.key)
        logger.info("encrypted env file.")
        ensure_encrypted_values(paths.work)

        shutil.move(paths.work, paths.enc)
        logger.info("Updated encrypted env file.")

    finally:
        cleanup_tmp([paths.work])
        logger.info("Cleaned up temporary files.")
        ensure_encrypted_values(paths.enc)


def embed_difference(
        env_file: str,
        work_enc_file: str
) -> bool:

    load_env_data = load_env_file(env_file)
    load_work_enc_data = load_enc_file(work_enc_file)

    add_data = {k: v for k, v in load_env_data.items() if k not in load_work_enc_data}

    if not add_data:
        logger.warning("New keys is not found.")
        return False

    add_data_to_plain_file(add_data, work_enc_file)
    return True


def add_data_to_plain_file(
        add_data: dict,
        plain_file: str
) -> None:
    with open_file(plain_file, 'a') as f:
        for key, value in add_data.items():
            f.write(f"{key}={value}\n")
            logger.info(f"Added new key: {key}")


def ensure_encrypted_file_exists(enc_file: str) -> bool:
    if os.path.isfile(enc_file):
        return False
    with open_file(enc_file, 'w'):
        pass
    logger.info(f"created empty encrypted env file: {enc_file}")
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(input("please enter target env: "))
