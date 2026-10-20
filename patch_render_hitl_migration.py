from pathlib import Path


PATH = Path("emidaf_studio/app.py")

text = PATH.read_text(
    encoding="utf-8"
)


BLOCK = '''
# =========================================================
# MIGRATIONS RUNTIME EMIDAF
# =========================================================

def _run_runtime_migrations():
    """
    Exécute les migrations SQLite idempotentes nécessaires
    avant le démarrage de l'application.

    Utile notamment sur Render, où la base distante peut
    avoir un schéma plus ancien que le code déployé.
    """
    from pathlib import Path
    import subprocess
    import sys

    migration_script = Path(
        "migrate_teacher_validation_hitl.py"
    )

    if not migration_script.exists():
        print(
            "[EMIDAF] Migration HITL absente : "
            "aucune migration exécutée."
        )
        return

    try:
        subprocess.run(
            [
                sys.executable,
                str(migration_script),
            ],
            check=True,
        )

        print(
            "[EMIDAF] Migration HITL vérifiée."
        )

    except Exception as exc:
        print(
            "[EMIDAF] Migration HITL impossible :",
            exc,
        )
        raise


_run_runtime_migrations()

'''


if "_run_runtime_migrations()" in text:

    print(
        "[INFO] Migration runtime déjà installée."
    )

else:

    anchor = "import emidaf_studio.pages.edse.callbacks"

    position = text.find(
        anchor
    )

    if position < 0:
        raise RuntimeError(
            "Point d'insertion introuvable dans app.py"
        )

    text = (
        text[:position]
        + BLOCK
        + text[position:]
    )

    PATH.write_text(
        text,
        encoding="utf-8",
    )

    print(
        "[OK] Migration runtime ajoutée à app.py"
    )
