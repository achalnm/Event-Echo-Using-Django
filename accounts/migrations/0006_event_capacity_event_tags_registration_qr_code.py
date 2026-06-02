from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_event_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='capacity',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='registration',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
    ]
