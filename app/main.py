from app.data.db import init_db
from app.ui.bienvenida import abrir_bienvenida
from app.ui.ventana_principal import iniciar_app


def main():
    init_db()
    # Arranca por bienvenida y, al dar "Ingresar", abre la principal
    abrir_bienvenida(iniciar_app)


if __name__ == "__main__":
    main()
