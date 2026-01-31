from app.data.db import init_db
from app.ui.ventana_principal import iniciar_app


def main():
    init_db()
    iniciar_app()


if __name__ == "__main__":
    main()
