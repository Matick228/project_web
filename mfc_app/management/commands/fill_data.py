from django.core.management.base import BaseCommand
from mfc_app.models import Category, Service, Branch, News, Status, User, ServiceStatistic, Appointment
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Fill database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to fill database with sample data...')


        categories_data = [
            'Паспортные услуги',
            'Регистрационные услуги',
            'Налоговые услуги',
            'Социальные услуги',
            'Юридические услуги',
            'Транспортные услуги',
            'Недвижимость',
            'Бизнес',
            'Семья и дети',
            'Образование'
        ]

        categories = []
        for name in categories_data:
            cat, created = Category.objects.get_or_create(name=name)
            categories.append(cat)
            self.stdout.write(f'Created category: {name}')



        statuses_data = [
            {'name': 'Ожидание', 'description': 'Заявка ожидает обработки'},
            {'name': 'Подтверждено', 'description': 'Заявка подтверждена'},
            {'name': 'Выполнено', 'description': 'Услуга оказана'},
            {'name': 'Отменено', 'description': 'Заявка отменена'}
        ]

        statuses = []
        for data in statuses_data:
            status, created = Status.objects.get_or_create(
                name=data['name']
            )
            statuses.append(status)
            self.stdout.write(f'Created status: {data["name"]}')


        services_data = [
            {'name': 'Замена паспорта РФ', 'category': 0, 'duty': 300,
             'desc': 'Замена паспорта РФ при достижении 20 и 45 лет'},
            {'name': 'Выдача загранпаспорта', 'category': 0, 'duty': 5000,
             'desc': 'Оформление заграничного паспорта старого и нового образца'},
            {'name': 'Регистрация по месту жительства', 'category': 1, 'duty': 0,
             'desc': 'Постоянная регистрация по месту жительства'},
            {'name': 'Регистрация брака', 'category': 8, 'duty': 350, 'desc': 'Государственная регистрация брака'},
            {'name': 'Получение ИНН', 'category': 2, 'duty': 0,
             'desc': 'Получение идентификационного номера налогоплательщика'},
            {'name': 'Регистрация ИП', 'category': 7, 'duty': 800,
             'desc': 'Государственная регистрация индивидуального предпринимателя'},
            {'name': 'Получение справки о несудимости', 'category': 4, 'duty': 1000,
             'desc': 'Выдача справки об отсутствии судимости'},
            {'name': 'Обмен водительского удостоверения', 'category': 5, 'duty': 2000,
             'desc': 'Замена водительского удостоверения'},
            {'name': 'Регистрация автомобиля', 'category': 5, 'duty': 2000,
             'desc': 'Постановка автомобиля на учет в ГИБДД'},
            {'name': 'Получение материнского капитала', 'category': 3, 'duty': 0,
             'desc': 'Оформление сертификата на материнский капитал'},
            {'name': 'Оформление пенсии', 'category': 3, 'duty': 0, 'desc': 'Назначение и оформление пенсии'},
            {'name': 'Получение свидетельства о рождении', 'category': 8, 'duty': 0,
             'desc': 'Государственная регистрация рождения'},
            {'name': 'Оформление инвалидности', 'category': 3, 'duty': 0, 'desc': 'Медико-социальная экспертиза'},
            {'name': 'Получение льгот', 'category': 3, 'duty': 0, 'desc': 'Оформление социальных льгот'},
            {'name': 'Регистрация права собственности', 'category': 6, 'duty': 2000,
             'desc': 'Государственная регистрация права на недвижимость'},
        ]

        services = []
        for data in services_data:
            service, created = Service.objects.get_or_create(
                name=data['name'],
                defaults={
                    'category': categories[data['category']],
                    'state_duty': data['duty'],
                    'description': data['desc']
                }
            )
            services.append(service)
            self.stdout.write(f'Created service: {data["name"]}')


        branches_data = [
            {'name': 'МФЦ Центральный', 'address': 'ул. Ленина, 1', 'phone': '+79161234567',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Северный', 'address': 'пр. Мира, 25', 'phone': '+79161234568',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Южный', 'address': 'ул. Садовая, 15', 'phone': '+79161234569',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Западный', 'address': 'ул. Победы, 10', 'phone': '+79161234570',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Восточный', 'address': 'пр. Строителей, 5', 'phone': '+79161234571',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Центр-2', 'address': 'ул. Советская, 33', 'phone': '+79161234572',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Приморский', 'address': 'наб. Речная, 8', 'phone': '+79161234573',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Горный', 'address': 'ул. Горная, 12', 'phone': '+79161234574',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Парковый', 'address': 'ул. Парковая, 7', 'phone': '+79161234575',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Студенческий', 'address': 'пр. Студенческий, 20', 'phone': '+79161234576',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Торговый', 'address': 'ул. Торговая, 45', 'phone': '+79161234577',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
            {'name': 'МФЦ Заречный', 'address': 'ул. Заречная, 3', 'phone': '+79161234578',
             'hours': '09:00-18:00 (Пн-Пт), 10:00-16:00 (Сб)'},
        ]

        branches = []
        for data in branches_data:
            branch, created = Branch.objects.get_or_create(
                name=data['name'],
                defaults={
                    'address': data['address'],
                    'phone': data['phone'],
                    'work_hours': data['hours']
                }
            )
            branches.append(branch)
            self.stdout.write(f'Created branch: {data["name"]}')


        news_data = [
            {'title': 'Открытие нового филиала МФЦ',
             'content': 'Сообщаем об открытии нового современного филиала МФЦ в центре города. Новый филиал оснащен современным оборудованием и предлагает расширенный перечень услуг.'},
            {'title': 'Упрощена процедура получения паспорта',
             'content': 'С 1 января 2024 года упрощена процедура получения и замены паспорта РФ. Теперь для подачи заявления требуется меньше документов.'},
            {'title': 'Электронная запись на услуги',
             'content': 'Теперь вы можете записаться на любую услугу через личный кабинет на нашем портале. Это сэкономит ваше время и позволит избежать очередей.'},
            {'title': 'Новые услуги в МФЦ',
             'content': 'Добавлены 5 новых государственных услуг, доступных во всех филиалах. Список услуг постоянно расширяется для вашего удобства.'},
            {'title': 'Изменение графика работы',
             'content': 'Обратите внимание на изменение графика работы филиалов в праздничные дни. Актуальное расписание доступно на сайте.'},
            {'title': 'Мобильное приложение МФЦ',
             'content': 'Теперь все услуги доступны в мобильном приложении. Скачайте приложение в App Store или Google Play.'},
            {'title': 'Бесплатные консультации',
             'content': 'Всем гражданам предоставляются бесплатные консультации по вопросам получения государственных услуг.'},
            {'title': 'Обновление системы онлайн-записи',
             'content': 'Проведено обновление системы онлайн-записи. Теперь система работает быстрее и стабильнее.'},
            {'title': 'Скидки для пенсионеров',
             'content': 'Введены скидки на государственные пошлины для пенсионеров при обращении в МФЦ.'},
            {'title': 'Расширение перечня электронных услуг',
             'content': 'Добавлено 15 новых электронных услуг, которые можно получить не выходя из дома.'},
        ]

        for i, data in enumerate(news_data):
            news, created = News.objects.get_or_create(
                title=data['title'],
                defaults={
                    'content': data['content'],
                }
            )
            self.stdout.write(f'Created news: {data["title"]}')


        try:
            user, created = User.objects.get_or_create(
                email='test@example.com',
                defaults={
                    'username': 'testuser',
                    'first_name': 'Иван',
                    'last_name': 'Петров',
                    'phone': '+79160000000',
                    'password': make_password('testpassword123')
                }
            )
            if created:
                self.stdout.write('Created test user: test@example.com')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))


        for service in services:
            stat, created = ServiceStatistic.objects.get_or_create(
                service=service,
                defaults={
                    'view_count': random.randint(50, 500),
                    'appointment_count': random.randint(5, 50)
                }
            )

        self.stdout.write('Created service statistics')


        for i in range(20):
            appointment, created = Appointment.objects.get_or_create(
                user=user,
                service=random.choice(services),
                branch=random.choice(branches),
                status=random.choice(statuses),
                desired_date=date.today() + timedelta(days=random.randint(1, 30)),
                desired_time=f"{random.randint(9, 17)}:00:00"
            )

        self.stdout.write('Created sample appointments')

        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )