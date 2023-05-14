## Neovim install

This is a script I use to install neovim inside arbitrary container.

## Requirements

Since container environments are extremely compact (most of the time are) environments, we should only assume the existence of some common tools:

- `Python3`
- `curl`
- `tar`

Also, this tool currently only install the executable via eget to the users `~/.local/bin`. If this is not in your path, add it with the following:

```
export PATH=$PATH:~/.local/bin
```


