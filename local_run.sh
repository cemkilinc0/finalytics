#!/usr/bin/env bash



#### TODO: fix this script to allow local builds as well ####



set -e  # Exit script on first error
set -o pipefail  # Exit script if any command in a pipeline fails

# Define paths and variables
VENV_PATH="venv"
ACTIVATE_SCRIPT_POSIX="$VENV_PATH/bin/activate"
ACTIVATE_SCRIPT_WIN="$VENV_PATH/Scripts/activate"
DEPENDENCIES=(
    django
    pre-commit
    mypy
    bandit
    black
    pylint
    types-requests
    python-decouple
    psycopg2
    requests
    django-extensions
    redis
    "celery[py-amqp,redis,auth,msgpack]"
    celery-redbeat
    django-celery-results
    django-celery-beat
    django-redis
    pyautogen
)

function main() {
    case "$1" in
        setup)
            create_venv
            activate_venv
            upgrade_pip
            install_dependencies
            install_type_stubs
            setup_pre_commit_hooks
            check_django_setup
            generate_requirements
            ;;
        run)
            activate_venv
            run_django_services
            ;;
        migrate)
            activate_venv
            migrate_django
            ;;
        *)
            echo "Usage: $0 {setup|run|migrate}"
            exit 1
            ;;
    esac
}

function create_venv() {
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
}

function activate_venv() {
    echo "Activating virtual environment..."
    if [[ -f "$ACTIVATE_SCRIPT_POSIX" ]]; then
        source "$ACTIVATE_SCRIPT_POSIX"
    elif [[ -f "$ACTIVATE_SCRIPT_WIN" ]]; then
        source "$ACTIVATE_SCRIPT_WIN"
    else
        echo "Error: Could not find the virtual environment activation script."
        exit 1
    fi
}

function upgrade_pip() {
    echo "Upgrading pip..."
    pip install --upgrade pip
}

function install_dependencies() {
    echo "Installing dependencies..."
    pip install "${DEPENDENCIES[@]}"
}

function install_type_stubs() {
    echo "Installing missing type stubs..."
    mypy --install-types --non-interactive
}

function setup_pre_commit_hooks() {
    echo "Setting up pre-commit hooks..."
    pre-commit install
}

function check_django_setup() {
    echo "Checking Django setup..."
    python manage.py check || { echo "Django check failed"; exit 1; }
}

function run_django_services() {
    echo "Launching Django services..."
    python manage.py runserver
}

function migrate_django() {
    echo "Migrating Django database..."
    python manage.py makemigrations
    python manage.py migrate
}

function generate_requirements() {
    echo "Generating requirements.txt..."
    pip freeze > requirements.txt
}

# Call the main function
main "$@"
