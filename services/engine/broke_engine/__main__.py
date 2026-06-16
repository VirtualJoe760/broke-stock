"""Run the engine API: `python -m broke_engine`."""

from __future__ import annotations


def main() -> None:
    import uvicorn

    uvicorn.run("broke_engine.api:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
