"""
This script installs neovim on container system.
"""

import os
import sys
import argparse
from os.path import basename, expanduser
import shutil

# pylint: disable=import-outside-toplevel, unused-import, missing-function-docstring, literal-comparison, line-too-long, invalid-name, redefined-outer-name, broad-exception-caught


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Neovim install specification")
    parser.add_argument(
        "-lvim",
        "--lunarvim",
        action="store_true",
        help="Specify whether to install lunarvim or not",
    )
    parser.add_argument("-r", "--rg", action="store_true", help="Install rigrep")
    parser.add_argument("-l", "--lg", action="store_true", help="Install lazygit")
    parser.add_argument("-a", "--all", action="store_true", help="Install all")

    args = parser.parse_args()

    # if args.language is not None:
    #     args.language = args.language.split(',')

    return args


def user_path_is_in_path() -> bool:
    user_bin = expanduser("~/.local/bin")

    path = os.environ["PATH"].split(os.pathsep)

    if user_bin not in path:
        print("User bin is not in path")
        return False

    return True


def download_eget() -> bool:
    """

    Download the eget executable into the current directory

    :return: If the command is successfully
    """

    try:
        os.system("curl https://zyedidia.github.io/eget.sh | sh")
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


def install_rg() -> bool:
    user_local_bin = expanduser("~/.local/bin")

    try:
        os.system(f"./eget BurntSushi/ripgrep --to {user_local_bin}")
    except Exception as e:
        print(e)
        return False

    return True


def install_lg() -> bool:
    user_local_bin = expanduser("~/.local/bin")

    try:
        os.system(f"./eget jesseduffield/lazygit --to {user_local_bin}")
    except Exception as e:
        print(e)
        return False

    return True

def install_tree_sitter() -> bool:
    user_local_bin = expanduser("~/.local/bin")

    try:
        os.system(f"./eget tree_sitter/tree_sitter --to {user_local_bin}")
    except Exception as e:
        print(e)
        return False

    return True


def install_fd() -> bool:
    user_local_bin = expanduser("~/.local/bin")

    try:
        os.system(f"./eget sharkdp/fd --asset linux-gnu --to {user_local_bin}")
    except Exception as e:
        print(e)
        return False

    return True


def install_neovim() -> bool:
    user_local = expanduser("~/.local")

    neovim_release_url = (
        "https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz"
    )

    asset_name = basename(neovim_release_url)

    if not shutil.which("tar"):
        print("tar is not installed, please install it before run this script")
        return False

    try:
        os.system(
            f"curl -OL {neovim_release_url}  && tar xf {asset_name} --strip-components=1 -C {user_local}"
        )

    except Exception as e:
        print(e)
        return False

    return True


if __name__ == "__main__":
    args = parse_args()

    user_local_bin = expanduser("~/.local/bin")

    if not os.path.exists(user_local_bin):
        os.makedirs(user_local_bin)

    # if curl_is_installed():
    #     download_mod = "curl"
    # elif request_is_installed():
    #     download_mod = "request"
    # else:
    #     print(
    #         "Neither curl nor request is avaliable on your OS, install it manually before run this script"
    #     )

    assert (
        curl_is_installed()
    ), "Curl is not installed, please install it before run this script"

    if install_neovim():
        print("neovim downloaded")
    else:
        print("fail to download neovim")

    if not user_path_is_in_path():
        print("User bin is not in path, please add it to your path with the following:")
        print(f"export PATH=$PATH:{user_local_bin}")

    if args.all:
        if not download_eget():
            print("Fail to download eget")
            sys.exit(1)

        if not install_rg():
            print("Fail to install ripgrep")
            sys.exit(1)

        if not install_lg():
            print("Fail to install lazygit")
            sys.exit(1)

        if not install_fd():
            print("Fail to install fd")
            sys.exit(1)

        if not install_tree_sitter():
            print("Fail to install tree-sitter")
            sys.exit(1)

        print("Lunarvim requies interactive installation. Execute the following code:")
        print(
            "bash <(curl -s https://raw.githubusercontent.com/lunarvim/lunarvim/master/utils/installer/install.sh)"
        )

        sys.exit("Successfully installed all")

    if args.lunarvim:
        print("Lunarvim requies interactive installation. Execute the following code:")
        print(
            "bash <(curl -s https://raw.githubusercontent.com/lunarvim/lunarvim/master/utils/installer/install.sh)"
        )
        print(
            "It is adviced to install ripgrep and lazygit before execution, you can use this scrip with -r and -lg to easily install them"
        )

    if args.rg:
        if not download_eget():
            print("Fail to download eget")
            sys.exit(1)

        if not install_rg():
            print("Fail to install ripgrep")
            sys.exit(1)

    if args.lg:
        if not download_eget():
            print("Fail to download eget")
            sys.exit(1)

        if not install_lg():
            print("Fail to install lazygit")
            sys.exit(1)
