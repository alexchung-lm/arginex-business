"""Gemini API — 把客製化平面酒標貼到 3D 瓶身意象圖"""

import os
import uuid

SHOWCASE_TEMPLATE = os.path.join(os.path.dirname(__file__), "templates", "showcase_A.png")

PROMPT = (
    "我上傳了兩張圖。第一張是產品意象圖（有酒瓶、木盒、青梅的場景），"
    "第二張是客製化的平面酒標。請把第一張意象圖中瓶身上的酒標替換成第二張的客製化酒標。"
    "保留原本的瓶身形狀、光影、金箔繩結、木盒和青梅場景，只換標籤內容。"
    "直接輸出圖片，不需要文字說明。"
)


def generate_showcase(label_path: str, output_dir: str = "output") -> str | None:
    """把客製化平面酒標貼到瓶身意象圖上，回傳生成的意象圖路徑。"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[SHOWCASE] GEMINI_API_KEY not set, skipping")
        return None

    try:
        from google import genai
        from google.genai import types
        from PIL import Image

        client = genai.Client(api_key=api_key)

        # 開啟兩張圖片
        showcase_img = Image.open(SHOWCASE_TEMPLATE)
        label_img = Image.open(label_path)

        print(f"[SHOWCASE] 呼叫 Gemini API（模型: gemini-2.0-flash-exp）...")

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[showcase_img, label_img, PROMPT],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            ),
        )

        # 從 response 提取圖片
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # 儲存圖片
                os.makedirs(output_dir, exist_ok=True)
                filename = f"{uuid.uuid4().hex[:8]}_showcase.png"
                out_path = os.path.join(output_dir, filename)

                image = part.as_image()
                image.save(out_path)
                print(f"[SHOWCASE] 意象圖已生成: {out_path}")
                return out_path

        # 如果沒有圖片，印出文字回應
        for part in response.candidates[0].content.parts:
            if part.text:
                print(f"[SHOWCASE] Gemini 文字回應: {part.text[:200]}")

        print("[SHOWCASE] response 中沒有圖片")
        return None

    except Exception as e:
        print(f"[SHOWCASE] 生成失敗: {e}")
        import traceback
        traceback.print_exc()
        return None
