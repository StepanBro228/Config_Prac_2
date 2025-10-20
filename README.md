# Задание 1 — Вариант 8 

Минимальный CLI-скрипт на Python 3.11+, который читает настройки из **TOML** и выводит их в формате `ключ=значение`. 

## Формат конфигурации (TOML)
Секция `[app]` и поля:
- **package_name** *(string, обязательный)* — имя пакета; без управляющих символов.
- **repo** *(string, обязательный)* — URL (`http/https`) или локальный путь.
- **test_mode** *(bool, обязательный)* — режим работы с тестовым репо.
- **version** *(string, обязательный)* — формат `X.Y` или `X.Y.Z` (допускаются `-suffix` / `+meta`).
- **output_image** *(string, обязательный)* — имя файла изображения (`.png` или `.svg`).
- **ascii_tree** *(bool, обязательный)* — флаг вывода ASCII-дерева.
- **filter_substring** *(string, необязательный)* — подстрока для фильтра (может быть пустой).

**Пример `config.toml`:**
```toml
[app]
package_name = "openssl"
repo = "https://git.alpinelinux.org/aports"
test_mode = false
version = "1.1.1"
output_image = "deps.svg"
ascii_tree = true
filter_substring = "test"
```

---

## Вывод
Скрипт печатает **ровно 7 строк** в фиксированном порядке:
```
package_name=...
repo=...
test_mode=true|false
version=...
output_image=...
ascii_tree=true|false
filter_substring=...
```

---
