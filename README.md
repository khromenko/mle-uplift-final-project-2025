# Подготовка виртуальной машины

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/khromenko/mle-uplift-final-project-2025.git
```

## Активируйте виртуальное окружение

Используйте то же самое виртуальное окружение, что и созданное для работы с уроками. Если его не существует, то его следует создать. Для работы используйте `python3.10.13`. С другими версиями python могут возникнуть конфликты с библиотеками

---
[Выполнение требования по версии Python]
### Установка версии python 3.10.13
Так как текущая версия на ВМ python3.10.12, не соответсвует требуемой 3.10.13, необходимо установить новую версию.

Чтобы не конфликтовать и не испортить ничего в системных настройках python на ВМ, выполним установку версии 3.10.13 через утилиту pyenv.

Инструкция по работе с pyenv, установке и управления версиями тут - https://xtool.ru/v/python-update/#main.

Ниже приведено выполнение необходимых инструкций на ВМ.
Команды выполняются из рабочей директории проекта - `~/mle_projects/sprint-5/mle-uplift-final-project-2025`
1. установка pyenv

    ```bash
    # Установка зависимостей для сборки Python (Ubuntu/Debian)
    sudo apt update
    sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl

    # Установка pyenv
    curl https://pyenv.run | bash

    # Добавление pyenv в PATH (в ~/.bashrc или ~/.zshrc)
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc
    ```
2. установка версии 3.10.13

    ```bash
    pyenv install 3.10.13
    # Installed Python-3.10.13 to /home/mle-user/.pyenv/versions/3.10.13
    python --versions
    # Python 3.10.13
    ```
3. применение версии 3.10.13 локально для текущей директории проекта

    ```bash
    pyenv local 3.10.13
    ```

теперь можно вернуться к установке venv для проекта

---

Создать новое виртуальное окружение и инициализировать его
```bash
python -m venv .venv_mle-uplift-final-project-2025
. .venv_mle-uplift-final-project-2025/bin/activate
```
Установить в него необходимые зависимости (python-пакеты)

Чтобы исправить конфликты при установке, версии библиотек были актуализированы под версии, которые определены для 5-ого Спринта (Uplift-моделирование) согласно файлу зависимостей 
- https://code.s3.yandex.net/landings-v2-machine-learning/Files/requirements.txt

```bash
pip install -r requirements.txt
```

TODO - нужна ли кастомизированная под Яндекс.Практикум версия scikit-uplift, которая была локально использована в 5-м Спринте? 
- попробуем сначала обойтись штатной версией ..

# Полезный код

в `utils.py` лежит код, который может помочь вам при выполнении проекта
