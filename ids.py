#!/usr/bin/env python3
"""
NET-05 IDS — Sistema de Detección de Intrusos
Uso: sudo python ids.py [--iface eth0] [--count 100]
"""
import argparse
from rich.console import Console
from src.capture import start_capture
from src.detector import load_model, predict
from src.alerter import alert_console, alert_telegram

console = Console()


def main():
    parser = argparse.ArgumentParser(description="NET-05 Homemade IDS")
    parser.add_argument("--iface", default=None, help="Interfaz de red (ej: eth0)")
    parser.add_argument("--count", type=int, default=0, help="Paquetes a capturar (0=infinito)")
    args = parser.parse_args()

    console.print("[bold blue]NET-05 IDS — Iniciando...[/bold blue]")
    model, scaler = load_model()
    console.print("[green]✓ Modelo cargado[/green]")
    console.print(f"[dim]Escuchando en: {args.iface or 'todas las interfaces'}[/dim]\n")

    def on_packet(features):
        vector = features.to_model_vector()
        result = predict(model, scaler, vector)
        alert_console(features, result)
        alert_telegram(features, result)

    try:
        start_capture(on_packet, interface=args.iface, packet_count=args.count)
    except KeyboardInterrupt:
        console.print("\n[yellow]IDS detenido.[/yellow]")


if __name__ == "__main__":
    main()
