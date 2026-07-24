# -*- coding: utf-8 -*-
import subprocess, os

SCRATCH = "/private/tmp/claude-501/-Users-stanislav-code-stanislav-v1/9d0230e4-280e-4706-96ef-b855e34827e5/scratchpad"

def ts(t):
    h = int(t//3600); m = int(t%3600//60); s = t%60
    return f"{h}:{m:02d}:{s:05.2f}"

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: EN,Arial,66,&H00FFFFFF,&H00FFFFFF,&H00181410,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,5,70,70,0,1
Style: UA,Arial,46,&H00E8D6C8,&H00FFFFFF,&H00181410,&H80000000,0,0,0,0,100,100,0,0,1,3,1,5,70,70,0,1
Style: ADLIB,Arial,54,&H00C8CFE8,&H00FFFFFF,&H00181410,&H80000000,0,-1,0,0,100,100,0,0,1,3,1,5,70,70,0,1
Style: TITLE,Arial,50,&H00FFFFFF,&H00FFFFFF,&H00181410,&H80000000,-1,0,0,0,100,100,2,0,1,3,1,8,40,40,120,1
Style: SUBT,Arial,28,&H00B8BFD4,&H00FFFFFF,&H00181410,&H80000000,0,0,0,0,100,100,3,0,1,2,0,8,40,40,196,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def build_ass(fname, title_ua, title_en, duration, lines):
    ev = []
    ev.append(f"Dialogue: 0,{ts(0.5)},{ts(duration-0.2)},TITLE,,0,0,0,,{{\\fad(400,400)}}{title_ua}")
    ev.append(f"Dialogue: 0,{ts(0.5)},{ts(duration-0.2)},SUBT,,0,0,0,,{{\\fad(400,400)}}{title_en}")
    for item in lines:
        if len(item) == 4:
            en, ua, a, b = item
            if en is None:
                ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},ADLIB,,0,0,0,,{{\\fad(250,250)}}{ua}")
            else:
                ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},EN,,0,0,0,,{{\\fad(250,250)}}{en}\\N{{\\rUA}}{ua}")
    open(os.path.join(SCRATCH, fname), "w").write(HEADER + "\n".join(ev) + "\n")

STEPS = [
    ("Warsaw. Morning.", "Варшава. Ранок.", 3.4, 6.0),
    ("My son says: today we walk!", "Син каже: сьогодні ми гуляємо!", 6.0, 10.2),
    ("I say: okay. A small walk.", "Я кажу: добре. Маленька прогулянка.", 10.2, 16.8),
    ("One hundred steps! Two hundred! Three!", "Сто кроків! Двісті! Триста!", 17.9, 22.0),
    ("The morning is good! Warsaw, I come!", "Ранок гарний! Варшаво, я йду!", 22.0, 25.7),
    ("One thousand steps! Okay! Good!", "Тисяча кроків! Окей! Добре!", 25.7, 29.5),
    ("Two thousand! ...Where is breakfast?!", "Дві тисячі! ...Де сніданок?!", 29.5, 35.6),
    ("Four thousand steps — we eat. We go!", "Чотири тисячі кроків — ми їмо. Йдемо!", 36.6, 40.1),
    ("Six thousand steps — we eat again!", "Шість тисяч кроків — знову їмо!", 40.1, 44.5),
    ("Eight thousand — my phone says: STOP.", "Вісім тисяч — телефон каже: СТОП.", 44.5, 48.4),
    ("My son says: no! Come! We go!", "Син каже: ні! Давай! Ідемо!", 48.4, 52.3),
    ("SEVENTEEN THOUSAND STEPS! (left! right!)", "СІМНАДЦЯТЬ ТИСЯЧ КРОКІВ! (лівою! правою!)", 52.3, 56.4),
    ("SEVENTEEN THOUSAND STEPS!", "СІМНАДЦЯТЬ ТИСЯЧ КРОКІВ!", 56.4, 58.9),
    ("My phone says: who ARE you today?!", "Телефон питає: хто ти сьогодні ВЗАГАЛІ?!", 58.9, 63.0),
    ("I say: I don't know! I WALK!", "Я кажу: не знаю! Я ЙДУ!", 63.0, 69.3),
    ("Twelve thousand... slowly... slowly...", "Дванадцять тисяч... повільно... повільно...", 70.5, 76.0),
    ("I see a taxi. I say: TAXI!", "Бачу таксі. Кажу: ТАКСІ!", 76.0, 81.0),
    ("My son says: NO. We walk.", "Син каже: НІ. Ми йдемо пішки.", 81.0, 86.0),
    (None, "«Я тобі це запам'ятаю...»", 86.0, 91.0),
    ("Fifteen thousand... I want my bed...", "П'ятнадцять тисяч... хочу в ліжко...", 91.2, 94.8),
    ("Sixteen thousand... I want my beer...", "Шістнадцять тисяч... хочу пива...", 94.8, 97.2),
    ("Seventeen thousand — THE HOTEL!", "Сімнадцять тисяч — ГОТЕЛЬ!", 97.2, 100.7),
    ("I SEE THE HOTEL! WE ARE HERE!", "Я БАЧУ ГОТЕЛЬ! МИ ТУТ!", 100.7, 106.8),
    ("SEVENTEEN THOUSAND STEPS! (left! right!)", "СІМНАДЦЯТЬ ТИСЯЧ КРОКІВ! (лівою! правою!)", 108.6, 112.5),
    ("SEVENTEEN THOUSAND STEPS!", "СІМНАДЦЯТЬ ТИСЯЧ КРОКІВ!", 112.5, 116.0),
    ("My phone says: who ARE you today?!", "Телефон питає: хто ти сьогодні ВЗАГАЛІ?!", 116.0, 119.5),
    ("I say: I don't know! I WALK!", "Я кажу: не знаю! Я ЙДУ!", 119.5, 124.5),
    ("Night. The bed is good. Very good.", "Ніч. Ліжко хороше. Дуже хороше.", 139.0, 142.0),
    ("My phone says: seventeen thousand steps.", "Телефон каже: сімнадцять тисяч кроків.", 142.0, 145.0),
    ("I say... yes. I do it. Me!", "Я кажу... так. Я це зробив. Я!", 145.0, 147.6),
    ("Tomorrow? The bus. The bus, please.", "Завтра? Автобус. Автобус, будь ласка.", 147.6, 153.8),
]

