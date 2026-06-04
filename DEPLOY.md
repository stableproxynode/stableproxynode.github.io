# DEPLOY — публикация и обновление сайта

## ⭐ Основной хостинг — Timeweb S3 (российский, открывается из РФ)

**Адрес:** https://stableproxynode.s3.twcstorage.ru/index.html
Хранилище: S3-бакет `stableproxynode` (Timeweb Cloud, регион ru-1, 1 ₽/мес).

**Обновить сайт** (после правок в `index.html`):
```bash
cd "/Users/alex/Папка на компьютере/VS CODE"
TW_S3_KEY="ВАШ_ACCESS_KEY" TW_S3_SECRET="ВАШ_SECRET_KEY" python3 deploy-s3.py
```
Ключи S3 берутся в панели Timeweb → Объектное хранилище → бакет `stableproxynode`.
Скрипт `deploy-s3.py` подписывает запрос (AWS SigV4) и заливает `index.html`.
Изменения видны сразу.

> Чтобы получить «красивый» адрес `https://stableproxynode.ru` — нужно довести
> регистрацию домена `.ru` (оплата + паспортные данные регистранта), затем
> привязать домен к бакету в панели Timeweb. Сейчас домен в статусе
> `registration_fail`, поэтому используется прямой адрес хранилища.

---

## Зеркала

- **GitHub Pages (основной, открывается из России без VPN):** https://stableproxynode.github.io
  Репозиторий: `stableproxynode/stableproxynode.github.io`
- **surge.sh (зеркало, для заграницы / VPN):** https://stable-proxy-node.surge.sh

---

## Обновить GitHub Pages (основной)

После изменений в `index.html` из папки проекта:

```bash
cd "/Users/alex/Папка на компьютере/VS CODE"
git add -A && git commit -m "обновил ссылку прокси"
git push
```

Через ~1 минуту сайт обновится. Либо без терминала: на странице репозитория
**Add file → Upload files**, перетащить новый `index.html`, **Commit changes**.

> Примечание: одноразовый токен `proxy-deploy` после первой публикации нужно
> отозвать (https://github.com/settings/tokens). Для последующих `git push`
> GitHub попросит логин/пароль или новый токен.

---

## Обновить surge-зеркало (необязательно)

---

## Как переопубликовать после изменений

Из папки проекта выполни:

```bash
npx surge ./ stable-proxy-node.surge.sh
```

При первом запуске surge попросит **email и пароль** — это создаёт бесплатный
аккаунт (или входит в существующий). Дальше публикация занимает 2–3 секунды.

---

## Типичный сценарий: «прокси упал, нужно сменить ссылку»

1. Открой `index.html`.
2. В блоке `CONFIG` (в начале `<script>`) поменяй `proxyLink` на новую рабочую ссылку.
3. Сохрани файл.
4. Выполни `npx surge ./ stable-proxy-node.surge.sh`.
5. Через пару секунд новая ссылка уже на сайте — пользователям достаточно обновить страницу.

---

## Сменить адрес / поддомен

Замени `stable-proxy-node` на любой свободный поддомен:

```bash
npx surge ./ my-cool-proxy.surge.sh
```

Можно подключить и собственный домен — см. https://surge.sh/help/adding-a-custom-domain

---

## Альтернативные хостинги (если захочешь уйти с surge)

| Сервис | Команда / способ | Плюсы |
|--------|------------------|-------|
| **GitHub Pages** | запушить репозиторий, включить Pages | надёжно, привязка к GitHub |
| **Netlify** | `npx netlify deploy --prod` или drag-and-drop | удобная панель, формы |
| **Cloudflare Pages** | подключить репозиторий | быстрый CDN, защита |
| **Vercel** | `npx vercel --prod` | мгновенный деплой |

Сайт — статический (один `index.html`), поэтому подойдёт любой из них без изменений.
