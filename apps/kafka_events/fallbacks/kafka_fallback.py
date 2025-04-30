import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

FALLBACK_DIR = Path("logs/kafka_fallbacks")
FALLBACK_DIR.mkdir(parents=True, exist_ok=True)


def save_event_to_fallback(topic, event):
    try:
        timestamp = datetime.utcnow().isoformat()
        fallback_file = FALLBACK_DIR / f"{topic}.log"

        with open(fallback_file, "a") as f:
            f.write(json.dumps({"timestamp": timestamp, "event": event}) + "\\n") # noqa501

        logger.warning(f"📦 Evento salvo em fallback: {event}")
    except Exception as e:
        logger.error(f"❌ Falha ao salvar fallback: {e}")
