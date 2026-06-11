from __future__ import annotations

import os
from functools import lru_cache

_MODEL = os.environ.get("TRNS_NLLB_MODEL", "facebook/nllb-200-distilled-600M")
_SRC_LANG = "eng_Latn"
_TGT_LANG = "tha_Thai"
_BATCH_SIZE = int(os.environ.get("TRNS_NLLB_BATCH_SIZE", "8"))


@lru_cache(maxsize=1)
def _load_model():
    try:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError(
            'Local translate requires optional deps: pip install -e ".[local]"'
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(_MODEL, src_lang=_SRC_LANG)
    model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL)
    tgt_id = tokenizer.convert_tokens_to_ids(_TGT_LANG)
    return tokenizer, model, tgt_id


def translate_texts(texts: list[str]) -> list[str]:
    if not texts:
        return []
    tokenizer, model, tgt_id = _load_model()
    results: list[str] = []
    for i in range(0, len(texts), _BATCH_SIZE):
        chunk = texts[i : i + _BATCH_SIZE]
        inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model.generate(**inputs, forced_bos_token_id=tgt_id, max_new_tokens=256, max_length=None)
        decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        results.extend(t.strip() for t in decoded)
    return results
