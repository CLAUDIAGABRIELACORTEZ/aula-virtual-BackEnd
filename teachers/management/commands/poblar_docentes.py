from django.core.management import BaseCommand
from faker import Faker
from accounts.models import CustomUser
from teachers.models import Docente

#instale la libreria Faker
class Command(BaseCommand):
    help = 'Poblando la base de datos con docentes'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Número de docentes a crear')
    
    def handle(self, *args, **kwargs):
        total = kwargs['total']
        faker = Faker()

        for _ in range(total):
            nombre = faker.first_name()
            apellido = faker.last_name()
            email = faker.unique.email()
            username = faker.unique.user_name()
            ci = faker.unique.random_number(digits=4, fix_len=True)
            telefono = faker.numerify(text='########')
            password = 'docente123'

            user = CustomUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                nombre=nombre,
                apellido=apellido,
                ci=str(ci),
                telefono=telefono,
                rol='docente'
            )

            Docente.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS(f'{total} docentes creado exitosamente.'))
