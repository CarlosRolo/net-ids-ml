import os
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from dotenv import load_dotenv

load_dotenv()
console = Console()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def alert_console(features, prediction: dict) -> None:
    """Muestra alerta en terminal con Rich."""
    ts = datetime.now().strftime("%H:%M:%S")

    if prediction["is_anomaly"]:
        title = f"[bold red]⚠  ANOMALY DETECTED — {ts}[/bold red]"
        style = "red"
    else:
        title = f"[dim green]✓  Normal traffic — {ts}[/dim green]"
        style = "green"

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("Field", style="dim", width=18)
    table.add_column("Value")

    table.add_row("Src IP", str(features.src_ip))
    table.add_row("Dst IP", str(features.dst_ip))
    table.add_row("Protocol", features.protocol.upper())
    table.add_row("Dst Port", str(features.dst_port))
    table.add_row("Bytes →", str(features.src_bytes))
    table.add_row("Score", f"{prediction['score']:.4f}")
    table.add_row("Label", f"[bold]{prediction['label']}[/bold]")

    console.print(Panel(table, title=title, border_style=style))


def alert_telegram(features, prediction: dict) -> None:
    """Envía alerta a Telegram si hay anomalía y el token está configurado."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    if not prediction["is_anomaly"]:
        return

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = (
        f"🚨 *IDS ALERT — ANOMALY*\n"
        f"`{ts}`\n\n"
        f"*Src:* `{features.src_ip}:{features.src_port}`\n"
        f"*Dst:* `{features.dst_ip}:{features.dst_port}`\n"
        f"*Protocol:* `{features.protocol.upper()}`\n"
        f"*Bytes:* `{features.src_bytes}`\n"
        f"*Score:* `{prediction['score']:.4f}`"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }, timeout=5)
    except Exception as e:
        console.print(f"[yellow]Telegram error: {e}[/yellow]")
