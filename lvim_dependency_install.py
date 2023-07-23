import os
import pathlib
from shutil import which

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Neovim install specification")
    parser.add_argument(
        "-lvim",
        "--lunarvim",
        action="store_true",
        help="Specify whether to install lunarvim or not",
    )
    parser.add_argument(
        "-c",
        "--conservative",
        action="store_true",
        help="Not install base program lanaguge manager if not found",
    )

    args = parser.parse_args()
    return args


def get_pkg_manager() -> str:
    # check if apt is installed on the system
    if which("apt") is not None:
        return "apt"
    elif which("pacman") is not None:
        return "pacman"
    elif which("dnf") is not None:
        return "dnf"
    elif which("yum") is not None:
        return "yum"
    elif which("zypper") is not None:
        return "zypper"
    elif which("apk") is not None:
        return "apk"

    print("No package manager found on the system")
    return None


def pip_installed(args) -> bool:
    # check if pip3 is installed on the system
    if which("pip3") is not None:
        return True
    elif args.conservative:
        return False
    elif get_pkg_manager() is not None:
        pkg_manager = get_pkg_manager()
        if pkg_manager == "apt":
            try:
                os.system("sudo apt update; sudo apt install -y python3-pip")
                return True
            except:
                print("Error installing pip3")
                return False
        elif pkg_manager == "pacman":
            try:
                os.system("sudo pamcan -Sy; sudo pacman -S python-pip --noconfirm")
                return True
            except:
                print("Error installing pip3")
                return False
        elif pkg_manager == "yum":
            try:
                os.system("sudo yum install -y python3-pip")
            except:
                print("Error installing pip3")
                return False

        elif pkg_manager == "dnf":
            raise NotImplementedError
        elif pkg_manager == "zypper":
            raise NotImplementedError
        elif pkg_manager == "apk":
            raise NotImplementedError

    print("pip3 is not installed on the system, please install it manually")
    return False


def cargo_installed(args):
    if which("cargo") is not None:
        return True
    elif args.conservative:
        return False

    if which("curl") is None:
        print("curl is not installed on the system, please install it manually")
        return False

    try:
        os.system("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
        return True
    except:
        print("Error installing rustup")
        return False

    return False


def node_installed(args):
    if which("node") is not None:
        return True
    elif args.conservative:
        return False
    elif get_pkg_manager() is not None:
        pkg_manager = get_pkg_manager()
        if pkg_manager == "apt":
            try:
                os.system("sudo apt update; sudo apt install nodejs")
                return True
            except:
                print("Error installing nodejs")
                return False
        elif pkg_manager == "pacman":
            try:
                os.system("sudo pamcan -Sy; sudo pacman -S nodejs npm --noconfirm")
                return True
            except:
                print("Error installing nodejs")
                return False
        elif pkg_manager == "dnf":
            raise NotImplementedError
        elif pkg_manager == "yum":
            raise NotImplementedError
        elif pkg_manager == "zypper":
            raise NotImplementedError
        elif pkg_manager == "apk":
            raise NotImplementedError

    return False


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
    # get args
    args = parse_args()
    if not pip_installed(args):
        print("pip3 is not installed on the system, please install it manually")
        return
    elif not cargo_installed(args):
        print("cargo is not installed on the system, please install it manually")
        return
    elif not node_installed(args):
        print("nodejs is not installed on the system, please install it manually")
        return

    # install neovim
    if not install_neovim():
        print("Error installing neovim")
        return
