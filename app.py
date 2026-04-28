import os
import re
from pathlib import Path

# =========================
# CONFIG (EDIT PER SHOW)
# =========================
CONFIG = {
    "directory": r"C:\Handbrakes\Compressed",
    "show_name": "EarthWorm Jim",
    "season": 1,
    "pattern": "{show} S{season:02}E{episode:02}",
    "start_episode": 1,
    "dry_run": False,  # set False when ready to rename
    "extensions": [".mp4", ".mkv", ".avi"]
}

# =========================
# HELPERS
# =========================
def natural_sort(files):
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key.name)]

    return sorted(files, key=alphanum_key)


def get_files(directory, extensions):
    return [
        f for f in Path(directory).iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    ]


# =========================
# RENAMING LOGIC
# =========================
def rename_files():
    directory = CONFIG["directory"]
    show = CONFIG["show_name"]
    season = CONFIG["season"]
    pattern = CONFIG["pattern"]
    start_ep = CONFIG["start_episode"]
    dry_run = CONFIG["dry_run"]

    files = get_files(directory, CONFIG["extensions"])
    files = natural_sort(files)

    print(f"\nFound {len(files)} files\n")

    for idx, file in enumerate(files, start=start_ep):
        new_name = pattern.format(
            show=show,
            season=season,
            episode=idx
        )

        new_file = file.with_name(new_name + file.suffix)

        print(f"{file.name}  -->  {new_file.name}")

        if not dry_run:
            os.rename(file, new_file)

    print("\nDone.")
    if dry_run:
        print("⚠️ DRY RUN enabled — no files were changed.")


if __name__ == "__main__":
    rename_files()