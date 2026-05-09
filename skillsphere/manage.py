"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # #region agent log (db env debugging)
    # Prints on every run so we can prove Railway is running this code.
    def _shape(name: str):
        exists = name in os.environ
        val = os.environ.get(name)
        is_empty = exists and (val is None or str(val) == "")
        looks_like_railway_ref = isinstance(val, str) and val.strip().startswith("${{") and val.strip().endswith("}}")
        return {"exists": bool(exists), "empty": bool(is_empty), "len": (len(val) if isinstance(val, str) else None), "railway_ref_syntax": bool(looks_like_railway_ref)}

    try:
        print(
            "DBG_DBENV BOOT manage.py@2026-05-07 "
            f"RAILWAY_SERVICE_NAME={'set' if os.getenv('RAILWAY_SERVICE_NAME') else 'missing'} "
            f"DATABASE_URL={_shape('DATABASE_URL')} "
            f"PGHOST={_shape('PGHOST')} PGDATABASE={_shape('PGDATABASE')} PGUSER={_shape('PGUSER')}"
        )
    except Exception:
        pass
    # #endregion

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsphere.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
