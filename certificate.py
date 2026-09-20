# -*- coding: utf-8 -*-
"""توليد شهادة PDF عربية لمنصة OptoAcademy (بدون اعتماد على Streamlit)."""
import hashlib
import io
import math
import os
from urllib.parse import urlencode

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

try:  # تشكيل الحروف العربية + الاتجاه من اليمين لليسار
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_SHAPING = True
except ImportError:  # يعمل التطبيق، لكن الشهادة لن تكون سليمة عربياً
    HAS_SHAPING = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")

NAVY = HexColor("#1E3A8A")
GOLD = HexColor("#C9A227")
GOLD_LIGHT = HexColor("#F1D77A")
GREEN = HexColor("#15803D")
GREY = HexColor("#475569")

AR_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
             "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
_AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

LINKEDIN_CERT_NAME = "OptoAcademy Clinical Expert Certificate"
LINKEDIN_ORG = "OptoAcademy"


def ar(text):
    """يهيّئ النص العربي للرسم داخل PDF."""
    if HAS_SHAPING:
        return get_display(arabic_reshaper.reshape(text))
    return text


def arabic_date(d):
    return f"{d.day} {AR_MONTHS[d.month - 1]} {d.year}".translate(_AR_DIGITS)


def credential_id(name, case_keys, issued):
    raw = f"{name.strip()}|{issued.isoformat()}|{','.join(sorted(case_keys))}"
    return "OPTO-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper()


def linkedin_url(issued, cred_id):
    params = {
        "startTask": "CERTIFICATION_NAME",
        "name": LINKEDIN_CERT_NAME,
        "organizationName": LINKEDIN_ORG,
        "issueYear": issued.year,
        "issueMonth": issued.month,
        "certId": cred_id,
    }
    return "https://www.linkedin.com/profile/add?" + urlencode(params)


def register_fonts():
    """Amiri من assets/fonts أولاً، وإلا خط عربي من النظام، وإلا Helvetica.
    يعيد (الخط العادي، الخط العريض، اسم الخط أو None)."""
    candidates = [
        ("Amiri", os.path.join(FONT_DIR, "Amiri-Regular.ttf"),
         os.path.join(FONT_DIR, "Amiri-Bold.ttf")),
        ("Noto Naskh Arabic", "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
         "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf"),
        ("DejaVu Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("FreeSerif", "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
         "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"),
    ]
    for label, regular, bold in candidates:
        if not os.path.exists(regular):
            continue
        tag = label.replace(" ", "")
        try:
            pdfmetrics.registerFont(TTFont(f"{tag}-Regular", regular))
            pdfmetrics.registerFont(TTFont(f"{tag}-Bold", bold if os.path.exists(bold) else regular))
            return f"{tag}-Regular", f"{tag}-Bold", label
        except Exception:
            continue
    return "Helvetica", "Helvetica-Bold", None


def font_status():
    """(اسم الخط المستخدم أو None، هل التشكيل متاح)"""
    return register_fonts()[2], HAS_SHAPING


def _star(c, cx, cy, r_out, r_in, color):
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, fill=1, stroke=0)


