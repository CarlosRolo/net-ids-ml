#!/usr/bin/env python3
"""
Entrena el modelo Isolation Forest con el dataset NSL-KDD.
Uso: python train.py
"""
import sys
from rich.console import Console
from rich.progress import track
from src.features import load_nslkdd, prepare_training_data
from src.detector import train_model, save_model

console = Console()
TRAIN_PATH = "data/nslkdd/KDDTrain+.txt"


def main():
    console.print("[bold blue]NET-05 IDS — Training[/bold blue]\n")

    console.print(f"[dim]Cargando dataset: {TRAIN_PATH}[/dim]")
    df = load_nslkdd(TRAIN_PATH)

    normal = df[df["label_binary"] == 0]
    attacks = df[df["label_binary"] == 1]
    console.print(f"  Normal:  [green]{len(normal):,}[/green] registros")
    console.print(f"  Ataques: [red]{len(attacks):,}[/red] registros\n")

    console.print("[dim]Preparando features...[/dim]")
    X_train = prepare_training_data(df)
    console.print(f"  Shape: {X_train.shape}\n")

    console.print("[dim]Entrenando Isolation Forest...[/dim]")
    model, scaler = train_model(X_train, contamination=0.1)

    save_model(model, scaler)
    console.print("\n[bold green]✓ Entrenamiento completado.[/bold green]")


if __name__ == "__main__":
    main()
