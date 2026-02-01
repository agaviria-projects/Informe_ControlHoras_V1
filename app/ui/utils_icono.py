from pathlib import Path
from PIL import Image, ImageTk

def aplicar_icono(win):
    """
    Aplica el icono corporativo a cualquier ventana (Tk o Toplevel).
    No rompe si el archivo no existe.
    """
    try:
        base_dir = Path(__file__).resolve().parents[2]  # .../app/ui -> raíz del proyecto
        logo_path = base_dir / "assets" / "logo.png"
        img = Image.open(logo_path).resize((64, 64))
        icon = ImageTk.PhotoImage(img)
        win.iconphoto(True, icon)
        win._icon_ref = icon  # CLAVE: evitar que se pierda
    except Exception:
        pass
