# How To

##### Remove all packages

git-bash command line:
```
conan remove -f $(cat name-version.txt | cut -d ':' -f1 | xargs -I '{}' echo '{}')
```

##### Export windows packages

git-bash command line:
```
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | grep 'windows*' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | grep 'windows*' | xargs -I '{}' bash -c "cmake --build --preset {} --target conan-export || exit 255"
```

##### Export windows packages

git-bash command line:
```
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | grep 'linux*' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | grep 'linux*' | xargs -I '{}' bash -c "cmake --build --preset {} --target conan-export || exit 255"
```
