import logging
import subprocess

logger = logging.getLogger(__name__)


def run_decrypt(enc_file: str, key_path: str) -> None:
    try:
        subprocess.run(
            ["dotenvx", "decrypt", "-fk", key_path, "-f", enc_file],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        logger.error(f"decrypt failed: {stderr}")
        raise


def run_encrypt(plain_file: str, key_path: str) -> None:
    try:
        subprocess.run(
            ["dotenvx", "encrypt", "-fk", key_path, "-f", plain_file],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        logger.error(f"encrypt failed: {stderr}")
        raise
