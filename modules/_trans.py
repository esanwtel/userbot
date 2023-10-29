
import re
import subprocess
import typing
from contextlib import suppress
from emoji import replace_emoji
from string import ascii_letters, ascii_uppercase, ascii_lowercase
from markdown.core import markdown
from bs4 import BeautifulSoup


def import_lib(
    lib_name: str,
    pkg_name: typing.Optional[str] = None,
) -> typing.Any:
    from importlib import import_module

    if pkg_name is None:
        pkg_name = lib_name
    lib_name = re.sub(r"(=|>|<|~).*", "", lib_name)
    try:
        return import_module(lib_name)
    except ImportError:
        done = subprocess.run(["python3", "-m", "pip", "install", "--no-cache-dir", "-U", pkg_name])
        if done.returncode != 0:
            raise AssertionError(f"Failed to install library {pkg_name} (pip exited with code {done.returncode})")
        return import_module(lib_name)


def replace_all(
    text: str,
    repls: dict,
    regex: bool = False,
) -> str:
    if regex:
        return reduce(lambda a, kv: re.sub(*kv, a, flags=re.I), repls.items(), text)
    return reduce(lambda a, kv: a.replace(*kv), repls.items(), text)

def strip_format(text: str) -> str:
    repls = {
        "~~": "",
        "--": "",
        "__": "",
        "||": "",
    }
    return replace_all(BeautifulSoup(markdown(text), features="html.parser").get_text(), repls).strip()


def strip_emoji(text: str) -> str:
    return replace_emoji(text, "").strip()


def strip_ascii(text: str) -> str:
    return text.encode("ascii", "ignore").decode("ascii")