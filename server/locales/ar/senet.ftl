# ترجمة لعبة سنت

game-name-senet = سنت

# بداية اللعبة
senet-game-started = { $p1 } هو اللاعب الأول، { $p2 } هو اللاعب الثاني. { $first } يبدأ أولاً.

# رمي العصي
senet-throw = { $player } يرمي { $result }.{ $bonus ->
    [yes] {" "}رمية إضافية!
   *[no] {""}
}

# الحركة
senet-move-you = تنتقل من المربع { $from } إلى المربع { $to }.
senet-move-other = { $player } ينتقل من المربع { $from } إلى المربع { $to }.
senet-swap-you = تتبادل المواقع مع { $opponent } على المربع { $to }. { $opponent } يعود إلى المربع { $from }.
senet-swap-other = { $player } يتبادل المواقع مع { $opponent } على المربع { $to }. { $opponent } يعود إلى المربع { $from }.
senet-bearoff-you = تخرج قطعتك من المربع { $from }. { $remaining } قطعة متبقية.
senet-bearoff-other = { $player } يخرج قطعته من المربع { $from }. { $remaining } قطعة متبقية.
senet-water-you = وصلت إلى بيت الماء! القطعة ترسل إلى المربع { $dest }.
senet-water-other = { $player } وصل إلى بيت الماء! القطعة ترسل إلى المربع { $dest }.
senet-happiness-you = وصلت إلى بيت السعادة.
senet-happiness-other = { $player } وصل إلى بيت السعادة.

# لا حركات متاحة
senet-no-moves-you = ليس لديك حركات مشروعة.
senet-no-moves-other = { $player } ليس لديه حركات مشروعة.

# تسميات المربعات
senet-sq-empty = { $sq }
senet-sq-own = { $sq }، قطعتك
senet-sq-opponent = { $sq }، { $owner }
senet-sq-empty-special = { $sq }، { $name }
senet-sq-own-special = { $sq }، { $name }، قطعتك
senet-sq-opponent-special = { $sq }، { $name }، { $owner }

# أسماء المربعات الخاصة
senet-house-rebirth = البعث
senet-house-happiness = السعادة
senet-house-water = الماء
senet-house-three-truths = الحقائق الثلاث
senet-house-re-atum = رع-آتوم

# الحالة
senet-status = { $p1 }: { $off1 } خارج. { $p2 }: { $off2 } خارج.{ $phase ->
    [throwing] {" "}في انتظار الرمي.
   *[moving] {" "}الرمية: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = لم يتم الرمي بعد.

# الفوز
senet-wins = { $player } فاز! جميع القطع خرجت.

# تسميات الإجراءات
senet-check-status = الحالة
senet-check-sticks = العصي
senet-check-score = النتيجة
senet-score = { $p1 }: { $off1 } خارج. { $p2 }: { $off2 } خارج.

# الأخطاء
senet-not-your-piece = هذه ليست قطعتك.
senet-no-piece-there = لا توجد قطعة هناك.
senet-no-moves-from-here = لا توجد حركات مشروعة من هذا المربع.

# الخيارات
senet-option-bot-difficulty = مستوى الروبوت: { $bot_difficulty }
senet-option-select-bot-difficulty = اختر مستوى الروبوت
senet-option-changed-bot-difficulty = تم تعيين مستوى الروبوت إلى { $bot_difficulty }.
senet-difficulty-random = عشوائي
senet-difficulty-simple = بسيط
