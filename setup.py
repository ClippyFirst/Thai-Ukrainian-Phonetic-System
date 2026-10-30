"""Setuptools build hook that packages only runtime-required registries."""
from __future__ import annotations

from pathlib import Path
from shutil import copy2, copytree

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildPyWithRuntimeData(build_py):
    def run(self) -> None:
        super().run()
        repository_root = Path(__file__).resolve().parent
        package_data_root = Path(self.build_lib) / "thai_ukrainian" / "_data"
        copytree(repository_root / "data" / "thai", package_data_root / "thai", dirs_exist_ok=True)
        copy2(repository_root / "data" / "ua_target_vectors.csv", package_data_root / "ua_target_vectors.csv")

    def get_outputs(self, include_bytecode: int = 1) -> list[str]:
        outputs = super().get_outputs(include_bytecode)
        package_data_root = Path(self.build_lib) / "thai_ukrainian" / "_data"
        if package_data_root.is_dir():
            outputs.extend(str(path) for path in package_data_root.rglob("*") if path.is_file())
        return outputs


setup(cmdclass={"build_py": BuildPyWithRuntimeData})
