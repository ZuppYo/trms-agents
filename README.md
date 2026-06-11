# trns-agents

CLI ช่วย **พากย์ YouTube ภาษาอังกฤษ → ไทย** สำหรับใช้งานส่วนตัว (local-first)

Pipeline หลัก: ดึง caption → แปล → สังเคราะห์เสียง (TTS) → รวมเป็น MP4 + ซับไตเติ้ลไทย

---

## สิ่งที่ได้

| ไฟล์ | คำอธิบาย |
|------|----------|
| `output.th.mp4` | วิดีโอต้นฉบับ + เสียงพากย์ไทย |
| `output.th.srt` | ซับไตเติ้ลไทย (ไทม์โค้ดตาม segment เดิม) |

งานถูกแบ่งเป็น **batch** (~5 นาที/batch) พร้อม checkpoint — รันวิดีโอยาวแล้วหยุดกลางทางได้

---

## ความต้องการของระบบ

| รายการ | หมายเหตุ |
|--------|----------|
| **Python ≥ 3.11** | แนะนำใช้ venv |
| **FFmpeg** | รวมเสียง TTS + mux วิดีโอ ([Gyan.FFmpeg](https://www.gyan.dev/ffmpeg/builds/) ผ่าน winget บน Windows) |
| **yt-dlp** | ติดตั้งอัตโนมัติกับ package; ใช้ดาวน์โหลดวิดีโอต้นฉบับ |
| **RAM / ดิสก์** | โหมด local โหลดโมเดล NLLB (~600M) + PyTorch — แนะนำ RAM 8 GB+ |

โค้ด **ค้นหา FFmpeg จาก WinGet อัตโนมัติ** ถ้าไม่อยู่ใน PATH แต่แนะนำให้เพิ่ม `ffmpeg` เข้า PATH เพื่อให้ yt-dlp merge วิดีโอได้ตรงๆ

---

## ติดตั้ง (ครั้งแรก)

```powershell
cd E:\SRC\ai\my\trns-agents

# สร้าง virtual environment
python -m venv .venv
.venv\Scripts\activate

# ติดตั้ง package + dependencies สำหรับโหมด local (NLLB + PyTorch)
pip install -e ".[local]"

# (ถ้ายังไม่มี FFmpeg)
winget install Gyan.FFmpeg
```

### โหมด cloud (ไม่บังคับ)

ต้องการแปลด้วย Gemini แทน NLLB:

```powershell
copy .env.example .env
# แก้ GEMINI_API_KEY ใน .env
pip install -e .
```

---

## เริ่มวิดีโอใหม่

```powershell
.venv\Scripts\activate

trns-agents dub "https://www.youtube.com/watch?v=VIDEO_ID" --mode local --resume
```

คำสั่งนี้จะ:

1. ดึง **YouTube captions** (ภาษาอังกฤษ)
2. แปลเป็นไทยด้วย **NLLB-200** (local)
3. สร้างเสียงด้วย **Edge TTS** (`th-TH-NiwatNeural` — เสียงผู้ชาย)
4. ดาวน์โหลดวิดีโอ + รวมเป็น `output.th.mp4`

### ทดสอบก่อน (batch เดียว)

```powershell
trns-agents dub "https://www.youtube.com/watch?v=VIDEO_ID" --mode local --resume --max-batches 1 --skip-render
```

ได้แค่ SRT + ไฟล์ TTS ของ batch แรก — ยังไม่ mux MP4

---

## วิดีโอยาว / รันต่อจากกลางคัน

ใช้ `--resume` เสมอเมื่อรันซ้ำ URL เดิม:

```powershell
# แปล + TTS ต่อ (ข้าม batch ที่เสร็จแล้ว)
trns-agents dub "https://www.youtube.com/watch?v=VIDEO_ID" --mode local --resume --skip-render

# เมื่อครบทุก segment — mux MP4
trns-agents dub "https://www.youtube.com/watch?v=VIDEO_ID" --mode local --resume
```

ตรวจความคืบหน้า:

```powershell
python -c "from pathlib import Path; import json; w=Path('.trns-agents/VIDEO_ID'); print('batches done:', sorted(x.name for x in (w/'batches').iterdir() if (x/'.done').exists())); d=json.load(open(w/'segments.json',encoding='utf-8')); print('tts_done', sum(1 for s in d['segments'] if s['status']=='tts_done'), '/', len(d['segments']))"
```

(แทน `VIDEO_ID` ด้วยรหัสวิดีโอจริง)

### แก้ batch ที่แปลผิด

```powershell
trns-agents dub "https://www.youtube.com/watch?v=VIDEO_ID" --mode local --redo-batches 2 --max-batches 1 --skip-render
```

จากนั้น remux:

```powershell
trns-agents dub "https://www.youtube.com/watch?v=VIDEO_ID" --mode local --resume
```

---

## ตัวเลือก CLI (`dub`)

| Flag | คำอธิบาย |
|------|----------|
| `--mode local` | NLLB + Edge TTS (ค่าเริ่มต้น, ไม่ต้อง API key) |
| `--mode cloud` | Gemini แปล + TTS cloud (ต้อง `GEMINI_API_KEY`) |
| `--resume` | โหลด checkpoint จาก work dir เดิม |
| `--skip-render` | หยุดหลัง SRT/TTS — ไม่ assemble / ไม่ mux |
| `--skip-download` | ไม่ดาวน์โหลดวิดีโอ (ใช้ `source.mp4` ที่มีอยู่) |
| `--max-batches N` | ประมวลผลแค่ N batch แรก |
| `--redo-batches 0,1` | ล้างและทำ batch ใหม่ |
| `--batch-minutes N` | ขนาด batch (ค่าเริ่มต้น 5 นาที) |
| `--transcript path.srt` | ใส่ transcript เอง (VTT/SRT) แทน YouTube API |

---

## โฟลเดอร์งาน (work dir)

```
.trns-agents/{video_id}/
├── meta.json           # ข้อมูลโปรเจกต์
├── segments.json       # ทุก segment + สถานะ
├── batches/
│   ├── 000/
│   │   ├── .done       # batch เสร็จแล้ว
│   │   └── tts/        # ไฟล์เสียงต่อ segment
│   └── ...
├── dubbed.full.wav     # เสียงรวมทั้งเรื่อง
├── source.mp4          # วิดีโอต้นฉบับ
├── output.th.mp4       # ผลลัพธ์
└── output.th.srt
```

เปลี่ยนตำแหน่ง work dir: ตั้ง `TRNS_WORK_DIR` ใน `.env`

---

## ตัวแปรสภาพแวดล้อม (ไม่บังคับ)

| ตัวแปร | ค่าเริ่มต้น | คำอธิบาย |
|--------|-------------|----------|
| `GEMINI_API_KEY` | — | จำเป็นสำหรับ `--mode cloud` |
| `TRNS_WORK_DIR` | `.trns-agents` | โฟลเดอร์ checkpoint |
| `TRNS_BATCH_MINUTES` | `5` | ความยาว batch |
| `TRNS_TTS_VOICE_LOCAL` | `th-TH-NiwatNeural` | เสียง Edge TTS |
| `TRNS_NLLB_MODEL` | `facebook/nllb-200-distilled-600M` | โมเดลแปล |

---

## ข้อจำกัด

- **ใช้ส่วนตัวเท่านั้น** — ไม่ได้ออกแบบสำหรับเผยแพร่เชิงพาณิชย์หรือละเมิดลิขสิทธิ์
- **ต้องมี caption บน YouTube** — ถ้าไม่มี auto-caption ให้ใช้ `--transcript` ใส่ไฟล์ SRT/VTT เอง (faster-whisper ยังไม่รวมใน POC)
- **คุณภาพแปล** — NLLB ใช้ได้แต่ไม่ natural เท่า LLM; ประโยคยาวหรือศัพท์เฉพาะอาจผิด
- **TTS** — เสียงเดียวทั้งเรื่อง ไม่มี speaker diarization / ปรับจังหวะตามความยาว segment อัตโนมัติ
- **เวลารัน** — วิดีโอ ~30 นาที ใช้เวลาหลายสิบนาที (แปล + TTS บน CPU)
- **โหมด cloud** — มีในโค้ดแต่ยังไม่ใช่ workflow หลักของ Phase 1
- **รูปแบบวิดีโอ** — yt-dlp อาจดาวน์โหลดแยก video+audio ถ้า FFmpeg ไม่อยู่ใน PATH ของ yt-dlp

---

## แก้ปัญหาเบื้องต้น

| อาการ | แนวทาง |
|-------|--------|
| `ffmpeg` not found | ติดตั้ง FFmpeg หรือเพิ่ม WinGet bin เข้า PATH |
| ไม่มีเสียงใน MP4 | รัน remux อีกครั้งด้วย `--resume` (ไม่ใส่ `--skip-render`) |
| `source.mp4 missing` | ติดตั้ง yt-dlp; ตรวจ FFmpeg สำหรับ merge |
| Auto transcript failed | วิดีโอไม่มี caption → `--transcript file.srt` |
| แปลช้า / RAM เต็ม | ลด `TRNS_NLLB_BATCH_SIZE` หรือใช้ `--max-batches` ทีละน้อย |

---

## โครงสร้างโปรเจกต์

```
src/trns_agents/
├── cli.py          # คำสั่ง trns-agents dub
├── pipeline.py     # workflow หลัก
├── translate/      # NLLB (local) / Gemini (cloud)
├── tts/            # Edge TTS / cloud
└── render/         # assemble เสียง, mux, SRT
```

ประวัติการพัฒนา Phase 1: [`task/archive/2026-06-11/`](task/archive/2026-06-11/)
