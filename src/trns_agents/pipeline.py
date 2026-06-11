from __future__ import annotations

import os
from pathlib import Path

from rich.console import Console
from rich.progress import Progress

from .batch import assign_batches, group_by_batch
from .batch_reset import reset_batches
from .models import BackendMode, ProjectMeta, Segment, SegmentStatus, SegmentsDocument, extract_video_id
from .render import download_video, replace_audio, write_srt
from .render.audio import assemble_dubbed_audio
from .transcript import fetch_youtube_transcript, load_manual_transcript
from .translate import translate_segments_gemini, translate_segments_local
from .tts import synthesize_segment_cloud, synthesize_segment_local
from .workdir import WorkDir

console = Console()


def _voice_for_mode(mode: BackendMode) -> str:
    if mode == BackendMode.CLOUD:
        return os.environ.get("TRNS_TTS_VOICE_CLOUD", "Charon")
    return os.environ.get("TRNS_TTS_VOICE_LOCAL", "th-TH-NiwatNeural")


def acquire_transcript(
    video_id: str,
    url: str,
    manual_path: Path | None,
) -> tuple[list[Segment], str]:
    if manual_path:
        console.print(f"[cyan]Loading manual transcript:[/] {manual_path}")
        return load_manual_transcript(manual_path), "manual"
    try:
        console.print("[cyan]Fetching YouTube captions…[/]")
        return fetch_youtube_transcript(video_id), "auto"
    except Exception as exc:
        console.print(f"[yellow]Auto transcript failed ({exc}); use --transcript or --transcribe[/]")
        raise


def run_dub_pipeline(
    url: str,
    mode: BackendMode = BackendMode.LOCAL,
    *,
    resume: bool = False,
    transcript_file: Path | None = None,
    batch_minutes: int | None = None,
    skip_download: bool = False,
    skip_render: bool = False,
    max_batches: int | None = None,
    redo_batches: list[int] | None = None,
) -> WorkDir:
    video_id = extract_video_id(url)
    work = WorkDir(video_id)
    batch_mins = batch_minutes or int(os.environ.get("TRNS_BATCH_MINUTES", "5"))

    if work.segments_path.exists() and (resume or redo_batches):
        doc = work.load_segments()
        meta = work.load_meta()
        console.print(f"[green]Resume[/] — {len(doc.segments)} segments loaded")
        if redo_batches:
            doc = reset_batches(work, doc, redo_batches)
            console.print(f"[yellow]Reset batches[/] {redo_batches} for reprocess")
    else:
        segments, source = acquire_transcript(video_id, url, transcript_file)
        segments = assign_batches(segments, batch_mins)
        meta = ProjectMeta(
            video_id=video_id,
            url=url,
            mode=mode,
            voice=_voice_for_mode(mode),
            batch_minutes=batch_mins,
            transcript_source=source,  # type: ignore[arg-type]
        )
        doc = SegmentsDocument(video_id=video_id, segments=segments)
        work.save_meta(meta)
        work.save_segments(doc)
        console.print(f"[green]Acquired[/] {len(segments)} segments ({source})")

    groups = group_by_batch(doc.segments)
    voice = meta.voice
    batch_ids = sorted(groups.keys())
    if max_batches is not None:
        batch_ids = batch_ids[:max_batches]

    with Progress() as progress:
        task = progress.add_task("Processing batches", total=len(batch_ids))
        for batch_id in batch_ids:
            batch_segs = groups[batch_id]
            if resume and work.is_batch_done(batch_id) and not (
                redo_batches and batch_id in redo_batches
            ):
                progress.advance(task)
                continue

            to_translate = [s for s in batch_segs if not s.text_th or s.status == SegmentStatus.PENDING]
            if to_translate:
                if mode == BackendMode.CLOUD:
                    translated = translate_segments_gemini(to_translate)
                else:
                    translated = translate_segments_local(to_translate)
                updated_map = {s.id: s for s in translated}
                for i, seg in enumerate(doc.segments):
                    if seg.id in updated_map:
                        doc.segments[i] = updated_map[seg.id]
                batch_segs = [doc.segments[i] for i, s in enumerate(doc.segments) if s.batch_id == batch_id]

            batch_dir = work.batch_dir(batch_id)
            for seg in batch_segs:
                wav_path = batch_dir / "tts" / f"{seg.id}.wav"
                if seg.tts_wav and Path(seg.tts_wav).exists() and seg.status == SegmentStatus.TTS_DONE:
                    continue
                if mode == BackendMode.CLOUD:
                    synthesize_segment_cloud(seg, wav_path, voice=voice)
                else:
                    synthesize_segment_local(seg, wav_path, voice=voice)
                for i, s in enumerate(doc.segments):
                    if s.id == seg.id:
                        doc.segments[i] = s.model_copy(
                            update={"tts_wav": str(wav_path), "status": SegmentStatus.TTS_DONE}
                        )

            work.save_segments(doc)
            work.mark_batch_done(batch_id)
            progress.advance(task)

    write_srt(
        [s for s in doc.segments if s.status == SegmentStatus.TTS_DONE],
        work.output_srt,
    )
    console.print(f"[green]Wrote[/] {work.output_srt}")

    if skip_render:
        return work

    assemble_segs = [
        s
        for s in doc.segments
        if s.status == SegmentStatus.TTS_DONE and s.tts_wav and Path(s.tts_wav).exists()
    ]
    if max_batches is not None:
        allowed_batches = set(batch_ids)
        assemble_segs = [s for s in assemble_segs if s.batch_id in allowed_batches]

    total_ms = max((s.end_ms for s in assemble_segs), default=0)
    dubbed_wav = work.path("dubbed.full.wav")
    assemble_dubbed_audio(assemble_segs, total_ms, dubbed_wav)
    console.print(f"[green]Assembled[/] {dubbed_wav}")

    source_mp4 = work.path("source.mp4")
    if not skip_download and not source_mp4.exists():
        console.print("[cyan]Downloading video…[/]")
        download_video(url, source_mp4)

    if source_mp4.exists():
        replace_audio(source_mp4, dubbed_wav, work.output_mp4)
        console.print(f"[bold green]Done:[/] {work.output_mp4}")
    else:
        console.print("[yellow]Skip mux — source.mp4 missing (install yt-dlp)[/]")

    return work
