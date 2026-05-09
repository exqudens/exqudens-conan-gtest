from pathlib import Path

required_conan_version = ">=2.0"

from conan import ConanFile
from conan.tools.files import copy

class ConanConfiguration(ConanFile):

    def requirements(self):
        try:
            if self.user and self.channel:
                self.requires(f"github-gtest/1.11.0@{self.user}/{self.channel}")
            else:
                self.requires("github-gtest/1.11.0")
        except Exception as e:
            self.output.error(e)
            raise e

    def generate(self):
        try:
            for dep in self.dependencies.values():
                copy(self, pattern="*", src=Path(dep.package_folder).as_posix(), dst=Path(self.build_folder).as_posix())
        except Exception as e:
            self.output.error(e)
            raise e
