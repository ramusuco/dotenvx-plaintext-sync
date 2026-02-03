import shutil
import logging
import sys
from dotenvx_plaintext_sync.lib.paths import prepare_paths
from dotenvx_plaintext_sync.lib.dotenvx_runner import run_decrypt
from dotenvx_plaintext_sync.lib.validation import validate_files, ensure_gitignore, ensure_encrypted_values, validate_environment
from dotenvx_plaintext_sync.lib.io_utils import open_file, cleanup_tmp

logger = logging.getLogger(__name__)


def main(target_env: str, apply: bool = False) -> None:
    logger.info(f"Extracting latest env for target environment: {target_env}")
    validate_environment(target_env)
    paths = prepare_paths(target_env)

    ensure_gitignore()
    validate_files([paths.key, paths.enc])

    try:
        shutil.copy(paths.enc, paths.work)

        run_decrypt(paths.work, paths.key)
        logger.info("Decrypted existing encrypted env file.")
        write_without_header(paths.work, paths.latest)
        logger.info(f"Wrote {paths.latest}")

        if apply:
            shutil.copy(paths.latest, paths.plain)
            logger.info(f"Applied to {paths.plain}")
    finally:
        cleanup_tmp([paths.work])
        logger.info("Cleaned up temporary files.")
        ensure_encrypted_values(paths.enc)


def pull(target_env: str) -> None:
    main(target_env, apply=True)


def write_without_header(
        work_enc_file: str,
        env_latest_file: str
) -> None:
    with open_file(work_enc_file, 'r') as src, open_file(env_latest_file, 'w') as out:
        started = False
        for line in src:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                if started:
                    out.write(line)
                continue
            if '=' not in line:
                if started:
                    out.write(line)
                continue
            key, _ = stripped.split('=', 1)
            if key.strip().startswith('DOTENV_'):
                continue
            if not started:
                started = True
            out.write(line)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(input("please enter target env: "))
