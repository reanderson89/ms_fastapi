# Add to `.zshrc`

```
# Python Blueboard
## Homebrew path
export PATH="${PATH}:/opt/homebrew/bin:${PATH}"
export PATH="${PATH}:/opt/homebrew/sbin"

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PIPENV_PYTHON="$PYENV_ROOT/shims/python"

plugin=(
  pyenv
)

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
#

```
source ~/.zshrc
brew install pyenv pyenv-virtualenv
pip3 install -r src/reqs.txt

pyenv install 3.11.1
pyenv versions
pyenv global 3.11.1
```
