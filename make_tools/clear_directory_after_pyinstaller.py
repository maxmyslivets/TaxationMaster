import os
import shutil
from pathlib import Path


def process_directories(base_directory: Path):
    """
    Ищет папку bin, удаляет её, переименовывает dist в bin,
    и удаляет папку build в указанной директории.

    :param base_directory: Путь к корневой директории для обработки.
    """
    bin_dir = base_directory / "bin"
    dist_dir = base_directory / "dist"
    build_dir = base_directory / "build"
    spec_file = base_directory / "TaxationTool.spec"

    # Удаление папки bin, если она существует
    if os.path.isdir(bin_dir):
        print(f"Удаление папки: {bin_dir}")
        shutil.rmtree(bin_dir)
    else:
        print(f"Папка bin не найдена: {bin_dir}")

    # Переименование папки dist в bin, если dist существует
    if os.path.isdir(dist_dir):
        print(f"Переименование {dist_dir} в {bin_dir}")
        os.rename(dist_dir, bin_dir)
    else:
        print(f"Папка dist не найдена: {dist_dir}")

    # Удаление папки build, если она существует
    if os.path.isdir(build_dir):
        print(f"Удаление папки: {build_dir}")
        shutil.rmtree(build_dir)
    else:
        print(f"Папка build не найдена: {build_dir}")

    # Удаление .spec файла, если он существует
    if spec_file.name in os.listdir(base_directory):
        print(f"Удаление spec файла: {spec_file}")
        os.remove(spec_file)
    else:
        print(f"Файл spec не найден: {spec_file}")


if __name__ == "__main__":
    base_dir = Path("")
    process_directories(base_dir)
