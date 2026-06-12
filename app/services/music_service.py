from pathlib import Path
from datetime import datetime
import shutil
import requests


ACE_STEP_UI_URL = "http://127.0.0.1:7860"  # l'UI Gradio, pas 8001
ACE_OUTPUT_DIR = Path("/Users/lancri/ACE-Step-1.5/gradio_outputs")
LOCAL_STORAGE_DIR = Path("app/storage/audio")

LOCAL_STORAGE_DIR.mkdir(parents=True, exist_ok=True)


class MusicService:
    def generate_instrumental(self, prompt: str, duration: int = 60) -> dict:
        # Le payload pour l'endpoint Gradio /predict
        payload = {
            "data": [
                "",                              # lyrics (vide)
                prompt,                          # tags/prompt
                duration                         # duration
            ]
        }

        response = requests.post(
            f"{ACE_STEP_UI_URL}/predict",
            json=payload,
            timeout=600
        )
        response.raise_for_status()
        result = response.json()

        latest_file = self._find_latest_audio_file()
        if not latest_file:
            raise RuntimeError("No generated audio file found in ACE-Step output directory")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = LOCAL_STORAGE_DIR / f"track_{timestamp}{latest_file.suffix}"
        shutil.copy2(latest_file, dest)

        return {
            "provider": "ace_step",
            "prompt": prompt,
            "audio_path": str(dest),
            "duration": duration,
            "raw_result": result,
        }

    def _find_latest_audio_file(self) -> Path | None:
        files = []
        for ext in ("*.wav", "*.mp3", "*.flac"):
            files.extend(ACE_OUTPUT_DIR.rglob(ext))
        if not files:
            return None
        return max(files, key=lambda p: p.stat().st_mtime)