#!/bin/sh
#!/bin/zsh

if [ "$DATABASE" = "postgres" ]
then
    echo "Attempting to enter postgres database..."

    # Wait for the PostgreSQL database to be ready
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        echo "Waiting for postgres..."
    sleep 1
    done

    echo "PostgreSQL started"
fi

#create migration for toDo app
python manage.py makemigrations toDo
#create migration for users app
python manage.py makemigrations users
# python manage.py flush --no-input
python manage.py migrate

# Collect the static files
python manage.py collectstatic --noinput

exec "$@"