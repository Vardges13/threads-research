#!/usr/bin/env python3
"""Upload reels-scenarios.md to Notion as a structured page."""

import json
import urllib.request
import urllib.error

API_KEY = "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"
API_VERSION = "2025-09-03"
PARENT_PAGE_ID = "2fc83182-3725-80e5-9ebc-f4c8df0eac09"
PAGE_TITLE = "🎬 Сценарии Reels — 10 штук"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Notion-Version": API_VERSION,
    "Content-Type": "application/json",
}


def notion_request(method, endpoint, data=None):
    url = f"https://api.notion.com/v1/{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"HTTP {e.code}: {err_body}")
        raise


def rich_text(text, bold=False, italic=False, code=False):
    """Create a rich_text element, splitting if >2000 chars."""
    items = []
    while text:
        chunk = text[:2000]
        text = text[2000:]
        items.append({
            "type": "text",
            "text": {"content": chunk},
            "annotations": {
                "bold": bold,
                "italic": italic,
                "strikethrough": False,
                "underline": False,
                "code": code,
                "color": "default",
            },
        })
    return items


def heading_2(text):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": rich_text(text[:2000])},
    }


def heading_3(text):
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": rich_text(text[:2000])},
    }


def paragraph(text, bold=False, italic=False):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": rich_text(text, bold=bold, italic=italic)},
    }


def bulleted(text, bold=False):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text(text, bold=bold)},
    }


