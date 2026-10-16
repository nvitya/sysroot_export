#!/usr/bin/env python3
"""Export each sysroot and create a separate ZIP archive tagged with YYMMDD."""

from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import sys

export_dir = Path(__file__).resolve().parent / "exports"

# Adjust these:

SOURCE_ROOTS = (
    Path("/lindata/dev_arm/sysroot_armhf_trixie"),
    Path("/lindata/dev_arm/sysroot_arm64_trixie"),
    Path("/lindata/dev_riscv/sysroot_riscv64_trixie"),
)

date_tag = datetime.now().strftime("%y%m%d")


def export_directory(srcroot: Path, export_dir: Path, date_tag: str) -> None:

    # export the sysroot using the sysroot_export.py utility
    script_dir = Path(__file__).resolve().parent
    subprocess.run(
        [
            sys.executable,
            str(script_dir / "sysroot_export.py"),
            str(srcroot),
            str(export_dir / srcroot.name),
            "--clean",
        ],
        check=True,
    )

    # create date-tagged zip
    archive = shutil.make_archive(
        str(export_dir / f"{srcroot.name}_{date_tag}"),
        "zip",
        root_dir=export_dir,
        base_dir=srcroot.name,
    )
    print(f"Created: {archive}", flush=True)


def main() -> int:
    try:
        for srcroot in SOURCE_ROOTS:
            export_directory(srcroot, export_dir, date_tag)
    except subprocess.CalledProcessError as exc:
        SystemExit(exc.returncode)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return SystemExit(1)

main()
