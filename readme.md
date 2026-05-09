# exqudens-conan-gtest

## how-to-create-github-conan-package

1. `cmake -P cmake/util.cmake -- conan_create_github_package NAME github-gtest VERSION 1.11.0 URL https://github.com/google/googletest/archive/refs/tags/release-1.11.0.zip EXPECTED_MD5 52943a59cefce0ae0491d4d2412c120b`
1. *(optional)* check `conan list 'github-gtest/1.11.0:*'`
1. *(optional)* check ``conan cache path 'github-gtest/1.11.0:${conan list-output-packages[0]}'``
1. *(optional)* check ``ls -1a ${conan-cache-path-output}``
1. *(optional)* `conan upload github-gtest/1.11.0 --remote gitlab`

## how-to-test-all-presets

1. `git clean -xdf`
1. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
1. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target cmake-test || exit 255"`

## how-to-build-all-presets

1. `git clean -xdf`
1. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
1. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target cmake-install || exit 255"`

## how-to-export-all-presets

1. `conan list 'gtest/*'`
1. `conan remove -c 'gtest'`
1. `git clean -xdf`
1. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
1. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target conan-export || exit 255"`

## vscode

1. `git clean -xdf`
1. `cmake --preset ${preset}`
1. `cmake --build --preset ${preset} --target vscode`
1. use vscode debugger launch configurations: `cppvsdbg-test-app`, `cppdbg-test-app`

### extensions

For `command-variable-launch.json`
use [Command Variable](https://marketplace.visualstudio.com/items?itemName=rioj7.command-variable#pickstringremember) `version >= v1.69.0`

