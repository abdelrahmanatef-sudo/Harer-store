"""
رفع منتجات حرير ستور على Supabase
شغّل: python upload_products_final.py
محتاج: pip install requests
"""
import requests

SUPABASE_URL = "https://ojocqktlpegfksfmoens.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qb2Nxa3RscGVnZmtzZm1vZW5zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE1Nzk2MjksImV4cCI6MjEwNzE1NTYyOX0.xQSaKAngmR6qa0I1FegQ59VmT0RtfhNObnaQ9mmCJ1E"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

session = requests.Session()
session.headers.update(HEADERS)

# ─── جيب الـ category IDs ───
cats_raw = session.get(f"{SUPABASE_URL}/rest/v1/categories?select=id,slug").json()
cats = {c["slug"]: c["id"] for c in cats_raw}
print("Categories:", cats)

# ─── المنتجات ───
# (name, description, price, old_price, image_url, category_slug, brand, stock, is_featured)
products = [

    # ══ ANKER ══
    (
        "شاحن Anker 25W Compact",
        "شاحن USB-C سريع 25 وات مدمج — متوافق مع iPhone وSamsung وأندرويد — ضمان 18 شهر",
        850, 950,
        "https://mea.store.anker.com/cdn/shop/files/B2656211_Richimage_TD01_UK.png?v=1775719427",
        "charger", "Anker", 20, True
    ),
    (
        "كابل Anker USB-C to USB-C 60W مضفر",
        "كابل مضفر سريع 60W — طول 1 متر — يتحمل 12,000 ثنية — For Apple وSamsung وGoogle",
        350, 420,
        "https://eu.anker.com/cdn/shop/files/B8753011_TD01_8c9e406a-15af-4464-8973-d46ee58523f8.png?v=1749631993",
        "cable", "Anker", 30, True
    ),

    # ══ K3 PRO كابلات ══
    (
        "كابل K3 PRO Micro USB 60W",
        "كابل Data عالي الكثافة High-Density Weaving — شحن سريع 60W — طول 1 متر — كود 3058",
        150, 200,
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85&fm=jpg",
        "cable", "K3 PRO", 50, False
    ),
    (
        "كابل K3 PRO Type-C to Type-C 100W",
        "كابل شحن فائق السرعة 100W — High-Density Weaving — متاح أسود وأبيض — طول 1 متر — كود 3052/3057",
        275, 350,
        "https://images.unsplash.com/photo-1612815292170-d0a1d1873619?w=800&q=85&fm=jpg",
        "cable", "K3 PRO", 40, True
    ),
    (
        "كابل K3 PRO Type-C to Type-C مسطح 100W",
        "كابل مسطح 100W — تصميم Flat أبيض أنيق — سهل الحمل — طول 1 متر — كود 3048",
        250, 320,
        "https://images.unsplash.com/photo-1622637323696-7a44b65e3e67?w=800&q=85&fm=jpg",
        "cable", "K3 PRO", 35, False
    ),
    (
        "كابل K3 PRO USB to Lightning 60W",
        "كابل Data Lightning سريع 60W — High-Density Weaving أبيض — طول 1 متر — كود 3056",
        250, 320,
        "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&q=85&fm=jpg",
        "cable", "K3 PRO", 40, False
    ),
    (
        "كابل K3 PRO USB to Lightning مسطح",
        "كابل Lightning مسطح — K3 القرشي صناع الضمان — طول 1 متر — كود 0739",
        150, 190,
        "https://images.unsplash.com/photo-1585338107379-7b5c4ab65a32?w=800&q=85&fm=jpg",
        "cable", "K3 PRO", 30, False
    ),
    (
        "كابل K3 PRO Type-C to Type-C شفاف 100W",
        "كابل شفاف 100W — ضمان 12 شهر — USB-IF Certified — شحن آمن — كود 3062",
        300, 380,
        "https://images.unsplash.com/photo-1612815292170-d0a1d1873619?w=800&q=85&fm=jpg",
        "cable", "K3 PRO", 25, True
    ),
    (
        "كابل K3 PRO Type-C to Lightning",
        "كابل Type-C to Lightning — طول 1.2 متر — مناسب لـ iPhone — Clear Cable",
        0, None,
        "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&q=85&fm=jpg",
        "cable", "K3 PRO", 20, False
    ),

    # ══ K3 PRO شواحن ══
    (
        "شاحن K3 PRO 45W USB-C",
        "شاحن USB-C سريع 45W — 3X Faster — Advanced Protection — لون أسود — كود 3065",
        450, 550,
        "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&q=85&fm=jpg",
        "charger", "K3 PRO", 25, True
    ),
    (
        "شاحن K3 PRO 45W Select (PD+USB-A)",
        "شاحن 45W منفذين PD+USB-A — For iPhone وSamsung — 3X Faster — كود 3064",
        450, 550,
        "https://images.unsplash.com/photo-1606229365485-93a3b8ee0385?w=800&q=85&fm=jpg",
        "charger", "K3 PRO", 20, False
    ),

    # ══ K3 PRO سماعات ══
    (
        "سماعة K3 PRO H100 Regulated Sound",
        "سماعة سلكية 3.5mm — صوت نقي Regulated Sound — مريحة للاستخدام الطويل",
        0, None,
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=85&fm=jpg",
        "earbuds", "K3 PRO", 30, False
    ),

    # ══ 3TECH كابلات ══
    (
        "كابل 3TECH Micro USB 2.4A",
        "كابل Micro USB سريع 2.4A — علبة كرافت بيج أنيقة — طول 1 متر — كود TM009",
        150, 190,
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85&fm=jpg",
        "cable", "3TECH", 60, False
    ),
    (
        "كابل 3TECH Lightning 3A",
        "كابل Lightning سريع 3A — علبة كرافت بيج — مناسب لـ iPhone — طول 1 متر",
        150, 190,
        "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&q=85&fm=jpg",
        "cable", "3TECH", 60, False
    ),
    (
        "كابل 3TECH Type-C to Type-C 65W Super Fast",
        "كابل شحن فائق السرعة 65W — متاح أبيض ووردي/بيج — طول 1 متر",
        400, 500,
        "https://images.unsplash.com/photo-1612815292170-d0a1d1873619?w=800&q=85&fm=jpg",
        "cable", "3TECH", 45, True
    ),
    (
        "كابل 3TECH USB-C to Lightning 65W Super Fast",
        "كابل Type-C to Lightning 65W Super Fast — متاح أبيض ووردي/بيج — طول 1 متر",
        400, 500,
        "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&q=85&fm=jpg",
        "cable", "3TECH", 40, False
    ),
    (
        "كابل 3TECH Type-C شفاف 3A",
        "كابل Type-C سريع 3A — علبة شفافة تركواز — تصميم عصري — طول 1 متر — كود TT301",
        0, None,
        "https://images.unsplash.com/photo-1612815292170-d0a1d1873619?w=800&q=85&fm=jpg",
        "cable", "3TECH", 35, False
    ),
    (
        "كابل 3TECH Lightning شفاف 3A",
        "كابل Lightning سريع 3A — علبة شفافة تركواز — تصميم عصري — طول 1 متر — كود TL201",
        0, None,
        "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&q=85&fm=jpg",
        "cable", "3TECH", 35, False
    ),
    (
        "كابل 3TECH Micro USB 2.4A شفاف",
        "كابل Micro USB 2.4A — علبة شفافة تركواز — متاح تركواز وأبيض — طول 1 متر — كود 1210",
        175, 220,
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85&fm=jpg",
        "cable", "3TECH", 50, False
    ),
    (
        "كابل 3TECH AUX 3.5mm",
        "كابل صوت AUX 3.5mm — لون رمادي داكن — جودة عالية للسيارة والسماعات — كود 0345",
        150, 190,
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=85&fm=jpg",
        "cable", "3TECH", 40, False
    ),
    (
        "كابل 3TECH 2 IN 1 Quick Charging",
        "كابل 2 في 1 للشحن السريع — متعدد الاستخدامات — سهل الحمل — كود TC201",
        499, 599,
        "https://images.unsplash.com/photo-1606229365485-93a3b8ee0385?w=800&q=85&fm=jpg",
        "cable", "3TECH", 20, True
    ),

    # ══ 3TECH شواحن ══
    (
        "شاحن 3TECH PD 30W",
        "شاحن USB-C سريع 30W — منفذ USB-C واحد — أبيض أنيق — كود TW100",
        450, 550,
        "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&q=85&fm=jpg",
        "charger", "3TECH", 30, True
    ),
    (
        "شاحن 3TECH PD 30W مكعب",
        "شاحن 30W تصميم مكعب مع حماية متقدمة — أبيض — منفذ USB-C — كود TW301",
        650, 750,
        "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&q=85&fm=jpg",
        "charger", "3TECH", 20, False
    ),
    (
        "شاحن 3TECH Dual USB 5V/2.1A",
        "شاحن منفذين USB-A — شحن سريع 5V/2.1A — مناسب لكل الأجهزة — كود TW002",
        300, 380,
        "https://images.unsplash.com/photo-1606229365485-93a3b8ee0385?w=800&q=85&fm=jpg",
        "charger", "3TECH", 35, False
    ),
    (
        "شاحن سيارة 3TECH PD",
        "شاحن سيارة USB-A + USB-C PD — سريع ومضغوط — للاستخدام في السيارة — كود TQ202",
        350, 430,
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85&fm=jpg",
        "charger", "3TECH", 25, False
    ),
    (
        "شاحن سيارة 3TECH USB-C QC 3.0",
        "شاحن سيارة USB-C Quick Charge 3.0 — مدمج وصغير الحجم — كود TQ102",
        0, None,
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85&fm=jpg",
        "charger", "3TECH", 20, False
    ),
]

# ─── حذف القديم ───
print("\n🗑  Deleting old products...")
r = session.delete(f"{SUPABASE_URL}/rest/v1/products?id=neq.00000000-0000-0000-0000-000000000000")
print(f"   → {r.status_code}")

# ─── رفع الجديد ───
print(f"\n📦 Inserting {len(products)} products...\n")
ok = errors = 0

for name, desc, price, old_price, img, cat_slug, brand, stock, featured in products:
    data = {
        "name": name,
        "description": desc,
        "price": price,
        "image_url": img,
        "category_id": cats.get(cat_slug),
        "brand": brand,
        "stock": stock,
        "is_featured": featured
    }
    if old_price is not None:
        data["old_price"] = old_price

    r = session.post(f"{SUPABASE_URL}/rest/v1/products", json=data)
    if r.status_code in (200, 201):
        ok += 1
        print(f"  ✓  {name[:55]}")
    else:
        errors += 1
        print(f"  ✗  {name[:55]}")
        print(f"     {r.status_code}: {r.text[:150]}")

print(f"\n{'='*58}")
print(f"  ✅  تم رفع {ok} منتج بنجاح   ❌  {errors} أخطاء")
print(f"{'='*58}")
