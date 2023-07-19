# Linting with Ruff

## TL;DR

Ruff is a linter.  Linting is the process of running a program that will analyse code for potential errors.

- [ruff](https://github.com/astral-sh/ruff)
- [rules](https://beta.ruff.rs/docs/rules/)
- Configuration is in `puproject.toml`

## Examples

- `ruff check app/models` - Run linter on all of `app/models`
- `ruff check app/models --select UP007` - Run linter on all of `app/models` only for rule UP007
- `ruff check app/models --ignore UP007` - Run linter on all of `app/models` and ignore rule UP007
- `ruff check app/models --fix` - Auto-fix the easy ones

## Notes

- We probably want to ignore UP007 (`Use X | Y for type annotations`)