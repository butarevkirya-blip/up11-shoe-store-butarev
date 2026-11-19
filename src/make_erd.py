import os
import webbrowser


def find_project_root():
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, 'src')):
        return cwd
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isdir(os.path.join(current, 'src')):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE = find_project_root()
DOCS = os.path.join(BASE, 'docs')
os.makedirs(DOCS, exist_ok=True)
print("Корень проекта:", BASE)
print("Папка docs:    ", DOCS)

TBL_W = 220
FIELD_H = 22
HEADER_H = 32


def draw_table(x, y, name, fields, fill, stroke):
    w = TBL_W
    h = HEADER_H + len(fields) * FIELD_H
    parts = []
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2" rx="4"/>'
    )
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{HEADER_H}" '
        f'fill="{stroke}" stroke="{stroke}" stroke-width="2" rx="4"/>'
    )
    parts.append(
        f'<rect x="{x}" y="{y + HEADER_H - 3}" width="{w}" height="3" fill="{stroke}"/>'
    )
    parts.append(
        f'<text x="{x + 8}" y="{y + 22}" font-family="Arial" font-size="15" '
        f'font-weight="bold" fill="#ffffff">{name}</text>'
    )
    for i, f in enumerate(fields):
        fy = y + HEADER_H + (i + 1) * FIELD_H - 6
        prefix = ""
        if f.startswith("PK "):
            prefix = "🔑 "
            f = f[3:]
        elif f.startswith("FK "):
            prefix = "🔗 "
            f = f[3:]
        parts.append(
            f'<text x="{x + 8}" y="{fy}" font-family="Arial" font-size="12" '
            f'fill="#000000">{prefix}{f}</text>'
        )
        if i < len(fields) - 1:
            parts.append(
                f'<line x1="{x}" y1="{y + HEADER_H + (i + 1) * FIELD_H}" '
                f'x2="{x + w}" y2="{y + HEADER_H + (i + 1) * FIELD_H}" '
                f'stroke="#cccccc" stroke-width="1"/>'
            )
    return "\n".join(parts)


def draw_line(x1, y1, x2, y2, label1, label2):
    mx1 = x1 + (x2 - x1) * 0.18
    my1 = y1 + (y2 - y1) * 0.18
    mx2 = x1 + (x2 - x1) * 0.82
    my2 = y1 + (y2 - y1) * 0.82
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="#555555" stroke-width="2"/>'
        f'<circle cx="{x1}" cy="{y1}" r="4" fill="#555555"/>'
        f'<circle cx="{x2}" cy="{y2}" r="4" fill="#555555"/>'
        f'<text x="{mx1}" y="{my1 - 8}" font-family="Arial" font-size="16" '
        f'font-weight="bold" fill="#cc0000">{label1}</text>'
        f'<text x="{mx2}" y="{my2 - 8}" font-family="Arial" font-size="16" '
        f'font-weight="bold" fill="#cc0000">{label2}</text>'
    )


svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="900" viewBox="0 0 1500 900">']
svg.append('<rect width="1500" height="900" fill="#ffffff"/>')

svg.append(draw_table(40, 40, "roles",
                      ["PK role_id", "role_name"], "#fff2cc", "#d6b656"))
svg.append(draw_table(320, 40, "users",
                      ["PK user_id", "last_name", "first_name",
                       "middle_name", "login (UNIQUE)", "FK role_id"],
                      "#dae8fc", "#6c8ebf"))
svg.append(draw_table(620, 40, "orders",
                      ["PK order_id", "order_date", "FK user_id"],
                      "#d5e8d4", "#82b366"))
svg.append(draw_table(920, 40, "order_items",
                      ["PK order_item_id", "FK order_id",
                       "FK stock_item_id", "quantity", "price_at_order"],
                      "#f8cecc", "#b85450"))
svg.append(draw_table(40, 360, "products",
                      ["PK product_id", "category", "subcategory",
                       "manufacturer", "product_name", "image_path",
                       "composition", "description", "price"],
                      "#e1d5e7", "#9673a6"))
svg.append(draw_table(500, 460, "stock_items",
                      ["PK stock_item_id", "FK product_id",
                       "FK size_id", "quantity"],
                      "#ffe6cc", "#d79b00"))
svg.append(draw_table(900, 520, "sizes",
                      ["PK size_id", "size_value"], "#fff2cc", "#d6b656"))

svg.append(draw_line(260, 60, 320, 110, "1", "N"))
svg.append(draw_line(540, 110, 620, 110, "1", "N"))
svg.append(draw_line(840, 110, 920, 110, "1", "N"))
svg.append(draw_line(260, 460, 500, 490, "1", "N"))
svg.append(draw_line(900, 550, 720, 520, "1", "N"))
svg.append(draw_line(720, 480, 920, 200, "1", "N"))

svg.append('<text x="40" y="870" font-family="Arial" font-size="13" fill="#666666">'
           'PK — первичный ключ, FK — внешний ключ. Связи 1:N (один-ко-многим).</text>')
