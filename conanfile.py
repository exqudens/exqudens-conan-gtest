from os import path
from traceback import format_exc
from logging import error
from conans import ConanFile, tools


class ConanConfiguration(ConanFile):
    settings = "arch", "os", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": True}

    def set_name(self):
        try:
            self.name = tools.load(path.join(path.dirname(path.abspath(__file__)), "name-version.txt")).split(':')[0].strip()
        except Exception as e:
            error(format_exc())
            raise e

    def set_version(self):
        try:
            self.version = tools.load(path.join(path.dirname(path.abspath(__file__)), "name-version.txt")).split(':')[1].strip()
        except Exception as e:
            error(format_exc())
            raise e

    def package_info(self):
        try:
            self.cpp_info.names["cmake_find_package"] = "GTest"
            self.cpp_info.libs = tools.collect_libs(self)
        except Exception as e:
            error(format_exc())
            raise e


if __name__ == "__main__":
    pass