def callout(text, emoji="💡"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": rich_text(text),
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


def divider():
    return {"object": "block", "type": "divider", "divider": {}}


def parse_and_build_blocks():
    """Parse the markdown and build Notion blocks."""
    blocks = []

    # Intro
    blocks.append(paragraph(
        "10 сценариев Reels/TikTok — прогрев перед запуском курса",
        bold=True
    ))
    blocks.append(paragraph(
        "Курс: «Обгони конкурентов: 50 GPT-агентов в твой бизнес»\n"
        "Автор: Вардгес Арутюнян — предприниматель 15+ лет, туризм + отель, Курск"
    ))
    blocks.append(divider())

    # ===== РИЛС 1 =====
    blocks.append(heading_2("Рилс 1. «Я заменил 3 сотрудников на ИИ»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес смотрит в камеру, пауза, потом:", italic=True))
    blocks.append(paragraph("«Я уволил трёх сотрудников. И мне ни капли не стыдно.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (45 сек)", bold=True))
    blocks.append(paragraph(
        "«Я уволил трёх сотрудников. И мне ни капли не стыдно.\n\n"
        "Стоп-стоп, не спешите кидать тапком. Я никого не выгнал на улицу. "
        "Просто трое уволились сами — и я решил НЕ нанимать новых.\n\n"
        "Вместо этого я настроил GPT-агентов.\n\n"
        "Один — обрабатывает заявки на туры. Отвечает клиентам за 30 секунд. "
        "Раньше менеджер отвечал через полчаса. Или забывал вообще.\n\n"
        "Второй — пишет посты, письма, описания отелей. То, на что копирайтер "
        "тратил день, агент делает за 5 минут.\n\n"
        "Третий — считает, анализирует, формирует отчёты.\n\n"
        "Экономия? 180 тысяч в месяц на зарплатах. Плюс — ноль больничных, "
        "ноль опозданий, ноль «а я думал, это не моя задача».\n\n"
        "Я не против людей. Я за то, чтобы люди занимались тем, что ИИ НЕ может. "
        "А рутину — отдай машине.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Формат: говорящая голова, крупный план, прямой взгляд в камеру"))
    blocks.append(bulleted("Фон: офис или ресепшн отеля (реальный, не студийный)"))
    blocks.append(bulleted("На словах про каждого «сотрудника» — быстрая врезка скринов: чат-бот отвечает клиенту / текст генерируется / дашборд с цифрами"))
    blocks.append(bulleted("Текст на экране: «180 000 ₽/мес экономия» — появляется с ударным звуком"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Трендовый бит с нарастанием (энергичный, уверенный). В момент «180 тысяч» — звук cash register / монеты."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Хочешь узнать, каких сотрудников в ТВОЁМ бизнесе можно заменить на ИИ? Подпишись — скоро покажу всю систему.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#ИИдлябизнеса #GPTагенты #автоматизация #предприниматель #нейросети #бизнесбезсотрудников #ИИзаменитвсех"))

    blocks.append(divider())

    # ===== РИЛС 2 =====
    blocks.append(heading_2("Рилс 2. «GPT-агент написал КП за 2 минуты»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес за ноутбуком, поворачивается к камере:", italic=True))
    blocks.append(paragraph("«Смотри, что сейчас будет. Коммерческое предложение за 2 минуты.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (50 сек)", bold=True))
    blocks.append(paragraph(
        "«Мне написал клиент — корпоративная группа, 40 человек, хотят в Сочи на тимбилдинг. Нужно КП.\n\n"
        "Раньше я бы сел, открыл Ворд, начал мучиться: \"Уважаемый Иван Петрович, рады предложить вам...\" — полтора часа, три правки, и всё равно криво.\n\n"
        "Сейчас я делаю так.\n\n"
        "Пишу агенту: «КП для корпоратива, 40 человек, Сочи, бюджет 2 млн, тимбилдинг + банкет». Жму Enter.\n\n"
        "Всё. Красивое КП с разбивкой по дням, вариантами отелей, стоимостью. Осталось проверить цифры и отправить.\n\n"
        "Две минуты. Не полтора часа. Две минуты.\n\n"
        "А теперь вопрос: ты до сих пор КП руками пишешь? Серьёзно?»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Начало: Вардгес за столом с ноутбуком, камера чуть сбоку"))
    blocks.append(bulleted("Переход: скринкаст экрана — вводит запрос в GPT-агента"))
    blocks.append(bulleted("Результат на экране — красивый документ появляется"))
    blocks.append(bulleted("Сплит-скрин: слева «Раньше: 1.5 часа 😩» / справа «Сейчас: 2 мин 🚀»"))
    blocks.append(bulleted("Возврат на лицо Вардгеса — ухмылка"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Фоновый лёгкий lo-fi бит. В момент генерации — ускоренный звук печати (typewriter). На финале — звук «тадам»."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Сохрани это видео. А лучше — подпишись. Я покажу, как настроить такого агента с нуля. Без кода.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#КПзадвеминуты #GPTдлябизнеса #нейросетидляработы #автоматизациябизнеса #ИИпомощник #турбизнес #продажи"))

    blocks.append(divider())

    # ===== РИЛС 3 =====
    blocks.append(heading_2("Рилс 3. «Почему 90% предпринимателей используют ИИ неправильно»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес качает головой, разочарованно:", italic=True))
    blocks.append(paragraph("«Ты используешь ChatGPT как гугл. И это — проблема.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (50 сек)", bold=True))
    blocks.append(paragraph(
        "«Девять из десяти предпринимателей, которых я знаю, используют ИИ вот так: открывают ChatGPT, "
        "спрашивают \"напиши мне пост для Инстаграма\". Получают пресный текст. Говорят \"ну фигня ваш ИИ\" и закрывают.\n\n"
        "Это как купить Мерседес и ездить на нём только до магазина за хлебом.\n\n"
        "ИИ — это не поисковик. Это твой сотрудник. Но чтобы сотрудник работал хорошо, ему нужно ЧТО? "
        "Правильно — должностная инструкция.\n\n"
        "Промпт — это и есть должностная инструкция.\n\n"
        "Когда я даю агенту контекст — кто мой клиент, какой тон, какая цель, какие примеры — "
        "он выдаёт результат, который менеджер не напишет и за три дня.\n\n"
        "Проблема не в ИИ. Проблема в том, что ты не умеешь им управлять. Пока.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Формат: Вардгес стоит, жестикулирует, энергично"))
    blocks.append(bulleted("Текст на экране: «90% используют ИИ НЕПРАВИЛЬНО» — крупно, с красным акцентом"))
    blocks.append(bulleted("На примере «Мерседес за хлебом» — быстрая мемная врезка"))
    blocks.append(bulleted("В конце — текст: «Промпт = должностная инструкция»"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Драматичный бит в начале (разоблачение), потом переход в уверенный ритм. На «Мерседесе» — звук мотора."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Напиши в комментах \"ПРОМПТ\" — скину пример, как правильно ставить задачу ИИ. Это бесплатно.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#ChatGPT #промптинжиниринг #ИИнеработает #нейросетидлябизнеса #ошибкипредпринимателей #GPTагенты #бизнесхак"))

    blocks.append(divider())

    # ===== РИЛС 4 =====
    blocks.append(heading_2("Рилс 4. «Мой ИИ-помощник работает 24/7 и не просит зарплату»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес лежит на диване, показывает телефон:", italic=True))
    blocks.append(paragraph("«3 часа ночи. Мой сотрудник только что закрыл сделку. А я даже не проснулся.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (45 сек)", bold=True))
    blocks.append(paragraph(
        "«Три часа ночи. Клиент из Владивостока — у них уже утро — пишет: хочу тур на двоих в Турцию на майские. Бюджет 300 тысяч.\n\n"
        "Мой GPT-агент тут же отвечает. Предлагает три варианта. Уточняет даты. Берёт контакт. Ставит заявку в CRM.\n\n"
        "Я просыпаюсь — а у меня горячий лид лежит, готовый к оплате.\n\n"
        "Ни один живой менеджер не будет сидеть в три часа ночи. А агент — будет. И в выходные. И в праздники. И в отпуске.\n\n"
        "Я не плачу ему зарплату. Он не берёт больничный. Не уходит к конкурентам. Не обижается на тон в сообщении.\n\n"
        "Это не фантастика. Это мой вторник.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Начало: Вардгес в домашней обстановке, приглушённый свет, часы — 03:00"))
    blocks.append(bulleted("Врезка: экран телефона с чатом — бот общается с клиентом"))
    blocks.append(bulleted("Переход: утро, Вардгес с кофе, открывает CRM — там заявка"))
    blocks.append(bulleted("Текст на экране: «24/7. Без зарплаты. Без выходных.»"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Начало — тишина + звук уведомления на телефоне. Потом мягкий бит, нарастающий к финалу."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Хочешь такого же помощника? Жми подписку — скоро расскажу, как настроить это за один вечер.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#ИИпомощник #автоматизация #пассивныйдоход #бизнес247 #GPTбот #чатбот #нейросетидлябизнеса"))

    blocks.append(divider())

    # ===== РИЛС 5 =====
    blocks.append(heading_2("Рилс 5. «Как я экономлю 4 часа в день с помощью ИИ»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес показывает на часы:", italic=True))
    blocks.append(paragraph("«Четыре часа. Каждый день. Вот столько времени я себе вернул.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (55 сек)", bold=True))
    blocks.append(paragraph(
        "«Посчитай, сколько времени ты тратишь на рутину. Я посчитал.\n\n"
        "Ответы клиентам в мессенджерах — час. Написать пост, письмо, описание — час. "
        "Разобрать отчёты, свести цифры — час. Подготовить КП или презентацию — ещё час.\n\n"
        "Четыре часа. Каждый рабочий день. 20 часов в неделю. 80 часов в месяц.\n\n"
        "Это ДВЕ полные рабочие недели в месяц — на рутину.\n\n"
        "Сейчас всё это делают мои GPT-агенты. Я трачу 15 минут утром — проверить, подкорректировать, запустить.\n\n"
        "А освободившиеся 4 часа? Стратегия. Новые направления. Или просто — поехать с семьёй на обед, "
        "а не сидеть в офисе до восьми.\n\n"
        "Время — это единственный ресурс, который нельзя купить. Но можно перестать тратить его на фигню.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Вардгес стоит у доски / флипчарта, пишет маркером расчёт"))
    blocks.append(bulleted("Таймлапс: 1 час + 1 час + 1 час + 1 час = 4 часа"))
    blocks.append(bulleted("Перечёркивает красным маркером"))
    blocks.append(bulleted("Врезка: Вардгес с семьёй / на прогулке (лайфстайл)"))
    blocks.append(bulleted("Финальный кадр: текст «80 часов/мес = 2 рабочие недели»"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Мотивационный бит, средний темп. Звук маркера по доске. На финале — вдохновляющий подъём."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Напиши \"ВРЕМЯ\" в комментах — скину чек-лист: какие задачи в твоём бизнесе можно отдать ИИ уже сегодня.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#таймменеджмент #4часавдень #ИИдлябизнеса #продуктивность #автоматизация #GPTагенты #предпринимательство"))

    blocks.append(divider())

    # ===== РИЛС 6 =====
    blocks.append(heading_2("Рилс 6. «Тебе не нужен программист — тебе нужен промпт»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес поднимает руку, как бы останавливая:", italic=True))
    blocks.append(paragraph("«Стоп. Отложи кошелёк. Тебе НЕ нужен программист за 200 тысяч.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (50 сек)", bold=True))
    blocks.append(paragraph(
        "«Каждый второй предприниматель мне говорит: \"Вардгес, ну это ж надо разработчика нанимать, "
        "бота писать, CRM интегрировать...\"\n\n"
        "Нет. Не надо.\n\n"
        "Я — не айтишник. Я вообще из туризма. У меня отель и турагентство в Курске. "
        "Код я последний раз видел на уроке информатики в школе.\n\n"
        "Но я настроил 50 GPT-агентов. Сам. Без единой строчки кода.\n\n"
        "Потому что сегодня тебе не нужен код — тебе нужен промпт. Это текст. На русском языке. "
        "Который ты пишешь как ТЗ сотруднику.\n\n"
        "\"Ты — менеджер по продажам. Твоя задача — ответить клиенту, уточнить бюджет, предложить три варианта.\" "
        "Всё. Агент работает.\n\n"
        "Самый дорогой навык 2026 года — не программирование. Это умение разговаривать с ИИ.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Вардгес в кадре, стоя, уверенно жестикулирует"))
    blocks.append(bulleted("Текст на экране: «200 000 ₽ за разработчика» — перечёркивается"))
    blocks.append(bulleted("Показывает экран: простой промпт в чате — и результат"))
    blocks.append(bulleted("Финал: текст «Промпт > Код»"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Уверенный, чуть дерзкий бит. На «перечёркивании» — звук зачёркивания / удаления."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Подпишись — я покажу, как написать первого GPT-агента за 10 минут. Даже если ты полный ноль в технике.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#безкода #ноукод #промпт #GPTагенты #предпринимательство #ИИпросто #бизнесавтоматизация"))

    blocks.append(divider())

    # ===== РИЛС 7 =====
    blocks.append(heading_2("Рилс 7. «50 агентов в одном бизнесе — это как?»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес загибает пальцы, потом бросает руки:", italic=True))
    blocks.append(paragraph("«У меня в бизнесе работают 50 ИИ-агентов. И я не шучу.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (55 сек)", bold=True))
    blocks.append(paragraph(
        "«Люди слышат \"50 агентов\" и думают — это какая-то космическая станция. Сервер в подвале. Команда нёрдов.\n\n"
        "Не-а. Это просто 50 конкретных задач, которые раньше делали люди — а сейчас делает ИИ.\n\n"
        "Вот смотри. Агент для ответов в WhatsApp. Агент для подбора туров. Агент для написания постов. "
        "Агент для анализа конкурентов. Агент для составления смет. Агент для подготовки отзывов. "
        "Агент для email-рассылок...\n\n"
        "Каждый — заточен под одну задачу. Как отвёртка — под один шуруп. Не универсальный робот, "
        "а 50 точных инструментов.\n\n"
        "И знаешь, что самое крутое? Я их собирал не все разом. По одному. Одна неделя — один агент. "
        "За год — целая система, которая работает как часы.\n\n"
        "Тебе не надо 50 сразу. Начни с одного. Того, который закроет самую большую боль.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Вардгес считает на пальцах — потом машет рукой «не хватит пальцев»"))
    blocks.append(bulleted("Текст-список: агенты пролетают один за другим (анимация)"))
    blocks.append(bulleted("Схема: один большой круг «Бизнес» → 50 маленьких кругов-агентов"))
    blocks.append(bulleted("Финал: «1 неделя = 1 агент»"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Быстрый, энергичный бит. На перечислении агентов — ритмичные «тик-тик-тик» как счётчик."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«С какого агента начал бы ТЫ? Пиши в комментах свою задачу — подскажу, какого агента делать первым.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#50агентов #GPTагенты #системавбизнесе #ИИпомощники #автоматизациябизнеса #масштабирование #предприниматель"))

    blocks.append(divider())

    # ===== РИЛС 8 =====
    blocks.append(heading_2("Рилс 8. «ИИ для турбизнеса: реальный кейс»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес хлопает в ладоши:", italic=True))
    blocks.append(paragraph("«Клиент написал \"хочу в Египет\". Через 47 секунд он получил три готовых предложения.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (55 сек)", bold=True))
    blocks.append(paragraph(
        "«У меня турагентство. Классическая история: клиент пишет в WhatsApp — \"хочу на море в апреле, бюджет средний\".\n\n"
        "Раньше менеджер открывал пять сайтов, сравнивал цены, подбирал варианты, оформлял в документ. "
        "Минимум — 40 минут. Если клиентов пять одновременно — коллапс.\n\n"
        "Сейчас мой агент делает это за 47 секунд. Я засекал.\n\n"
        "Он знает все актуальные направления. Он знает, какие отели наш клиент любит. "
        "Он учитывает бюджет, даты, состав группы. И выдаёт красивый ответ с ценами и фотками.\n\n"
        "Менеджер подключается только когда надо закрыть сделку — позвонить, дожать, обсудить нюансы. "
        "То, где нужен живой человек.\n\n"
        "Результат? Конверсия выросла на 30%. Потому что клиент получает ответ СРАЗУ, а не через два часа, "
        "когда он уже ушёл к конкуренту.\n\n"
        "Это не теория. Это мой Курск. Мой бизнес. Мои цифры.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Начало: экран WhatsApp — приходит сообщение от клиента"))
    blocks.append(bulleted("Таймер на экране: 0 → 47 секунд"))
    blocks.append(bulleted("Скринкаст: агент формирует ответ с вариантами, фотками отелей"))
    blocks.append(bulleted("Вардгес в кадре, показывает графики: конверсия до/после"))
    blocks.append(bulleted("Текст: «+30% конверсия»"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Тиканье таймера (47 секунд). Потом — победный звук. Фоновый бит — позитивный, динамичный."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Если ты в туризме — подпишись обязательно. Я расскажу, как настроить такого агента под свою нишу.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#турбизнес #турагентство #ИИвтуризме #автоматизация #GPTагенты #кейс #конверсия"))

    blocks.append(divider())

    # ===== РИЛС 9 =====
    blocks.append(heading_2("Рилс 9. «Конкуренты не спят — они уже используют ИИ»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес наклоняется к камере, говорит тихо, как секрет:", italic=True))
    blocks.append(paragraph("«Пока ты думаешь \"мне это не надо\" — твой конкурент уже внедрил.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (50 сек)", bold=True))
    blocks.append(paragraph(
        "«Я общаюсь с предпринимателями каждый день. И вижу два типа.\n\n"
        "Первый: \"Ну это хайп, ChatGPT — игрушка, мне и так нормально.\" Сидит, делает всё руками, как в 2015 году.\n\n"
        "Второй: тихо, без лишнего шума, внедряет агентов. Автоматизирует продажи. Снижает косты. "
        "Обрабатывает в три раза больше заявок с тем же штатом.\n\n"
        "Через год первый будет гадать — почему клиенты уходят? Почему конкурент дешевле? "
        "Почему он быстрее отвечает?\n\n"
        "А ответ простой: конкурент не умнее тебя. Он просто начал раньше.\n\n"
        "Самое болезненное — ИИ не даёт преимущество тем, кто его использует. "
        "Он создаёт ПРОБЛЕМУ тем, кто его НЕ использует.\n\n"
        "Подумай об этом.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Начало: Вардгес говорит тихо, камера медленно наезжает (zoom in)"))
    blocks.append(bulleted("Сплит-экран: «Предприниматель 1» — хаос / «Предприниматель 2» — графики вверх"))
    blocks.append(bulleted("Текст: «Преимущество ≠ тем, кто использует. Проблема = тем, кто НЕ использует.»"))
    blocks.append(bulleted("Финал: чёрный экран с белым текстом — цитата"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Начало — тревожный, низкий бит (suspense). К финалу — нарастание, эпичный звук."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Не будь первым типом. Подпишись — я помогу начать. Без воды, без теории. Только практика.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#конкуренция #ИИвбизнесе #цифроваятрансформация #нейросети #бизнес2026 #GPTагенты #предпринимательство"))

    blocks.append(divider())

    # ===== РИЛС 10 =====
    blocks.append(heading_2("Рилс 10. «Что будет с бизнесом через год, если ты не внедришь ИИ»"))

    blocks.append(bulleted("🎣 Крючок (первые 2 сек)", bold=True))
    blocks.append(paragraph("Вардгес серьёзным тоном, прямо в камеру:", italic=True))
    blocks.append(paragraph("«Через год 40% малого бизнеса потеряют клиентов. И вот почему.»", bold=True))

    blocks.append(bulleted("📝 Сценарий (55 сек)", bold=True))
    blocks.append(paragraph(
        "«Давай начистоту. Без розовых очков.\n\n"
        "Что будет через год?\n\n"
        "Клиенты привыкнут к мгновенным ответам. Потому что кто-то уже отвечает им за секунды. "
        "И если ты отвечаешь через час — тебя просто вычёркивают.\n\n"
        "Стоимость привлечения клиента вырастет — и те, кто не автоматизировал воронку, "
        "будут платить вдвое больше за тот же результат.\n\n"
        "Контент будут генерировать потоком — а ты будешь сидеть раз в неделю и мучить один пост.\n\n"
        "Это не страшилка. Это математика. Кто быстрее — тот и ест. Так было всегда, "
        "просто сейчас \"быстрее\" значит — с ИИ.\n\n"
        "Я 15 лет в бизнесе. Я видел, как уходили те, кто не перешёл в интернет. "
        "Потом — те, кто не зашёл в соцсети. Сейчас — те, кто не внедрит ИИ.\n\n"
        "У тебя ещё есть время. Но оно тает.»"
    ))

    blocks.append(bulleted("🎬 Визуал", bold=True))
    blocks.append(bulleted("Вардгес сидит, серьёзный тон, камера на уровне глаз"))
    blocks.append(bulleted("Текст на экране — факты появляются один за другим как удары"))
    blocks.append(bulleted("Таймлайн: «2010 — интернет» → «2015 — соцсети» → «2025 — ИИ» → «2026 — ???»"))
    blocks.append(bulleted("Финал: часы, стрелка тикает, текст «Время тает»"))

    blocks.append(bulleted("🎵 Музыка/звук", bold=True))
    blocks.append(paragraph("Минималистичный, напряжённый бит. Тиканье часов на фоне. Финал — тишина + один удар."))

    blocks.append(bulleted("📱 CTA", bold=True))
    blocks.append(paragraph("«Ссылка в шапке профиля. Я готовлю кое-что, что поможет тебе внедрить ИИ быстро и без боли. Не пропусти.»"))

    blocks.append(bulleted("#️⃣ Хештеги", bold=True))
    blocks.append(paragraph("#будущеебизнеса #ИИилисмерть #автоматизация #малыйбизнес #нейросети2026 #GPTагенты #предпринимательство"))

    blocks.append(divider())

    # ===== ПОРЯДОК ПУБЛИКАЦИИ =====
    blocks.append(heading_2("📋 Порядок публикации (рекомендация)"))

    blocks.append(bulleted("Неделя 1: #3 (ошибки) → #5 (4 часа) — Проблема → решение. Привлечь внимание", bold=True))
    blocks.append(bulleted("Неделя 2: #1 (3 сотрудника) → #6 (без кода) — Провокация → снятие барьера", bold=True))
    blocks.append(bulleted("Неделя 3: #2 (КП за 2 мин) → #8 (кейс туризм) — Демонстрация → конкретный кейс", bold=True))
    blocks.append(bulleted("Неделя 4: #4 (24/7) → #7 (50 агентов) — Масштаб → детализация", bold=True))
    blocks.append(bulleted("Неделя 5: #9 (конкуренты) → #10 (через год) — Urgency → финальный прогрев перед запуском", bold=True))

    blocks.append(divider())

    # ===== СОВЕТЫ =====
    blocks.append(heading_2("💡 Общие советы по съёмке"))

    blocks.append(callout(
        "Свет: дневной или кольцевая лампа. Без тёмных углов\n"
        "Звук: петличный микрофон обязательно. Звук > картинка\n"
        "Длина: 30-60 секунд, не больше. Лучше 40-50\n"
        "Субтитры: ОБЯЗАТЕЛЬНО. 80% смотрят без звука\n"
        "Энергия: первые 2 секунды — максимальная. Потом можно чуть сбавить\n"
        "Повторы: не бойся перезаписывать. 3-5 дублей — норма\n"
        "Время публикации: 8:00-9:00 или 19:00-21:00 по Москве",
        emoji="🎥"
    ))

    return blocks


def main():
    print("Building blocks...")
    blocks = parse_and_build_blocks()
    print(f"Total blocks: {len(blocks)}")

    # Create page with first 100 blocks
    first_batch = blocks[:100]
    remaining = blocks[100:]

    page_data = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🎬"},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": PAGE_TITLE}}]
            }
        },
        "children": first_batch,
    }

    print("Creating page...")
    result = notion_request("POST", "pages", page_data)
    page_id = result["id"]
    page_url = result["url"]
    print(f"Page created: {page_url}")

    # Append remaining blocks in batches of 100
    batch_num = 1
    while remaining:
        batch = remaining[:100]
        remaining = remaining[100:]
        print(f"Appending batch {batch_num} ({len(batch)} blocks)...")
        notion_request("PATCH", f"blocks/{page_id}/children", {"children": batch})
        batch_num += 1

    print(f"\n✅ Done! Page URL: {page_url}")
    return page_url


if __name__ == "__main__":
    main()
