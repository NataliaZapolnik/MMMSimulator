import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FONT_PATH = os.path.join(BASE_DIR, 'assets\\fonts', 'UbuntuMono-Regular.ttf')

print("BASE_DIR:", BASE_DIR)
print("FONT_PATH:", FONT_PATH)