TOMA = [
    ("Nafplio. A restaurant by the water.", "Нафпліо. Ресторан біля води.", 4.0, 7.8),
    ("A beautiful night.", "Прекрасний вечір.", 7.8, 11.5),
    ("...I remember everything.", "...Я пам'ятаю все.", 11.5, 16.0),
    ("The candles burn by the quiet water,", "Свічки горять біля тихої води,", 42.4, 48.5),
    ("my son sits happy across from me.", "навпроти мене сидить щасливий син.", 48.5, 54.0),
    ("But right behind him — two elegant women,", "Але просто за ним — дві елегантні жінки,", 54.0, 60.0),
    ("and what they ordered... I can't believe.", "і те, що вони замовили... я не можу повірити.", 60.0, 66.2),
    ("The waiter brings it high, like a trophy:", "Офіціант несе його високо, як трофей:", 66.5, 72.0),
    ("a TOMAHAWK. One steak. One bone.", "ТОМАГАВК. Один стейк. Одна кістка.", 72.0, 77.5),
    ("I look at them. I look at the meat.", "Я дивлюсь на них. Дивлюсь на м'ясо.", 77.5, 83.0),
    ("They can't be serious... Oh. They are.", "Вони ж це не серйозно... О. Серйозно.", 83.0, 87.2),
    ("TO-MA-HAWK! (tomahawk!)", "ТО-МА-ГАВК!", 87.2, 89.6),
    ("Two women! One mountain of meat!", "Дві жінки! Одна гора м'яса!", 89.6, 91.4),
    ("I try to eat, I try to talk —", "Я намагаюсь їсти, намагаюсь говорити —", 91.4, 93.3),
    ("I can't stop watching them EAT!", "але не можу відірватись, як вони ЇДЯТЬ!", 93.3, 96.4),
    ("TO-MA-HAWK! (tomahawk!)", "ТО-МА-ГАВК!", 96.4, 99.6),
    ("The bone is as long as my arm!", "Кістка довга, як моя рука!", 99.6, 102.4),
    ("How could they eat it? HOW COULD THEY EAT IT?!", "Як вони його з'їли? ЯК ВОНИ ЙОГО З'ЇЛИ?!", 102.4, 106.4),
    ("...They ate it all. They ate it ALL!", "...Вони з'їли все. З'ЇЛИ ВСЕ!", 106.4, 110.8),
    ("My son says, \"Dad, your dinner is getting cold.\"", "Син каже: «Тату, твоя вечеря холоне».", 112.0, 117.0),
    ("My dinner? WHO CARES about my dinner?!", "Вечеря? КОГО ХВИЛЮЄ моя вечеря?!", 117.0, 122.0),
    ("Behind you, son, a miracle is happening —", "За тобою, сину, відбувається диво —", 122.0, 127.0),
    ("two women versus one ENORMOUS dish!", "дві жінки проти однієї ВЕЛЕТЕНСЬКОЇ страви!", 127.0, 132.2),
    ("And bite by bite, the mountain got smaller...", "І шматок за шматком гора меншала...", 132.5, 137.5),
    ("no hurry... laughing... a glass of wine...", "без поспіху... зі сміхом... з келихом вина...", 137.5, 142.5),
    ("An hour later — I swear it, I saw it —", "Через годину — клянусь, я сам бачив —", 142.5, 147.5),
    ("the plate was empty. The bone was CLEAN.", "тарілка порожня. Кістка ЧИСТА.", 147.5, 152.6),
    ("TO-MA-HAWK! (tomahawk!)", "ТО-МА-ГАВК!", 153.0, 155.5),
    ("Two women! One mountain of meat!", "Дві жінки! Одна гора м'яса!", 155.5, 158.0),
    ("I try to eat, I try to talk —", "Я намагаюсь їсти, намагаюсь говорити —", 158.0, 160.5),
    ("I can't stop watching them EAT!", "але не можу відірватись, як вони ЇДЯТЬ!", 160.5, 163.5),
    ("TO-MA-HAWK! (tomahawk!)", "ТО-МА-ГАВК!", 163.5, 166.5),
    ("The bone is as long as my arm!", "Кістка довга, як моя рука!", 166.5, 169.5),
    ("How could they eat it? HOW COULD THEY EAT IT?!", "Як вони його з'їли? ЯК ВОНИ ЙОГО З'ЇЛИ?!", 169.5, 173.0),
    ("...They ate it all. They ate it ALL!", "...Вони з'їли все. З'ЇЛИ ВСЕ!", 173.0, 176.6),
    ("That night I could not sleep at all.", "Тієї ночі я не міг заснути.", 176.8, 179.4),
    ("My son said, \"Dad, please. Let it go.\"", "Син сказав: «Тату, будь ласка. Забудь».", 179.4, 181.9),
    ("Let it go?! LET IT GO?!", "Забудь?! ЗАБУДЬ?!", 181.9, 184.2),
    ("Two women... one tomahawk... and NOTHING left!", "Дві жінки... один томагавк... і НІЧОГО не лишилось!", 184.2, 189.8),
    ("A week goes by. We're back at home.", "Минає тиждень. Ми вже вдома.", 194.9, 198.6),
    ("And still, at dinner, I look up and say:", "І досі за вечерею я підводжу очі й кажу:", 198.6, 203.5),
    ("\"...But HOW could they eat it?\"", "«...Але ЯК вони його з'їли?»", 203.5, 208.8),
    ("Nobody knows... nobody knows...", "Ніхто не знає... ніхто не знає...", 209.5, 216.5),
    ("(To-ma-hawk...)", "(пошепки) То-ма-гавк...", 217.0, 223.0),
]

