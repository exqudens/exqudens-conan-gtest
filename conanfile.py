from pathlib import Path
from logging import error


required_conan_version = ">=2.0"


from conan import ConanFile
from conan.tools.files import collect_libs, copy


class ConanConfiguration(ConanFile):
    settings = "arch", "os", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": True}

    def set_name(self):
        try:
            self.name = Path(__file__).parent.joinpath("name-version.txt").read_text().split(':')[0].strip()
        except Exception as e:
            error(e, exc_info=True)
            raise e

    def set_version(self):
        try:
            self.version = Path(__file__).parent.joinpath("name-version.txt").read_text().split(':')[1].strip()
        except Exception as e:
            error(e, exc_info=True)
            raise e

    def package(self):
        try:
            copy(self, pattern="*.*", excludes="*.bat", src=self.build_folder, dst=self.package_folder)
        except Exception as e:
            error(e, exc_info=True)
            raise e

    def package_info(self):
        try:
            self.cpp_info.set_property("cmake_file_name", "GTest")
            self.cpp_info.libs = collect_libs(self)
        except Exception as e:
            error(e, exc_info=True)
            raise e


if __name__ == "__main__":
    pass
