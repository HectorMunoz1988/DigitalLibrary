import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command


class Command(BaseCommand):
    help = "Prepara los datos iniciales de producción."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if username and email and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Superusuario '{username}' creado correctamente."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"El superusuario '{username}' ya existe."
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "No se han definido las variables del superusuario."
                )
            )

        if not User.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No hay usuarios en la base de datos."
                )
            )

        call_command("loaddata", "library_data")

        self.stdout.write(
            self.style.SUCCESS(
                "Datos iniciales cargados correctamente."
            )
        )