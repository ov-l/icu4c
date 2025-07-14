
from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path



def cpp_byte_array(name: str, blob: bytes, indent: int = 2,
                   line_width: int = 120) -> str:
    """Return *blob* formatted as a C array initialiser."""
    hex_bytes = [str(b) for b in blob]
    joined    = ", ".join(hex_bytes)
    wrapper   = textwrap.TextWrapper(width=line_width,
                                     initial_indent=" " * indent,
                                     subsequent_indent=" " * indent)
    return wrapper.fill(joined)


SUBSET_FILES = [
    "i18n/scriptset.cpp",
    "i18n/scriptset.h",
    "i18n/ucln_in.cpp",
    "i18n/ucln_in.h",
    "i18n/uspoof.cpp",
    "i18n/uspoof_impl.cpp",
    "i18n/uspoof_impl.h",
    "i18n/unicode/uspoof.h",
]

def vendor_headers_and_sources(icu_source: Path, dest_root: Path) -> None:
    """
    Copy the subset of ICU headers/sources required by your engine into *dest_root*.
    """
    print("→ Vendoring selected headers / sources")

    # 1. Entire common/
    shutil.copytree(icu_source / "common", dest_root / "common",
                    dirs_exist_ok=True)

    # 2. Individual files from i18n/
    for rel in SUBSET_FILES:
        src = icu_source / rel
        dst = dest_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    # 3. Top-level LICENSE
    shutil.copy2(icu_source.parent / "LICENSE", dest_root)
    

def embed_dat_as_cpp(dat_path: Path, dest_cpp: Path) -> None:
    """
    Generate a single C++ translation unit with the binary data embedded
    as an `unsigned char[]`.
    """
    blob = dat_path.read_bytes()
    array = cpp_byte_array("U_ICUDATA_ENTRY_POINT", blob)

    dest_cpp.write_text(textwrap.dedent(f"""\
        /* (C) 2016 and later: Unicode, Inc. and others.
           License & terms of use: https://www.unicode.org/copyright.html */
        #include <unicode/utypes.h>
        #include <unicode/udata.h>

        extern "C" U_EXPORT const size_t U_ICUDATA_SIZE = {len(blob)};
        extern "C" U_EXPORT const unsigned char U_ICUDATA_ENTRY_POINT[] = {{
        {array}
        }};
        """))
    print(f"✓ Embedded data         → {dest_cpp}")
    
    
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("--dat-path", type=Path, default=Path("icudt77l.dat"),
                   help="Data file path")
    p.add_argument("--engine-root", type=Path, default=Path("./"),
                   help="Where to copy headers, sources and .dat")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    dest_root: Path = args.engine_root.resolve()
    dest_root.mkdir(parents=True, exist_ok=True)
    
    dat_path: Path = args.dat_path.resolve()

    # ------------------------------------------------------------------ vendor sources
    # (re-use the build tree for file copying; it’s still around)
    icu_src = Path("temp/icu/source").resolve()
    vendor_headers_and_sources(icu_src, dest_root)

    # ------------------------------------------------------------------ optional C++ embed
    embed_dat_as_cpp(dat_path, dest_root / "icudata.gen.cpp")

    print("\n🎉  ICU update complete!")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(f"\n❌ Command failed: {exc.cmd}\n")
        sys.exit(exc.returncode)    