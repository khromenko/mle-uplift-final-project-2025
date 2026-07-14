# Проект 5-ого спринта - Uplift-моделирование (курс "ML-инженер с опытом" / Яндекс.Практикум)

Инструкция по запуску проекта

# Окружение

- Адрес репозитория GitHub
    - https://github.com/khromenko/mle-uplift-final-project-2025.git

- БД и S3-хранилище для логирования артефактов в MLflow - необходимо прописать в .env-файле
    - Персональная БД
        - host=rc1b-uh7kdmcx67eomesf.mdb.yandexcloud.net
        - port=6432
        - name=playground_mle_20260306_f5465b0629
        - user=mle_20260306_f5465b0629_freetrack
        - password=<...>
    - S3-хранилище 
        - MLFLOW_S3_ENDPOINT_URL=https://storage.yandexcloud.net
        - S3_BUCKET_NAME=/s3-student-mle-20260306-f5465b0629-freetrack/Sprint-5/Project
        - AWS_ACCESS_KEY_ID=YCAJE3Nlz8iDILW5VTYM1ihQB
        - AWS_SECRET_ACCESS_KEY=<...>


# Подготовка виртуальной машины

## Клонирование репозитория

Склонируйте репозиторий проекта:

```
git clone https://github.com/khromenko/mle-uplift-final-project-2025.git
```

## Настройка виртуального окружения

Рекомендации 
- используйте то же самое виртуальное окружение, что и созданное для работы с уроками
- если его не существует, то его следует создать
- для работы используйте `python3.10.13`. С другими версиями python могут возникнуть конфликты с библиотеками

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

### Создание нового виртуального окружения и его инициализировация
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

### Установить пакеты для MLflow (опциональная часть)

В проекте рекомендуется логировать результаты экспериментов в Mlflow, поэтому необходимо установить соответсвующие библиотеки

```bash
pip install -r requirements_mlflow.txt
```

# Запуск MLflow сервера

Для запуска MLflow сервера необходимо 
- проверить указание переменных окружения - см в .env-файле (по шаблону .env-template) -
    согласно описанию в [разделе "Окружение"](#Окружение)
- выполнить скрипт 

    ```bash
    bash run_mlflow_server_remote-db-s3.sh
    ```
- открыть web ui - адрес по-умолчанию (если не занят порт) - http://127.0.0.1:5000
- для остановки mlflow-server - остановить запущенный процесс в консоли (Ctrl+C) (или убить процессы gunicorn, если сессия потеряна)


# Полезный код

в `utils.py` лежит код, который может помочь вам при выполнении проекта
