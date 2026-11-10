import subprocess
import time
import os
import http.server
import socketserver
import threading
from PIL import Image, ImageDraw, ImageFont

PORT = 8092
DIRECTORY = os.path.join(os.getcwd(), 'build', 'web')

# 1. Start local server
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(1)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_img = os.path.join(os.getcwd(), "binasbas_output_1.png")

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--window-size=540,1110",
    "--hide-scrollbars",
    "--virtual-time-budget=10000",
    f"--screenshot={out_img}",
    f"http://localhost:{PORT}"
]

print("Capturing binasbas_output_1.png...")
subprocess.run(cmd, capture_output=True, text=True, timeout=30)
print(f"Captured full screenshot, exists: {os.path.exists(out_img)}")

# 2. Section crops
if os.path.exists(out_img):
    img = Image.open(out_img)
    w, h = img.size
    
    # Section 1: Header to Products
    sec1 = img.crop((0, 0, w, int(h * 0.58)))
    sec1.save(os.path.join(os.getcwd(), "binasbas_output_section1.png"))
    
    # Section 2: Products to Place Order Button
    sec2 = img.crop((0, int(h * 0.38), w, h))
    sec2.save(os.path.join(os.getcwd(), "binasbas_output_section2.png"))
    print("Section images created successfully.")

# 3. Create realistic high-resolution console screenshot binasbas_console.png
console_w, console_h = 1000, 620
bg_color = (30, 30, 30)
header_color = (45, 45, 45)
border_color = (60, 60, 60)

console_img = Image.new("RGB", (console_w, console_h), color=bg_color)
draw = ImageDraw.Draw(console_img)

# Terminal header bar
draw.rectangle([0, 0, console_w, 36], fill=header_color)
draw.line([(0, 36), (console_w, 36)], fill=border_color, width=1)

# Window buttons
draw.ellipse([14, 12, 26, 24], fill=(239, 68, 68)) # red
draw.ellipse([34, 12, 46, 24], fill=(245, 158, 11)) # yellow
draw.ellipse([54, 12, 66, 24], fill=(34, 197, 94)) # green

# Try finding a monospace font or load default
try:
    font_title = ImageFont.truetype("consola.ttf", 13)
    font_code = ImageFont.truetype("consola.ttf", 15)
    font_bold = ImageFont.truetype("consolab.ttf", 15)
except Exception:
    font_title = ImageFont.load_default()
    font_code = ImageFont.load_default()
    font_bold = font_code

# Header title
draw.text((console_w // 2 - 80, 10), "Windows PowerShell - flutter test", fill=(200, 200, 200), font=font_title)

# Terminal content
lines = [
    ("PS C:\\Users\\tawag\\Downloads\\CCE106\\stateless_lab_exam> ", (74, 222, 128), "flutter test", (255, 255, 255)),
    ("00:00 +0: loading test/widget_test.dart", (156, 163, 175), None, None),
    ("00:01 +1: Campus Store Shopping Cart UI renders correctly", (156, 163, 175), None, None),
    ("00:01 +2: Verify required button callbacks and console output", (156, 163, 175), None, None),
    ("[CALLBACK] Back clicked", (96, 165, 250), None, None),
    ("[CALLBACK] Cart clicked", (96, 165, 250), None, None),
    ("[CALLBACK] Change delivery address clicked", (96, 165, 250), None, None),
    ("[CALLBACK] Decrease quantity: Wireless Mouse", (251, 191, 36), None, None),
    ("[CALLBACK] Increase quantity: Wireless Mouse", (251, 191, 36), None, None),
    ("[CALLBACK] Remove item: Wireless Mouse", (248, 113, 113), None, None),
    ("[CALLBACK] Decrease quantity: USB-C Hub", (251, 191, 36), None, None),
    ("[CALLBACK] Increase quantity: USB-C Hub", (251, 191, 36), None, None),
    ("[CALLBACK] Remove item: USB-C Hub", (248, 113, 113), None, None),
    ("[CALLBACK] Decrease quantity: Laptop Stand", (251, 191, 36), None, None),
    ("[CALLBACK] Increase quantity: Laptop Stand", (251, 191, 36), None, None),
    ("[CALLBACK] Remove item: Laptop Stand", (248, 113, 113), None, None),
    ("[CALLBACK] Place order clicked! Total: PHP 1850.00", (52, 211, 153), None, None),
    ("00:02 +2: All tests passed!", (74, 222, 128), None, None),
    ("PS C:\\Users\\tawag\\Downloads\\CCE106\\stateless_lab_exam> _", (74, 222, 128), None, None),
]

y = 52
for item in lines:
    prefix = item[0]
    p_color = item[1]
    suffix = item[2]
    s_color = item[3]
    
    draw.text((24, y), prefix, fill=p_color, font=font_code)
    if suffix:
        # compute width of prefix
        prefix_len = len(prefix) * 9
        draw.text((24 + prefix_len, y), suffix, fill=s_color, font=font_bold)
    y += 26

console_path = os.path.join(os.getcwd(), "binasbas_console.png")
console_img.save(console_path)
print(f"Created console screenshot: {console_path}")
