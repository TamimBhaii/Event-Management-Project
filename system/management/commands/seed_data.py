from django.core.management.base import BaseCommand
from django.utils import timezone
from system.models import Category, Event, Participant
import random
from django.core.files.base import ContentFile, requests
# import requests

class Command(BaseCommand):
    help = 'Seed DB with categories, events and participants with images'

    def download_image(self, w=1200, h=600):
        url = f'https://picsum.photos/{w}/{h}'
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return ContentFile(r.content)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Image download failed: {e}'))
        return None

    def handle(self,*args,**options):
        self.stdout.write('Deleting old data...')
        Participant.objects.all().delete()
        Event.objects.all().delete()
        Category.objects.all().delete()

        cats = [
            ('Concert','Music & live shows'),
            ('Seminar','Informative talks'),
            ('Workshop','Hands-on sessions'),
            ('Sports','Competitive & fun'),
            ('Meetup','Community gatherings'),
            ('Tech','Hackathons & talks')
        ]
        cat_objs = []
        for name, desc in cats:
            c = Category.objects.create(name=name, description=desc)
            cat_objs.append(c)

        base = timezone.localdate()
        locations = ['City Hall','University Ground','Stadium','Community Center','Tech Park','Auditorium']

        events = []
        for i in range(35):
            cat = random.choice(cat_objs)
            d = base + timezone.timedelta(days=random.randint(-20,40))
            ev = Event.objects.create(
                name=f"{cat.name} Event #{i+1}",
                description=f"Sample {cat.name} event. Number {i+1}",
                date=d,
                time=timezone.now().time().replace(microsecond=0),
                location=random.choice(locations),
                category=cat
            )
            img = self.download_image(1200,600)
            if img:
                ev.banner.save(f'event_{i+1}.jpg', img, save=True)
            events.append(ev)

        for i in range(60):
            p = Participant.objects.create(
                name=f"Participant {i+1}",
                email=f"participant{i+1}@example.com"
            )
            avatar = self.download_image(400,400)
            if avatar:
                p.avatar.save(f'avatar_{i+1}.jpg', avatar, save=True)
            chosen = random.sample(events, k=random.randint(1,6))
            for ev in chosen:
                p.events.add(ev)

        self.stdout.write(self.style.SUCCESS('Seed complete: 35 events, 60 participants created.'))
