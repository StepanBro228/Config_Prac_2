import sys, os

try:
    import tomllib
except Exception:
    print("Ошибка: нужен Python 3.11+ (модуль tomllib).", file=sys.stderr)
    sys.exit(2)

ORDER = [
    "package_name",
    "repo",
    "test_mode",
    "version",
    "output_image",
    "ascii_tree",
    "filter_substring",
]

def fail(msg: str) -> None:
    print(f"Ошибка: {msg}", file=sys.stderr)
    sys.exit(2)

def is_semver_like(s: str) -> bool:
    # X.Y или X.Y.Z, где X,Y,Z — целые числа; допускаем суффиксы через - или +
    # Примеры ок: "1.2", "1.2.3", "1.2.3-beta", "1.2+meta"
    core = s.split("-", 1)[0].split("+", 1)[0]
    parts = core.split(".")
    if len(parts) not in (2, 3):
        return False
    return all(p.isdigit() and p != "" for p in parts)

def main():
    path = "config.toml" if len(sys.argv) == 1 else sys.argv[1]
    if not os.path.exists(path):
        fail(f"конфигурационный файл не найден: {path}")

    # читаем файл
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        fail(f"ошибка разбора TOML: {e}")

    # секция [app]
    app = data.get("app")
    if not isinstance(app, dict):
        fail("отсутствует секция [app] в config.toml")

    # Проверки параметров
    # Строковые
    for key in ("package_name", "repo", "version", "output_image"):
        if key not in app:
            fail(f"отсутствует обязательный параметр '{key}'")
        if not isinstance(app[key], str):
            fail(f"параметр '{key}' должен быть строкой")
        if app[key].strip() == "":
            fail(f"параметр '{key}' не может быть пустой строкой")

    # Булевые
    for key in ("test_mode", "ascii_tree"):
        if key not in app:
            fail(f"отсутствует обязательный параметр '{key}'")
        if not isinstance(app[key], bool):
            fail(f"параметр '{key}' должен быть логическим (true/false)")

    # параметр filter_substring
    if "filter_substring" in app and not isinstance(app["filter_substring"], str):
        fail("параметр 'filter_substring' должен быть строкой (может быть пустой)")


    package_name = app["package_name"].strip()
    repo         = app["repo"].strip()
    version      = app["version"].strip()
    output_image = app["output_image"].strip()
    test_mode    = app["test_mode"]
    ascii_tree   = app["ascii_tree"]
    filter_substring = app.get("filter_substring", "").strip()

    # package_name: без табов/переводов строки
    if "\n" in package_name or "\t" in package_name or "\r" in package_name:
        fail("параметр 'package_name' не должен содержать управляющих символов")

    # version
    if not is_semver_like(version):
        fail("некорректная 'version' — ожидается формат X.Y или X.Y.Z (допустимы -suffix/+meta)")

    # output_image: .png или .svg
    olow = output_image.lower()
    if not (olow.endswith(".png") or olow.endswith(".svg")):
        fail("параметр 'output_image' должен оканчиваться на .png или .svg")

    # repo: если не http и test_mode=true — путь должен существовать
    if not (repo.lower().startswith("http://") or repo.lower().startswith("https://")):
        if test_mode and not os.path.exists(repo):
            fail("при test_mode=true параметр 'repo' должен быть существующим локальным путём")

    values = {
        "package_name": package_name,
        "repo": repo,
        "test_mode": test_mode,
        "version": version,
        "output_image": output_image,
        "ascii_tree": ascii_tree,
        "filter_substring": filter_substring,
    }
    for key in ORDER:
        val = values.get(key, "")
        if isinstance(val, bool):
            val = str(val).lower()
        print(f"{key}={val}")

if __name__ == "__main__":
    main()
