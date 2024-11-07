# Android Git Scanner

This tool is a helper for [Odex Patcher](https://github.com/giacomoferretti/odex-patcher)

## Installation

1. Clone repository

    ```shell
    git clone https://github.com/giacomoferretti/android-git-scanner
    ```

2. Install dependencies

    ```shell
    poetry install
    ```

## Extract OAT versions

1. Clone `art` repository ~513MB (Skip if already cloned)

    ```shell
    git clone https://android.googlesource.com/platform/art android-art
    ```

2. Run scanner

    ```shell
    poetry run ags oat android-art
    ```

## Extract VDEX versions

1. Clone `art` repository ~513MB (skip if already cloned)

    ```shell
    git clone https://android.googlesource.com/platform/art android-art
    ```

2. Run scanner

    ```shell
    poetry run ags vdex android-art
    ```