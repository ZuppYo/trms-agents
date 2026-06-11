#!/usr/bin/env python3

"""Report caption overlap, drift, and projected timeline overlap for dub segments."""



from __future__ import annotations



import argparse

import json

import statistics

import sys

from pathlib import Path



sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))



from trns_agents.models import Segment

from trns_agents.render.audio import _MAX_TEMPO, _compute_placements





def _drift_stats(placements) -> tuple[float, float, float, int]:

    drifts = [pl.play_at_ms - pl.seg.start_ms for pl in placements]

    if not drifts:

        return 0.0, 0.0, 0.0, 0

    over_5s = sum(1 for d in drifts if d > 5000)

    return min(drifts), statistics.median(drifts), max(drifts), over_5s





def main() -> None:

    parser = argparse.ArgumentParser(description="Analyze dub segment timing")

    parser.add_argument("work_dir", type=Path, help="e.g. .trns-agents/QbjAQFJJyt0")

    parser.add_argument("--batch", type=int, default=None, help="Only segments in batch id")

    args = parser.parse_args()



    segments_path = args.work_dir / "segments.json"

    doc = json.loads(segments_path.read_text(encoding="utf-8"))

    segs = [Segment.model_validate(s) for s in doc["segments"]]

    if args.batch is not None:

        segs = [s for s in segs if s.batch_id == args.batch]



    clips = [s for s in segs if s.tts_wav and Path(s.tts_wav).exists()]

    if not clips:

        print("No TTS clips found")

        return



    cap_overlap = sum(

        1 for i in range(len(clips) - 1) if clips[i].end_ms > clips[i + 1].start_ms

    )



    placements = _compute_placements(clips)

    audio_overlap = 0

    for i in range(len(placements) - 1):

        end = placements[i].play_at_ms + placements[i].tts_ms

        if end > placements[i + 1].play_at_ms + 50:

            audio_overlap += 1



    drift_min, drift_med, drift_max, drift_over_5s = _drift_stats(placements)

    tempo_hits = sum(1 for pl in placements if pl.atempo > 1.001)

    trimmed = sum(1 for pl in placements if pl.trimmed)



    print(f"segments: {len(clips)}")

    print(f"max_tempo: {_MAX_TEMPO}")

    print(f"caption_window_overlaps: {cap_overlap}")

    print(f"timeline_audio_overlaps: {audio_overlap}")

    print(

        "drift_play_at_minus_start_ms_ms: "

        f"min={drift_min:.0f} median={drift_med:.0f} max={drift_max:.0f}"

    )

    print(f"segments_drift_over_5s: {drift_over_5s}")

    print(f"segments_with_atempo: {tempo_hits}")

    print(f"segments_trimmed_after_tempo: {trimmed}")

    if placements:

        last = placements[-1]

        print(f"timeline_end_ms: {last.play_at_ms + last.tts_ms}")





if __name__ == "__main__":

    main()

