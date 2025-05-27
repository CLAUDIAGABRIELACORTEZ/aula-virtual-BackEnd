from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser
from students.models import Alumno
from core.models import Curso

class Command(BaseCommand):
    help = 'Poblando la base de datos con alumnos'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Número de alumnos a crear')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        faker = Faker()

        for _ in range(total):
            nombre = faker.first_name()
            apellido = faker.last_name()
            email = faker.unique.email()
            username = faker.unique.user_name()[:10]
            ci = str(faker.unique.random_number(digits=4, fix_len=True))
            telefono = faker.numerify(text='########')
            password = 'alumno123'
            curso = Curso.objects.get(nombre="1ro B")

            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                nombre=nombre,
                apellido=apellido,
                ci=ci,
                telefono=telefono,
                rol='alumno'
            )

            Alumno.objects.create(user=user, curso=curso)

        self.stdout.write(self.style.SUCCESS(f'{total} alumnos creados exitosamente.'))