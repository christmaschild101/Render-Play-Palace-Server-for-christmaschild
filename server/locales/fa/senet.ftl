# ترجمه بازی سنت

game-name-senet = سنت

# شروع بازی
senet-game-started = { $p1 } بازیکن اول است، { $p2 } بازیکن دوم است. { $first } اول شروع می‌کند.

# پرتاب چوب‌ها
senet-throw = { $player } { $result } پرتاب می‌کند.{ $bonus ->
    [yes] {" "}پرتاب اضافه!
   *[no] {""}
}

# حرکت
senet-move-you = از خانه { $from } به خانه { $to } حرکت می‌کنید.
senet-move-other = { $player } از خانه { $from } به خانه { $to } حرکت می‌کند.
senet-swap-you = با { $opponent } در خانه { $to } جابه‌جا می‌شوید. { $opponent } به خانه { $from } برمی‌گردد.
senet-swap-other = { $player } با { $opponent } در خانه { $to } جابه‌جا می‌شود. { $opponent } به خانه { $from } برمی‌گردد.
senet-bearoff-you = مهره‌تان از خانه { $from } خارج می‌شود. { $remaining } مهره باقی‌مانده.
senet-bearoff-other = { $player } مهره‌اش را از خانه { $from } خارج می‌کند. { $remaining } مهره باقی‌مانده.
senet-water-you = به خانه آب رسیدید! مهره به خانه { $dest } فرستاده شد.
senet-water-other = { $player } به خانه آب رسید! مهره به خانه { $dest } فرستاده شد.
senet-happiness-you = به خانه شادی رسیدید.
senet-happiness-other = { $player } به خانه شادی رسید.

# بدون حرکت
senet-no-moves-you = هیچ حرکت قانونی ندارید.
senet-no-moves-other = { $player } هیچ حرکت قانونی ندارد.

# برچسب خانه‌ها
senet-sq-empty = { $sq }
senet-sq-own = { $sq }، مهره شما
senet-sq-opponent = { $sq }، { $owner }
senet-sq-empty-special = { $sq }، { $name }
senet-sq-own-special = { $sq }، { $name }، مهره شما
senet-sq-opponent-special = { $sq }، { $name }، { $owner }

# نام خانه‌های ویژه
senet-house-rebirth = تولد دوباره
senet-house-happiness = شادی
senet-house-water = آب
senet-house-three-truths = سه حقیقت
senet-house-re-atum = رع-آتوم

# وضعیت
senet-status = { $p1 }: { $off1 } خارج. { $p2 }: { $off2 } خارج.{ $phase ->
    [throwing] {" "}در انتظار پرتاب.
   *[moving] {" "}نتیجه پرتاب: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = هنوز پرتابی انجام نشده.

# برنده
senet-wins = { $player } برنده شد! همه مهره‌ها خارج شدند.

# برچسب‌های عملکرد
senet-check-status = وضعیت
senet-check-sticks = چوب‌ها
senet-check-score = امتیاز
senet-score = { $p1 }: { $off1 } خارج. { $p2 }: { $off2 } خارج.

# خطاها
senet-not-your-piece = این مهره شما نیست.
senet-no-piece-there = در اینجا مهره‌ای وجود ندارد.
senet-no-moves-from-here = هیچ حرکت قانونی از این خانه وجود ندارد.

# گزینه‌ها
senet-option-bot-difficulty = سطح دشواری ربات: { $bot_difficulty }
senet-option-select-bot-difficulty = انتخاب سطح دشواری ربات
senet-option-changed-bot-difficulty = سطح دشواری ربات به { $bot_difficulty } تنظیم شد.
senet-difficulty-random = تصادفی
senet-difficulty-simple = ساده
