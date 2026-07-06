# Building MarOMarker executables

MarOMarker is bundled into a standalone application with
[PyInstaller](https://pyinstaller.org) using the versioned
`maromarker.spec` file.

## Important: no cross compilation

PyInstaller cannot build for a different operating system than the one it
runs on. To ship for all three platforms you have to run the build once on
each:

- a Windows machine produces `MarOMarker.exe`
- a macOS machine produces a `MarOMarker.app` bundle
- a Linux machine produces a `MarOMarker` executable folder

The same `maromarker.spec` works on all three. If you do not have all three
machines, the easiest option is GitHub Actions with a build matrix (see
`Automated builds` below).

## Building locally

From the `MarOMarker` directory, in the project virtual environment:

```
cd MarOMarker
pip install -e .[dev]
pyinstaller maromarker.spec
```

The result is a self contained folder in `MarOMarker/dist/MarOMarker/`. Start
the program with `dist/MarOMarker/MarOMarker` (`MarOMarker.exe` on Windows).
The folder can be zipped and shared; the target machine does not need Python
or any of the dependencies installed.

The build is large (TensorFlow alone is well over a gigabyte) and takes a
few minutes.

## Automated builds (all platforms from one place)

The repository contains a GitHub Actions workflow at
`.github/workflows/build.yml` (in the repository root) that builds Windows,
macOS and Linux apps in parallel, each on its own runner. This is the
recommended way to produce all three, since you do not need to own all three
machines.

### Creating a new version

1. Make sure the code you want to release is on `master` (merge your branch
   and push it).

2. Bump the version in `MarOMarker/pyproject.toml` and
   `MarOMarker/src/maromarker/__init__.py` (both hold `version` /
   `__version__`), commit and push.

3. Tag the commit and push the tag. The tag must start with `v`:

   ```
   git tag v3.0.0
   git push origin v3.0.0
   ```

4. Pushing the tag starts the `build` workflow automatically. Watch it under
   the repository's **Actions** tab on GitHub.

5. When it finishes (around 10 to 20 minutes), open the completed run and
   download the three artifacts from the **Artifacts** section:
   `MarOMarker-windows-latest`, `MarOMarker-macos-latest` and
   `MarOMarker-ubuntu-latest`. Each is a zip of the ready to run application
   folder.

You can also start a build without tagging: on the **Actions** tab pick the
**build** workflow and use **Run workflow** (this is the `workflow_dispatch`
trigger).

### First-time setup

GitHub Actions is enabled by default for a repository. The only requirement
is that the code, the `maromarker.spec` file and the workflow are pushed to
GitHub.
