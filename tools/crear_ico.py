from pathlib import Path
from PIL import Image

base_dir = Path(__file__).resolve().parents[1]   # raíz del proyecto
png = base_dir / "assets" / "logo.png"
ico = base_dir / "assets" / "logo.ico"

img = Image.open(png).convert("RGBA")
img.save(ico, format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128)])
print("✅ ICO creado:", ico)
