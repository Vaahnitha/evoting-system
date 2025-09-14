# Generated manually for adding image field to Candidate model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='candidates/'),
        ),
    ]
