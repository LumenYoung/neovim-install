"""
This script installs neovim on container system.
"""

import os
import argparse
from os.path import basename, expanduser
import shutil

# pylint: disable=import-outside-toplevel, unused-import, missing-function-docstring, literal-comparison, line-too-long, invalid-name, redefined-outer-name, broad-exception-caught

neovim_release_url = (
    "https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Neovim install specification")
    parser.add_argument(
        "-l",
        "--lunarvim",
        action="store_true",
        help="Specify whether to install lunarvim or not",
    )
    parser.add_argument("-r", "--rg", action="store_true", help="Install rigrep")
    parser.add_argument("-lg", "--lazygit", action="store_true", help="Install lazygit")

    args = parser.parse_args()

    # if args.language is not None:
    #     args.language = args.language.split(',')

    return args


def download_eget() -> None:
    """
    
    Download the eget executable into the current directory

    :return: If the command is successfully
    """

    try:
        os.system("")
    except Exception as e:
        print(e)
        return False

    return True





def request_is_installed() -> bool:
    """

    This function checks if request is installed or not.

    :return: bool
    """
    try:
        import requests

        print("Request is already installed")
        return True
    except ImportError:
        print("Request is not installed")
        return False


def curl_is_installed() -> bool:
    # Check if curl is installed, if installed, return true , if not, return false

    which_path = shutil.which("curl")

    if which_path is None:
        print("Curl is not installed")
        return False

    print("Curl is already installed")

    return True


def untar_neovim() -> bool:
    """

    untar_neovim into the ~/.local folder

    :return: [TODO:description]
    """

    tar_filename = basename(neovim_release_url)

    # get user home folder
    home_dir = expanduser("~")

    try:
        os.system(f"tar xf {tar_filename} {home_dir}/.local")
    except Exception as e:
        print(e)
        return False

    return True


def install_rg(download_mod: str) -> bool:
    rigrep_download_url = (
        "https://github.com/BurntSushi/ripgrep/releases/latest"
    )

    if download_mod == "curl":
        os.system(f"curl -LO {rigrep_download_url}")
    elif download_mod == "request":
        import requests

        response = requests.get(rigrep_download_url, timeout=30)

        if response.status_code == 200:
            with open("nvim-linux64.tar.gz", "wb") as f:
                f.write(response.content)
            print("File downloaded successfully.")
        else:
            print(f"Request failed with status code {response.status_code}.")

            return False

    return True


def install_neovim(download_mod: str) -> bool:
    assert download_mod in ["curl", "request"]

    if download_mod == "curl":
        os.system(f"curl -LO {neovim_release_url}")
    elif download_mod == "request":
        import requests

        response = requests.get(neovim_release_url, timeout=30)

        if response.status_code == 200:
            with open(f"{basename(neovim_release_url)}", "wb") as f:
                f.write(response.content)
            print("File downloaded successfully.")
        else:
            print(f"Request failed with status code {response.status_code}.")

            return False

    return True


if __name__ == "__main__":
    args = parse_args()

    download_mod = ""
    if curl_is_installed():
        download_mod = "curl"
    elif request_is_installed():
        download_mod = "request"
    else:
        print(
            "Neither curl nor request is avaliable on your OS, install it manually before run this script"
        )

    if install_neovim("request"):
        print("neovim downloaded")
    else:
        print("fail to download neovim")