build_ass("steps.ass", "17 000 КРОКІВ", "SEVENTEEN THOUSAND STEPS  ·  Warsaw 2026", 167.9, STEPS)
build_ass("toma.ass", "ТОМАГАВК", "THE TOMAHAWK WOMEN  ·  Nafplio 2026", 231.5, TOMA)
print("ass files written")

JOBS = [
    ("steps.ass", "/Users/stanislav/Downloads/Seventeen Thousand Steps.mp3",
     "gradients=s=1080x1920:speed=0.012:nb_colors=3:c0=0x141a3d:c1=0x2a1548:c2=0x54123a:x0=200:y0=200:x1=900:y1=1750",
     "/Users/stanislav/Downloads/17000-krokiv-tiktok.mp4", 167.92),
    ("toma.ass", "/Users/stanislav/Downloads/How Could They Eat It.mp3",
     "gradients=s=1080x1920:speed=0.012:nb_colors=3:c0=0x2b0a12:c1=0x4a1020:c2=0x1a0a2e:x0=200:y0=200:x1=900:y1=1750",
     "/Users/stanislav/Downloads/tomahawk-tiktok.mp4", 231.52),
]

for ass, mp3, grad, out, dur in JOBS:
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", grad + f":d={dur+0.5}",
        "-i", mp3,
        "-filter_complex",
        f"[1:a]showwaves=s=1080x220:mode=cline:colors=0xFFFFFF@0.25:rate=30[wv];"
        f"[0:v][wv]overlay=0:1580[bg];"
        f"[bg]subtitles={ass}[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "320k", "-shortest", out,
    ]
    print("rendering", out)
    r = subprocess.run(cmd, cwd=SCRATCH, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:\n", r.stderr[-3000:])
        raise SystemExit(1)
print("done")
