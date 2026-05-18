#!/usr/bin/env python3
"""Positionsgroessen-Rechner mit fester Regelwerk-Logik."""

import argparse
import math
import sys


def frage_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).replace(",", ".").strip())
        except ValueError:
            print("  Ungueltige Eingabe, bitte erneut.")


def frage_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("  Ungueltige Eingabe, bitte erneut.")


def abrunden_50(zahl: float) -> int:
    if zahl <= 0:
        return 0
    return int(math.floor(zahl / 50.0)) * 50


def berechne(startkurs: float, intervall: float, stufen: int,
             stop_abstand: float, max_verlust: float, max_kapital: float) -> dict:
    kaufleiter = [round(startkurs - i * intervall, 10) for i in range(stufen + 1)]
    stop = round(kaufleiter[-1] - stop_abstand, 10)
    risiko_pro_stueck = sum(kurs - stop for kurs in kaufleiter)
    summe_kaufkurse = sum(kaufleiter)

    if risiko_pro_stueck <= 0:
        raise ValueError("Risiko pro Stueck ist <= 0. Pruefe Stop-Abstand und Kaufleiter.")
    if summe_kaufkurse <= 0:
        raise ValueError("Summe der Kaufkurse ist <= 0.")

    max_stueck_risiko = max_verlust / risiko_pro_stueck
    max_stueck_kapital = max_kapital / summe_kaufkurse
    theoretisches_limit = min(max_stueck_risiko, max_stueck_kapital)
    finale_stueckzahl = abrunden_50(theoretisches_limit)

    realer_verlust = finale_stueckzahl * risiko_pro_stueck
    reale_kapitalbindung = finale_stueckzahl * summe_kaufkurse
    bindendes_limit = "Risiko" if max_stueck_risiko <= max_stueck_kapital else "Kapital"

    return {
        "kaufleiter": kaufleiter,
        "stop": stop,
        "risiko_pro_stueck": risiko_pro_stueck,
        "summe_kaufkurse": summe_kaufkurse,
        "max_stueck_risiko": max_stueck_risiko,
        "max_stueck_kapital": max_stueck_kapital,
        "bindendes_limit": bindendes_limit,
        "theoretisches_limit": theoretisches_limit,
        "finale_stueckzahl": finale_stueckzahl,
        "realer_verlust": realer_verlust,
        "reale_kapitalbindung": reale_kapitalbindung,
    }


def drucke(ergebnis: dict, inputs: dict) -> None:
    line = "=" * 60
    print()
    print(line)
    print("  POSITIONSGROESSEN-RECHNER  -  ERGEBNIS")
    print(line)
    print(f"  Startkurs ........... {inputs['startkurs']:.4f}")
    print(f"  Intervall ........... {inputs['intervall']:.4f}")
    print(f"  Stufen .............. {inputs['stufen']}  (=> {inputs['stufen']+1} Kaeufe)")
    print(f"  Stop-Abstand ........ {inputs['stop_abstand']:.4f}")
    print(f"  Max. Verlust ........ {inputs['max_verlust']:.2f}")
    print(f"  Max. Kapital ........ {inputs['max_kapital']:.2f}")
    print("-" * 60)
    kl = " / ".join(f"{k:.4f}" for k in ergebnis["kaufleiter"])
    print(f"  Kaufleiter .......... {kl}")
    print(f"  Stop-Loss ........... {ergebnis['stop']:.4f}")
    print(f"  Risiko je 1 Stueck .. {ergebnis['risiko_pro_stueck']:.4f}")
    print(f"  Summe Kaufkurse ..... {ergebnis['summe_kaufkurse']:.4f}")
    print("-" * 60)
    print(f"  Max. Stueck (Risiko)   {ergebnis['max_stueck_risiko']:>12.2f}")
    print(f"  Max. Stueck (Kapital)  {ergebnis['max_stueck_kapital']:>12.2f}")
    print(f"  Bindendes Limit ...... {ergebnis['bindendes_limit']}")
    print(f"  Theoretisches Limit .  {ergebnis['theoretisches_limit']:>12.2f}")
    print(line)
    print(f"  FINALE STUECKZAHL (50er abgerundet): {ergebnis['finale_stueckzahl']}")
    print(f"  Realer Worst-Case-Verlust .........: {ergebnis['realer_verlust']:.2f}")
    print(f"  Reale Kapitalbindung ..............: {ergebnis['reale_kapitalbindung']:.2f}")
    print(line)
    print()


def parse_args(argv) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Positionsgroessen-Rechner")
    p.add_argument("--startkurs", type=float)
    p.add_argument("--intervall", type=float)
    p.add_argument("--stufen", type=int)
    p.add_argument("--stop-abstand", type=float, dest="stop_abstand")
    p.add_argument("--max-verlust", type=float, dest="max_verlust")
    p.add_argument("--max-kapital", type=float, dest="max_kapital")
    return p.parse_args(argv)


def hole_inputs(args: argparse.Namespace) -> dict:
    werte = {
        "startkurs": args.startkurs if args.startkurs is not None else frage_float("Startkurs ............ : "),
        "intervall": args.intervall if args.intervall is not None else frage_float("Intervall ............ : "),
        "stufen": args.stufen if args.stufen is not None else frage_int("Stufen (Zusatzkaeufe). : "),
        "stop_abstand": args.stop_abstand if args.stop_abstand is not None else frage_float("Stop-Abstand ......... : "),
        "max_verlust": args.max_verlust if args.max_verlust is not None else frage_float("Max. Verlust ......... : "),
        "max_kapital": args.max_kapital if args.max_kapital is not None else frage_float("Max. Kapital ......... : "),
    }
    if werte["stufen"] < 0:
        raise ValueError("Stufen muss >= 0 sein.")
    return werte


def main(argv=None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    inputs = hole_inputs(args)
    ergebnis = berechne(**inputs)
    drucke(ergebnis, inputs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
