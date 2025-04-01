import asyncio
import aiofiles
import shutil
import logging
from pathlib import Path
import argparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def copy_file(src: Path, dest_dir: Path):
    """Копіює файл у відповідну папку на основі його розширення."""
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / src.name
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, src, dest_file)
        logging.info(f"Копійовано: {src} -> {dest_file}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні {src}: {e}")


async def read_folder(source: Path, destination: Path):
    """Асинхронно читає всі файли у вихідній папці та розподіляє їх за розширеннями."""
    tasks = []
    for file in source.rglob("*"):
        if file.is_file():
            ext = file.suffix[1:] if file.suffix else "no_extension"
            dest_folder = destination / ext
            tasks.append(copy_file(file, dest_folder))
    await asyncio.gather(*tasks)


async def main():
    """Головна асинхронна функція, яка обробляє аргументи та запускає сортування файлів."""
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("destination", type=str, help="Шлях до папки призначення")

    args = parser.parse_args()
    source = Path(args.source).resolve()
    destination = Path(args.destination).resolve()

    if not source.is_dir():
        logging.error("Вказана вихідна папка не існує.")
        return

    await read_folder(source, destination)


if __name__ == "__main__":
    asyncio.run(main())
