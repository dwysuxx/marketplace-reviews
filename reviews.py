"""MKT-12: Відгуки та оцінки (US-14).

User story: Як покупець, я хочу залишити відгук і оцінку після покупки,
щоб допомогти іншим покупцям.

Критерії приймання:
1. Оцінка — ціле число від 1 до 5.
2. Залишити відгук може лише покупець, який купив цей товар.
3. Один покупець — один відгук на товар.
4. Текст відгуку не довший за 1000 символів (порожній текст дозволено).
5. Середній рейтинг товару округлюється до 0,1; без відгуків рейтингу немає (None).
"""

MAX_TEXT_LENGTH = 1000


class ReviewError(ValueError):
    """Некоректний відгук."""


class ReviewBook:
    def __init__(self):
        self._purchases = set()   # (user_id, product_id)
        self._reviews = {}        # (user_id, product_id) -> (rating, text)

    def register_purchase(self, user_id, product_id):
        self._purchases.add((user_id, product_id))

    def add_review(self, user_id, product_id, rating, text=""):
        if isinstance(rating, bool) or not isinstance(rating, int):
            raise ReviewError("Оцінка має бути цілим числом")
        if not 1 <= rating <= 5:
            raise ReviewError("Оцінка має бути від 1 до 5")
        if len(text) > MAX_TEXT_LENGTH:
            raise ReviewError("Текст відгуку довший за 1000 символів")
        key = (user_id, product_id)
        if key not in self._purchases:
            raise ReviewError("Відгук може залишити лише покупець цього товару")
        if key in self._reviews:
            raise ReviewError("Покупець уже залишив відгук на цей товар")
        self._reviews[key] = (rating, text.strip())

    def reviews_for(self, product_id):
        return [r for (u, p), r in self._reviews.items() if p == product_id]

    def average_rating(self, product_id):
        ratings = [rating for rating, _ in self.reviews_for(product_id)]
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 1)
