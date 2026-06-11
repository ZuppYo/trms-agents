from __future__ import annotations

import os
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

from .models import BackendMode
from .pipeline import run_dub_pipeline

console = Console()


@click.group()
@click.version_option(package_name="trns-agents")
def main() -> None:
    """trns-agents - YouTube EN to TH dubbing (personal use)."""
    load_dotenv()


@main.command("dub")
@click.argument("url")
@click.option(
    "--mode",
    type=click.Choice(["cloud", "local"], case_sensitive=False),
    default="local",
    help="cloud=Gemini API; local=Edge-TTS (+ placeholder translate)",
)
@click.option("--resume", is_flag=True, help="Resume from checkpoint in work dir")
@click.option(
    "--transcript",
    "transcript_file",
    type=click.Path(exists=True, path_type=Path),
    help="Manual VTT/SRT from Obsidian Web Clipper",
)
@click.option("--batch-minutes", type=int, default=None, help="Batch size in minutes (default 5)")
@click.option("--skip-download", is_flag=True, help="Skip yt-dlp video download")
@click.option("--skip-render", is_flag=True, help="Stop after SRT/TTS (no mux)")
@click.option("--max-batches", type=int, default=None, help="Process only first N batches (e.g. 1 for smoke test)")
@click.option(
    "--redo-batches",
    default=None,
    help="Comma-separated batch ids to re-translate/re-TTS (e.g. 0 or 0,1)",
)
def dub_cmd(
    url: str,
    mode: str,
    resume: bool,
    transcript_file: Path | None,
    batch_minutes: int | None,
    skip_download: bool,
    skip_render: bool,
    max_batches: int | None,
    redo_batches: str | None,
) -> None:
    """Dub a YouTube video: EN transcript to TH speech + subtitles."""
    backend = BackendMode(mode.lower())
    if backend == BackendMode.CLOUD and not os.environ.get("GEMINI_API_KEY"):
        raise click.ClickException("Set GEMINI_API_KEY for cloud mode (see .env.example)")

    redo: list[int] | None = None
    if redo_batches:
        redo = [int(x.strip()) for x in redo_batches.split(",") if x.strip()]

    work = run_dub_pipeline(
        url,
        backend,
        resume=resume or bool(redo),
        transcript_file=transcript_file,
        batch_minutes=batch_minutes,
        skip_download=skip_download,
        skip_render=skip_render,
        max_batches=max_batches,
        redo_batches=redo,
    )
    console.print(f"[dim]Work dir:[/] {work.root}")


if __name__ == "__main__":
    main()
