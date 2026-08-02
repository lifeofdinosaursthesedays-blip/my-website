"""アプリと同じ配色で5度圏アイコンを生成する。"""
import math, colorsys
from PIL import Image, ImageDraw

INK = (0x15, 0x18, 0x23)
HUB = (0x1e, 0x22, 0x30)
NEUTRAL = (0x2b, 0x31, 0x43)
BRASS = (0xc6, 0x96, 0x3f)

# 5度圏の順（C から時計回り）: (type, 調号の数)
KEYS = [("none",0),("sharp",1),("sharp",2),("sharp",3),("sharp",4),("sharp",5),
        ("flat",6),("flat",5),("flat",4),("flat",3),("flat",2),("flat",1)]

def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return (int(r*255), int(g*255), int(b*255))

def seg_color(kind, count):
    if kind == "none":
        return NEUTRAL
    t = count/6.0
    if kind == "sharp":
        return hsl(40, 34+t*26, 26+t*16)
    return hsl(168, 22+t*22, 24+t*15)

def render(size, pad_ratio=0.09, rounded=False):
    S = 8  # スーパーサンプリング
    W = size*S
    img = Image.new("RGBA", (W, W), INK + (255,))
    d = ImageDraw.Draw(img)

    cx = cy = W/2
    usable = W*(1 - 2*pad_ratio)
    r_out = usable/2
    r_in  = r_out*0.52
    step = 360/12

    for i, (kind, count) in enumerate(KEYS):
        a_mid = -90 + i*step
        a0, a1 = a_mid - step/2, a_mid + step/2
        d.pieslice([cx-r_out, cy-r_out, cx+r_out, cy+r_out], a0, a1,
                   fill=seg_color(kind, count) + (255,), outline=INK + (255,), width=max(1, S))

    # 中心のハブをくり抜く
    d.ellipse([cx-r_in, cy-r_in, cx+r_in, cy+r_in], fill=HUB + (255,), outline=INK+(255,), width=max(1,S))

    # 真上のポインタ（ルーレットの目印）。リムの外から先端を少し差し込む
    tip = cy - r_out*0.88
    top = cy - r_out*1.20
    half = r_out*0.15
    d.polygon([(cx, tip), (cx-half, top), (cx+half, top)], fill=BRASS + (255,))

    img = img.resize((size, size), Image.LANCZOS)

    if rounded:  # iOS 用は角丸不要（OSが処理）だが背景は不透明にしておく
        pass
    return img

for size, name in [(192,"icon-192.png"), (512,"icon-512.png"), (180,"apple-touch-icon.png")]:
    render(size).save(name)
# maskable はセーフゾーン確保のため内側80%に収める
render(512, pad_ratio=0.20).save("icon-512-maskable.png")
# ファビコン
render(64).save("favicon-64.png")
print("生成:", "icon-192.png icon-512.png apple-touch-icon.png icon-512-maskable.png favicon-64.png")
