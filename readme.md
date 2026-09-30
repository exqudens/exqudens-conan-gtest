# exqudens-conan-gtest

## cmake-variables

01. `-DCMAKE_UTIL_ONLY=1` to download `util.cmake` file only.

## how-to-create-github-conan-package

01. `cmake -DCMAKE_UTIL_ONLY=1 --preset windows.ninja.msvc-x64-x64.debug.shared`
01. `cmake -P build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake -- conan_export_pkg_zip ZIP_FILE_URL https://github.com/google/googletest/archive/refs/tags/release-1.11.0.zip EXPECTED_MD5 52943a59cefce0ae0491d4d2412c120b NAME github-gtest VERSION 1.11.0 USER exqudens CHANNEL development CHECK_FILE googletest-release-1.11.0/README.md`
01. *(optional)* check `conan list 'github-gtest/1.11.0:*'`
01. *(optional)* check ``conan cache path 'github-gtest/1.11.0:${conan list-output-packages[0]}'``
01. *(optional)* check ``ls -1a ${conan-cache-path-output}``
01. *(optional)* `conan upload github-gtest/1.11.0 --remote gitlab`

## how-to-test-all-presets

01. `git clean -xdf`
01. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
01. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target cmake-test || exit 255"`

## how-to-build-all-presets

01. `git clean -xdf`
01. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
01. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target cmake-install || exit 255"`

## how-to-export-all-presets

01. `conan list 'gtest/*'`
01. `conan remove -c 'gtest'`
01. `git clean -xdf`
01. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
01. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target conan-export || exit 255"`

## vscode

01. `git clean -xdf`
01. `cmake --preset ${preset}`
01. `cmake --build --preset ${preset} --target vscode`
01. use vscode debugger launch configurations: `cppvsdbg-test-app`, `cppdbg-test-app`

### extensions

01. For `command-variable-launch.json` use [Command Variable](https://marketplace.visualstudio.com/items?itemName=rioj7.command-variable#pickstringremember) `version >= v1.69.0`

