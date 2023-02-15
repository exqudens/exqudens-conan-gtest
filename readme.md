# How To

##### Export all packages

git-bash command line:
```
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | grep 'windows*' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | grep 'windows*' | xargs -I '{}' bash -c "cmake --build --preset {} --target conan-export || exit 255"
```