def build_certificate(name, case_titles, issued, cred_id):
    """يعيد بايتات ملف PDF للشهادة."""
    font, bold, _ = register_fonts()
    W, H = landscape(A4)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(W, H))
    c.setTitle("OptoAcademy Certificate")
    c.setAuthor("OptoAcademy")

    # الإطار
    c.setStrokeColor(NAVY)
    c.setLineWidth(4)
    c.rect(18, 18, W - 36, H - 36)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.rect(27, 27, W - 54, H - 54)

    # الترويسة
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, 555, "OptoAcademy Clinical Dashboard")
    c.setFont(bold, 44)
    c.drawCentredString(W / 2, 503, ar("شهادة إتمام"))
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 13)
    c.drawCentredString(W / 2, 480, "Certificate of Completion")

    c.setFillColor(GREY)
    c.setFont(font, 16)
    c.drawCentredString(W / 2, 445, ar("تشهد منصة OptoAcademy بأنّ"))

    # شريط ذهبي يتكيف مع طول الاسم
    name_txt = ar(name.strip())
    max_w = W - 2 * 110
    size = 36
    while size > 14 and pdfmetrics.stringWidth(name_txt, bold, size) > max_w - 70:
        size -= 1
    tw = pdfmetrics.stringWidth(name_txt, bold, size)
    band_w = min(max(260, tw + 80), max_w)
    band_h = max(58, size + 26)
    cy = 398
    c.setFillColor(GOLD_LIGHT)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.roundRect(W / 2 - band_w / 2, cy - band_h / 2, band_w, band_h, 10, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont(bold, size)
    c.drawCentredString(W / 2, cy - size * 0.32, name_txt)

    c.setFillColor(GREY)
    c.setFont(font, 15)
    c.drawCentredString(W / 2, 343, ar("أتمّ بنجاح جميع الحالات الإكلينيكية التفاعلية الأربع وبلغ مستوى «خبير إكلينيكي»"))

    # قائمة الحالات بعلامات ✓ (ترسم كمسار لتفادي غياب الرمز من الخط)
    y = 312
    for title in case_titles:
        txt = ar(title)
        w = pdfmetrics.stringWidth(txt, font, 14)
        c.setFillColor(NAVY)
        c.setFont(font, 14)
        c.drawCentredString(W / 2, y, txt)
        x = W / 2 + w / 2 + 16
        c.setStrokeColor(GREEN)
        c.setLineWidth(2.2)
        p = c.beginPath()
        p.moveTo(x - 6, y + 5)
        p.lineTo(x - 2, y + 1)
        p.lineTo(x + 6, y + 11)
        c.drawPath(p, stroke=1, fill=0)
        y -= 24

    # التاريخ و Credential ID (يسار)
    lx = 190
    c.setFillColor(GREY)
    c.setFont(font, 11)
    c.drawCentredString(lx, 128, ar("تاريخ الإتمام"))
    c.setFillColor(NAVY)
    c.setFont(bold, 15)
    c.drawCentredString(lx, 107, ar(arabic_date(issued)))
    c.setFillColor(GREY)
    c.setFont("Helvetica", 10)
    c.drawCentredString(lx, 82, "Credential ID")
    c.setFillColor(NAVY)
    c.setFont("Courier-Bold", 14)
    c.drawCentredString(lx, 64, cred_id)

    # الختم (وسط)
    sx, sy = W / 2, 112
    c.setFillColor(GOLD)
    c.circle(sx, sy, 43, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#FFFFFF"))
    c.setLineWidth(1.5)
    c.circle(sx, sy, 37, fill=0, stroke=1)
    c.setFillColor(NAVY)
    c.circle(sx, sy, 33, fill=1, stroke=0)
    _star(c, sx, sy + 16, 8, 3.4, GOLD_LIGHT)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(sx, sy - 5, "OPTO")
    c.setFillColor(GOLD_LIGHT)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(sx, sy - 17, "ACADEMY")

    # التوقيع (يمين)
    rx = W - 190
    c.setFillColor(NAVY)
    c.setFont("Times-Italic", 26)
    c.drawCentredString(rx, 100, "Rasha Hassan")
    c.setStrokeColor(NAVY)
    c.setLineWidth(1)
    c.line(rx - 85, 94, rx + 85, 94)
    c.setFillColor(GREY)
    c.setFont(font, 11)
    c.drawCentredString(rx, 78, ar("توقيع المنصة"))
    c.setFont("Helvetica", 9)
    c.drawCentredString(rx, 64, "OptoAcademy Program")

    c.setFillColor(GREY)
    c.setFont(font, 9)
    c.drawCentredString(W / 2, 40, ar("شهادة إتمام تعليمي صادرة عن منصة OptoAcademy، وليست ترخيصاً أو اعتماداً مهنياً."))

    c.showPage()
    c.save()
    return buf.getvalue()
