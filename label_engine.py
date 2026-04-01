"""酒標客製化引擎 — 合併模板：左側乾淨（Pillow 加字）+ 右側原版（Gemini 品質）"""

import os
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "templates/label_A_merged.png"
# 多平台字體：macOS 用行楷，Render(Ubuntu) 用 Noto Serif CJK
FONT_CANDIDATES = [
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/13b8ce423f920875b28b551f9406bf1014e0a656.asset/AssetData/Xingkai.ttc",  # macOS 行楷
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",  # Ubuntu noto-cjk
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",   # Ubuntu noto-cjk fallback
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",   # Ubuntu alt path
    os.path.join(os.path.dirname(__file__), "fonts", "NotoSansTC.ttf"),  # 本地字體（Render 用）
]
FONT_PATH = next((f for f in FONT_CANDIDATES if os.path.isfile(f)), FONT_CANDIDATES[-1])
GOLD_COLOR = (169, 131, 58, 255)


def draw_vertical_text(draw, text, x_center, y_start, y_end, font, color):
    """直書：每個字由上往下均勻分佈"""
    chars = list(text)
    bboxes = [font.getbbox(ch) for ch in chars]
    heights = [bb[3] - bb[1] for bb in bboxes]
    total_h = sum(heights)
    spacing = (y_end - y_start - total_h) / (len(chars) + 1)

    y = y_start + spacing
    for i, ch in enumerate(chars):
        bb = bboxes[i]
        char_w = bb[2] - bb[0]
        draw.text((x_center - char_w // 2, y - bb[1]), ch, fill=color, font=font)
        y += heights[i] + spacing


def generate_custom_label(
    company_name: str,
    logo_path: str | None = None,
    product_name: str = "草莓微醺果酒",
    output_dir: str = "output",
) -> str:
    """產生客製化酒標。只改左側產品名 + 加客戶 Logo，右側保留原版。"""
    img = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 1. 左側直書產品名（行楷毛筆字 230px）
    font_large = ImageFont.truetype(FONT_PATH, size=230)
    draw_vertical_text(draw, product_name, 275, 200, 1700, font_large, GOLD_COLOR)

    # 2. 客戶 Logo + 公司名（底部置中）
    if logo_path and os.path.isfile(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((250, 250), Image.LANCZOS)
        logo_x = (img.width - logo.width) // 2
        img.paste(logo, (logo_x, 1850), logo)

        draw = ImageDraw.Draw(img)
        font_small = ImageFont.truetype(FONT_PATH, size=55)
        name_y = 1850 + logo.height + 10
        name_bbox = font_small.getbbox(company_name)
        name_w = name_bbox[2] - name_bbox[0]
        draw.text(((img.width - name_w) // 2, name_y), company_name, fill=GOLD_COLOR, font=font_small)

    # 3. 儲存
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{company_name}_label.png")
    img.save(output_path)
    return output_path


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    test_logo = Image.new("RGBA", (200, 200), (255, 0, 0, 255))
    test_logo.save("test_logo.png")
    result = generate_custom_label("大成食品", "test_logo.png")
    print(f"輸出路徑: {result}")
