from django.conf import settings
from django.db import models

# Create your models here.
COLOR_CHOICES = [
    ('FF0000', 'Red'),
    ('FFA500', 'Orange'),
    ('00BFFF', 'Blue'),
    ('99FF00', 'Green'),
    ('003366', 'Indigo'),
]

class Miner(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название рига')
    description = models.CharField(max_length=255, verbose_name='Описание рига', blank=True)
    # rig_type = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     verbose_name='Владелец рига',
    # )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Владелец рига',
    )
    color = models.CharField(max_length=6, verbose_name='Цвет', blank=True)
    server = models.CharField(max_length=255, verbose_name='Сервер Пула', blank=True)
    miner_worker = models.CharField(max_length=255, verbose_name='Воркер', blank=True)
    bat = models.TextField(max_length=1000, verbose_name='Батник', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Риг"
        verbose_name_plural = "Риги"
        ordering = ("-created_at",)


class Stats(models.Model):
    miner = models.ForeignKey(
        Miner,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Риг',
    )
    datetime = models.DateTimeField(verbose_name='Дата создания')
    electricity = models.FloatField(verbose_name='Энергии сожрал', blank=True)
    speed = models.FloatField(verbose_name='Скорость в майнере', blank=True)
    power = models.IntegerField(verbose_name='Потребление ватт/час', blank=True)
    temperature = models.IntegerField(verbose_name='Температура', blank=True)
    memory_clock = models.IntegerField(verbose_name='Частота памяти', blank=True)
    core_clock = models.IntegerField(verbose_name='Частота ядра', blank=True)
    pool_speed = models.FloatField(verbose_name='Скорость на пуле', blank=True)
    server = models.CharField(max_length=255, verbose_name='Сервер пула', blank=True)
    shares_per_minute = models.FloatField(verbose_name='Решений в минуту', blank=True)
    accepted_shares = models.IntegerField(verbose_name='Принятые решения', blank=True)
    invalid_shares = models.IntegerField(verbose_name='Неправильные решения', blank=True)
    rejected_shares = models.IntegerField(verbose_name='Отклоненные решения', blank=True)
    stale_shares = models.IntegerField(verbose_name='Опаздавшие решения', blank=True)
    uptime = models.IntegerField(verbose_name='Аптайм', blank=True)
    miner_worker = models.CharField(max_length=255, verbose_name='Воркер', blank=True)

    def __str__(self):
        return f"{self.id} {self.miner.owner} {self.miner}"

    def get_owner(self):
        return self.miner.owner_id

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ("-id",)