svg.append('</svg>')
svg_content = "\n".join(svg)

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>ER-диаграмма — Чудо Обувь</title>
<style>
  body {{ font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 20px; }}
  h1 {{ color: #333; margin-bottom: 10px; }}
  .hint {{ background: #fff3cd; border: 2px solid #ffc107; padding: 15px; border-radius: 6px; margin-bottom: 20px; }}
  .hint b {{ color: #cc0000; }}
  .wrap {{ background: #fff; border: 1px solid #ddd; }}
  @media print {{
    .hint {{ display: none; }}
    body {{ padding: 0; }}
    @page {{ size: A3 landscape; margin: 10mm; }}
  }}
</style>
</head>
<body>
<h1>ER-диаграмма базы данных «Чудо Обувь»</h1>
<div class="hint">
  <b>Чтобы получить PDF:</b> нажми <b>Ctrl+P</b> → «Принтер» → «Сохранить как PDF» (или «Microsoft Print to PDF») → имя файла <b>ERD_module_1.pdf</b> → сохрани в папку <b>docs</b>.
</div>
<div class="wrap">
{svg_content}
</div>
</body>
</html>
"""

html_path = os.path.join(DOCS, 'ERD_module_1.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"[OK] HTML создан: {html_path}")

drawio_path = os.path.join(DOCS, 'ERD_module_1.drawio')
drawio_xml = '''<mxfile host="app.diagrams.net">
  <diagram id="erd" name="ERD">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" page="1" pageScale="1" pageWidth="1600" pageHeight="1000">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="roles" value="roles&#10;─────&#10;PK role_id&#10;role_name" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;fontStyle=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="40" y="40" width="200" height="100" as="geometry"/></mxCell>
        <mxCell id="users" value="users&#10;─────&#10;PK user_id&#10;last_name&#10;first_name&#10;middle_name&#10;login (UNIQUE)&#10;FK role_id" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;fontStyle=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1"><mxGeometry x="320" y="40" width="220" height="160" as="geometry"/></mxCell>
        <mxCell id="orders" value="orders&#10;─────&#10;PK order_id&#10;order_date&#10;FK user_id" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;fontStyle=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="620" y="40" width="200" height="110" as="geometry"/></mxCell>
        <mxCell id="order_items" value="order_items&#10;─────&#10;PK order_item_id&#10;FK order_id&#10;FK stock_item_id&#10;quantity&#10;price_at_order" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;fontStyle=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1"><mxGeometry x="920" y="40" width="230" height="150" as="geometry"/></mxCell>
        <mxCell id="products" value="products&#10;─────&#10;PK product_id&#10;category&#10;subcategory&#10;manufacturer&#10;product_name&#10;image_path&#10;composition&#10;description&#10;price" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;fontStyle=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1"><mxGeometry x="40" y="360" width="230" height="240" as="geometry"/></mxCell>
        <mxCell id="stock_items" value="stock_items&#10;─────&#10;PK stock_item_id&#10;FK product_id&#10;FK size_id&#10;quantity" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;fontStyle=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1"><mxGeometry x="500" y="460" width="220" height="130" as="geometry"/></mxCell>
        <mxCell id="sizes" value="sizes&#10;─────&#10;PK size_id&#10;size_value" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=8;fontStyle=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="900" y="520" width="180" height="100" as="geometry"/></mxCell>
        <mxCell id="e1" style="endArrow=classic;html=1;strokeWidth=2;" edge="1" parent="1" source="roles" target="users"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" style="endArrow=classic;html=1;strokeWidth=2;" edge="1" parent="1" source="users" target="orders"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" style="endArrow=classic;html=1;strokeWidth=2;" edge="1" parent="1" source="orders" target="order_items"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" style="endArrow=classic;html=1;strokeWidth=2;" edge="1" parent="1" source="products" target="stock_items"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" style="endArrow=classic;html=1;strokeWidth=2;" edge="1" parent="1" source="sizes" target="stock_items"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" style="endArrow=classic;html=1;strokeWidth=2;" edge="1" parent="1" source="stock_items" target="order_items"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
with open(drawio_path, 'w', encoding='utf-8') as f:
    f.write(drawio_xml)
print(f"[OK] DRAWIO создан: {drawio_path} ({os.path.getsize(drawio_path)} байт)")

print()
print("=" * 60)
print("ГОТОВО.")
print(f"  HTML:   {html_path}")
print(f"  DRAWIO: {drawio_path}")
print("=" * 60)
print()
print("СЕЙЧАС ОТКРОЮ HTML В БРАУЗЕРЕ.")
print("В браузере:")
print("  1. Нажми Ctrl+P")
print("  2. Принтер → «Сохранить как PDF» / «Microsoft Print to PDF»")
print("  3. Имя файла: ERD_module_1")
print("  4. Папка: docs (C:\\Users\\butar\\OneDrive\\Desktop\\up11-shoe-store-butarev\\docs)")
print("  5. Сохранить")
print()
print("После этого запусти src/verify.py — там будет FAIL=0")
print("=" * 60)

try:
    webbrowser.open(html_path)
    print("[OK] HTML открыт в браузере.")
except Exception as e:
    print(f"[INFO] Не удалось открыть браузер автоматически: {e}")
    print(f"Открой вручную: {html_path}")