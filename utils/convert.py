import subprocess
from pathlib import Path


def oda_converter(converter_path: Path, input_dir: Path, output_dir: Path,
            out_format="DXF", input_filter = "*.DWG", out_ver = "ACAD2018",
            recursive = "0", audit = "1") -> None:
    """
    Конвертация файлов AutoCAD.
    :param converter_path: path to oda converter
    :param input_dir: input directory
    :param output_dir: output directory
    :param out_format: Output file type: DWG, DXF, DXB
    :param input_filter: (Optional) Input files filter: *.DWG, *.DXF
    :param out_ver: Output version: ACAD9, ACAD10, ACAD12, ACAD14, ACAD2000, ACAD2004, ACAD2007, ACAD20010, ACAD2013, ACAD2018
    :param recursive: Recurse Input Folder: 0, 1
    :param audit: Audit each file: 0, 1
    :return: None
    """

    cmd = [converter_path, input_dir, output_dir, out_ver, out_format, recursive, audit, input_filter]
    subprocess.run(cmd, shell=True)
