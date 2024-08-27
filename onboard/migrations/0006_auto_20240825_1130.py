# Generated by Django 3.1.6 on 2024-08-25 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboard', '0005_auto_20240821_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessdetails',
            name='userIdFile',
            field=models.FileField(blank=True, null=True, upload_to='user-id-file'),
        ),
        migrations.AlterField(
            model_name='businessdetails',
            name='certOfCorporation',
            field=models.FileField(blank=True, null=True, upload_to='cert-of-corporation'),
        ),
        migrations.AlterField(
            model_name='businessdetails',
            name='commenceBusinessCert',
            field=models.FileField(blank=True, null=True, upload_to='commence-business-certs'),
        ),
        migrations.AlterField(
            model_name='businessdetails',
            name='companyProfileCert',
            field=models.FileField(blank=True, null=True, upload_to='company-profile-certs'),
        ),
        migrations.AlterField(
            model_name='directorids',
            name='directorIds',
            field=models.FileField(blank=True, null=True, upload_to='directors-certs'),
        ),
    ]
