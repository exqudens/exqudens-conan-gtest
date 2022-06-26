# How To

##### Export all packages

git-bash command line:
```
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' cmake --preset '{}'
cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' cmake --build --preset '{}' --target conan-export
```
