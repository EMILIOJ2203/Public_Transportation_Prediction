#!/usr/bin/env python3
from datetime import date, timedelta
from pathlib import Path
import argparse

WEEKDAYS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def generar_fechas(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

def nombre_carpeta(fecha: date, fmt: str):
    # fmt puede usar {iso}, {dd}, {mm}, {yyyy}, {weekday}
    return fmt.format(
        iso=fecha.isoformat(),
        dd=f"{fecha.day:02d}",
        mm=f"{fecha.month:02d}",
        yyyy=f"{fecha.year}",
        weekday=WEEKDAYS_ES[fecha.weekday()]
    )

def main():
    parser = argparse.ArgumentParser(description="Crear carpetas por fecha en una carpeta destino.")
    parser.add_argument("--dest", "-d", type=str, default=".", help="Carpeta destino (por defecto: carpeta actual).")
    parser.add_argument("--start", type=str, default="2025-09-08", help="Fecha inicio AAAA-MM-DD (por defecto: 2025-09-08).")
    parser.add_argument("--end", type=str, default="2026-01-03", help="Fecha fin AAAA-MM-DD (por defecto: 2026-01-03).")
    parser.add_argument("--format", "-f", type=str, default="{iso}_{weekday}", help="Formato de nombre: usa {iso},{dd},{mm},{yyyy},{weekday}.")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin crear carpetas.")
    args = parser.parse_args()

    dest = Path(args.dest).resolve()
    try:
        start_parts = [int(p) for p in args.start.split("-")]
        end_parts = [int(p) for p in args.end.split("-")]
        start_date = date(*start_parts)
        end_date = date(*end_parts)
    except Exception as e:
        print("Error: formato de fecha inválido. Usa AAAA-MM-DD.")
        return

    if start_date > end_date:
        print("Error: la fecha de inicio es posterior a la fecha final.")
        return

    print(f"Destino: {dest}")
    print(f"Rango: {start_date.isoformat()} → {end_date.isoformat()}")
    print(f"Formato de nombre: {args.format}")
    print("Modo simulación (dry-run):", args.dry_run)
    print()

    if not dest.exists():
        print("La carpeta destino no existe. Se creará:", dest)
        if not args.dry_run:
            dest.mkdir(parents=True, exist_ok=True)

    for f in generar_fechas(start_date, end_date):
        folder_name = nombre_carpeta(f, args.format)
        folder_path = dest / folder_name
        if args.dry_run:
            print("[DRY-RUN] Crear:", folder_path)
        else:
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                print("Creada:", folder_path)
            else:
                print("Ya existe:", folder_path)

if __name__ == "__main__":
    main()