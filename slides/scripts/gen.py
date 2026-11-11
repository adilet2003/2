import sys, base64, json, requests
COMMON = ("Recreate this presentation slide as a crisp, high-resolution, professional 16:9 slide. "
 "Keep the same layout, composition and style: white-blue gradient background, dark-blue rounded title banner with white bold text, "
 "golden wavy border lines, yellow autumn maple leaves in corners, pale-yellow rounded info box, blue check-mark bullets, "
 "clean realistic semi-illustrated imagery. All text must be rendered EXACTLY as given below in Kyrgyz Cyrillic, perfectly spelled, sharp and legible, no extra text:\n")
TEXTS = {
1: """Title (top, dark blue): "ОШ №111" / "Свердлов району" ; big italic title: "Иш-чаралар боюнча отчет".
Left: photo of school building with sign "ОШ №111" and Kyrgyz flag.
Right three cards with calendar icons:
"15-сентябрь – 15-октябрь" / "«Жол эрежеси (ПДД) айлыгы»" (pedestrian crossing sign icon);
"1-октябрь – 15-октябрь" / "«Карылар күнүнө карата акция»" (elderly Kyrgyz couple icon);
"20-октябрь – 25-ноябрь" / "«Укук бузуулардын алдын алуу айлыгы»" (scales of justice icon).
Bottom blue ribbon: "Коопсуз мектеп – коопсуз коом!" """,
2: """Title banner: "Жалпы маалымат".
Body text: "ОШ №111 мектебинде 2026-жылдын 15-сентябрынан 25-ноябрына чейин төмөнкү маанилүү багыттар боюнча иш-чаралар өткөрүлдү:"
Bullets: "ПДД боюнча айлык"; "Карылар күнүнө акция"; "Укук бузуулардын алдын алуу айлыгы".
Right: emblem with open book, graduation cap, globe and golden laurel wreath.""",
3: """Title banner: "1. 15-сентябрь – 15-октябрь" / "«Жол эрежеси (ПДД) айлыгы»".
Image: pedestrian crossing sign, traffic light, schoolboy and schoolgirl in uniform crossing at a zebra crossing, park and city.
Yellow box "Максаты:" bullets: "Окуучуларды жол эрежесине сактоого үйрөтүү;" "Жол кырсыктарынын алдын алуу;" "Коопсуз жүрүм-турумду калыптандыруу." """,
4: """Title banner: "Проведенные мероприятия".
Bullets: "Биринчи класстан 11-класска чейин класстык сааттар;" "Жол инспекторлору менен жолугушуулар;" "ЮИД командасынын ишмердүүлүгү;" "ПДД боюнча викториналар, конкурстар;" "Мектеп аймагында коопсуздук боюнча түшүндүрүү иштери."
Right: friendly traffic safety officer in a reflective yellow vest giving a road safety lesson to happy schoolchildren in a school yard.""",
5: """Title banner: "2. 1-октябрь – 15-октябрь" / "«Карылар күнүнө карата акция»".
Image: elderly Kyrgyz man in white kalpak and elderly woman in white headscarf receiving red roses from a schoolgirl with white bows; flowers at bottom.
Yellow box "Максаты:" bullets: "Улуу муунга урмат көрсөтүү;" (exact spelling: к-ө-р-с-ө-т-ү-ү) "Карыларга камкордук жасоо;" "Адамгерчиликке тарбиялоо." """,
6: """Title banner: "Иш-чаралардын жүрүшү".
Bullets: "Окуучулар тарабынан карыларга арналган концерт, белектер;" "«Карылар – коомдун баа жеткис кенчи» деген темада класстык сааттар;" "Мектеп жамаатынын кайрымдуулук акциясы."
Right: schoolgirls in uniform singing on stage with microphones, balloons, banner text "Улуу муун – ардактуу конокторубуз!" (exact spelling: к-о-н-о-к-т-о-р-у-б-у-з) """,
7: """Title banner: "3. 20-октябрь – 25-ноябрь" / "«Укук бузуулардын алдын алуу айлыгы»".
Image: golden scales of justice, judge gavel, red book with gold text "ЗАКОН".
Yellow box "Максаты:" bullets: "Окуучулар арасында укук бузуулардын алдын алуу;" "Зордук-зомбулук, буллинг жана кылмыштуулуктун алдын алуу;" "Мыйзамга баш ийүүгө тарбиялоо." """,
8: """Title banner: "Өткөрүлгөн иш-чаралар".
Bullets: "Инспекторлор, ИДН кызматкерлеринин лекциялары;" "«Укук бузууга жол жок» темасында класстык сааттар;" "Буллингге каршы акция;" (exact spelling: Б-у-л-л-и-н-г-г-е) "Мектеп парламентинин иши;" "Окуучулар үчүн маалыматтык материалдар жана стенгазеталар."
Right: red prohibition circle over the word "БУЛЛИНГ", red label below "ЖОЛ ЖОК!" """,
9: """Title banner: "Жыйынтык жана сунуштар".
Bullets: "Үч багыт боюнча өткөрүлгөн иш-чаралар өз максатына жетти." "Окуучулар жол эрежесин сактоого, улуу муунга урмат көрсөтүүгө жана мыйзамга баш ийүүгө (exact: и-й-ү-ү-г-ө) ийгиликтүү үйрөнүштү." "Алдыда да мындай иш-чараларды улантуу сунушталат."
Right big italic blue text: "Коопсуз мектеп – биздин жалпы милдетибиз!" with a logo of united people under a rising sun.""",
}
n=int(sys.argv[1]); size=sys.argv[2] if len(sys.argv)>2 else "1536x1024"
P=COMMON.replace("Recreate this presentation slide","Create a presentation slide")+TEXTS[n]+"\nThe slide must fill the whole canvas; do not show any other slides or fragments."
r=requests.post("https://api.openai.com/v1/images/generations",headers={"Authorization":"Bearer sk-dummy"},
  json={"model":"gpt-image-2","prompt":P,"size":size,"quality":"high","stream":True,"partial_images":1},timeout=900,stream=True)
img=None
for line in r.iter_lines():
    if not line.startswith(b"data:"): 
        if line and not line.startswith(b"event:"): print(line[:300])
        continue
    ev=json.loads(line[5:])
    if ev.get("type","").endswith("completed"): img=ev["b64_json"]
    elif "error" in ev: print(ev); sys.exit(1)
if not img: print(n,"no image", r.status_code); sys.exit(1)
open(f"slide_{n}.png","wb").write(base64.b64decode(img)); print(n,"ok"); sys.exit(0)
print(r.status_code, r.text[:300]) if not r.text.startswith("{") else None
j=r.json()
if "data" not in j: print(n, json.dumps(j)[:500]); sys.exit(1)
open(f"slide_{n}.png","wb").write(base64.b64decode(j["data"][0]["b64_json"])); print(n,"ok")
