# python-compile

Compile python apps to linux executables using docker.

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)
[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

![image](https://github.com/zackees/python-compile/assets/6856673/108c9af7-2a6f-4388-a2f3-d05aa826990e)




This project will use docker to compile your one file python app into a binary that's runnable on many
linux systems. This is the easiest way to build an app and may work directly out of the box for many setups.

Work in progress remains for building Windows/MacOS apps via the docker system.

*Example*

```bash
python-compile --os debian --input demo_http_server.py --requirements requirements.txt
```

[demo_http_server](https://github.com/zackees/python-compile/blob/main/src/python_compile/assets/demo_http_server.py)

# Notes

Right now we use the nuitka build. If you want custom build options then feel free to create a PR.

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.

# Links

  * Cross compiler toolchain images in linux:
    * https://github.com/dockcross/dockcross
  * MacOS images
    * https://hub.docker.com/r/sickcodes/docker-osx

# Releases
  * 1.0.11: Os path cleanup
  * 1.0.9: Better support for `ubuntu`
  * 1.0.8: Enables experimental `ubuntu` docker image support.
  * 1.0.7: Implement wheel support for the docker images.
  * 1.0.6: Better support for package isolation for native builds.
  * 1.0.5: You may now omit the `--os` parameter and compile against the current system.
  * 1.0.4: Fix
  * 1.0.3: Native windows compile is available if the host is also windows.