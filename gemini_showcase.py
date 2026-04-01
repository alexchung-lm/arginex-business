"""Gemini API — 把客製化平面酒標貼到 3D 瓶身意象圖"""

import os
import uuid
import base64
import signal
import google.generativeai as genai


SHOWCASE_TEMPLATE = os.path.join("templates", "showcase_A.png")

PROMPT = (
    "我上傳了兩張圖。第一張是產品意象圖（有酒瓶、木盒、青梅的場景），"
    "第二張是客製化的平面酒標。請把第一張意象圖中瓶身上的酒標替換成第二張的客製化酒標。"
    "保留原本的瓶身形狀、光影、金箔繩結、木盒和青梅場景，只換標籤內容。"
)


class _Timeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise _Timeout("Gemini API call timed out")


def generate_showcase(label_path: str, output_dir: str = "output") -> str | None:
    """
    把客製化平面酒標貼到瓶身意象圖上。
    - label_path: Pillow 產生的客製化酒標路徑
    - 使用 templates/showcase_A.png 作為底圖
    - 呼叫 Gemini API，上傳兩張圖 + prompt
    - 回傳生成的意象圖路徑，失敗回傳 None
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[SHOWCASE] GEMINI_API_KEY not set, skipping")
        return None

    old_handler = None
    try:
        # timeout 保護（30 秒）
        old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(30)

        genai.configure(api_key=api_key)

        # 上傳兩張圖片
        showcase_file = genai.upload_file(SHOWCASE_TEMPLATE)
        label_file = genai.upload_file(label_path)

        # 呼叫模型
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(
            [showcase_file, label_file, PROMPT],
            generation_config={"response_mime_type": "image/png"},
        )

        # 從 response 提取圖片
        for part in response.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_data = part.inline_data.data
                # inline_data.data 可能已經是 bytes 或是 base64 string
                if isinstance(image_data, str):
                    image_data = base64.b64decode(image_data)

                os.makedirs(output_dir, exist_ok=True)
                filename = f"{uuid.uuid4().hex[:8]}_showcase.png"
                out_path = os.path.join(output_dir, filename)
                with open(out_path, "wb") as f:
                    f.write(image_data)
                print(f"[SHOWCASE] 意象圖已生成: {out_path}")
                return out_path

        print("[SHOWCASE] response 中沒有圖片")
        return None

    except _Timeout:
        print("[SHOWCASE] Gemini API 超時（30s）")
        return None
    except Exception as e:
        print(f"[SHOWCASE] 生成失敗: {e}")
        return None
    finally:
        signal.alarm(0)
        if old_handler is not None:
            signal.signal(signal.SIGALRM, old_handler)
