# real-insta-accountni-buzish
buni  ishlatish real targetlarda sinash qonunan  taqiqlanadi 
bu  o'quv  uchun  
Asosiy ishlash mantiqi
1. Password generation (5 xil format)

Foydalanuvchi kiritgan ma’lumotlar asosida:

    Format 1: ism + yil (masalan: john1990)

    Format 2: ism + raqam (masalan: john123)

    Format 3: ism + so‘z (masalan: johnlove)

    Format 4: ism + belgi (masalan: john!)

    Format 5: kombinatsiyalar (masalan: johnlove123)

Bu parollar cheksiz sikl bo‘yicha aylanadi:
1 → 2 → 3 → 4 → 5 → 1 → 2 → ...
2. 7 qatlamli himoya (anti-detection)
1️⃣ Fingerprint Generator

Har bir so‘rovda yangi brauzer fingerprint yaratadi:

    Ekran o‘lchami

    Timezone

    Til

    Platforma (Windows/Mac/Linux/iPhone)

    WebGL, Canvas, Audio fingerprint

    User-Agent (real brauzerga o‘xshab)

2️⃣ Smart Rate Controller

So‘rovlar chastotasini boshqaradi:

    Muvaffaqiyatsiz urinishlar ko‘paysa, kutish vaqti oshadi

    Rate limit (429) bo‘lsa, qo‘shimcha kutish

    Jitter qo‘shib, odamdek qiladi

3️⃣ Behavior Simulator

Odamdek harakatlarni qo‘shadi:

    So‘rovdan oldin va keyin kutish

    Tasodifiy scroll, mouse harakati

    Yozish tezligi simulyatsiyasi

4️⃣ Proxy Manager

TOR proxylarni boshqaradi:

    Har bir thread alohida TOR port orqali ishlaydi

    Proxy health check

    Muvaffaqiyatsiz proxylarni vaqtincha bloklaydi

5️⃣ Session Manager

Har bir proxy+fingerprint uchun alohida session va cookie saqlaydi.
6️⃣ Pattern Randomizer

Har bir so‘rovda turli request pattern ishlatadi:

    Ba’zida public key olish bilan

    Ba’zida tezroq

    Ba’zida extra delay bilan

7️⃣ Auto Recovery

Xatolik turlariga qarab avtomatik chora ko‘radi:

    Rate limit → IP almashtirish, session tozalash

    Challenge → mobile proxyga o‘tish, thread kamaytirish

    Bad request → User-Agent almashtirish
