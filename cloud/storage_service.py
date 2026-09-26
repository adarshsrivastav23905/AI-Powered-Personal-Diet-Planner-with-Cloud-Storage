"""Cloud storage simulation utilities.

This file demonstrates the difference between structured database records and
unstructured file storage in a cloud environment.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List


class CloudStorageService:
    """Simulates cloud storage using a local user-scoped folder structure."""

    def __init__(self, base_dir: str = "cloud_storage"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def user_folder(self, user_id: str) -> Path:
        folder = self.base_dir / user_id
        folder.mkdir(exist_ok=True)
        return folder

    def upload_file(self, user_id: str, filename: str, content: bytes):
        folder = self.user_folder(user_id)
        target = folder / filename
        target.write_bytes(content)
        return str(target)

    def list_files(self, user_id: str) -> List[str]:
        folder = self.user_folder(user_id)
        return [str(p.name) for p in folder.iterdir() if p.is_file()]

    def delete_file(self, user_id: str, filename: str) -> bool:
        path = self.user_folder(user_id) / filename
        if path.exists():
            path.unlink()
            return True
        return False
