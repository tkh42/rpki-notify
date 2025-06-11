# myapp/management/commands/load_mock_data.py
from django.core.management.base import BaseCommand
from backend.models import Inconsistency, Error, Reachability

class Command(BaseCommand):
    help = 'Load mock data into the database'

    def handle(self, *args, **kwargs):
        Inconsistency.objects.bulk_create([
            Inconsistency(detail="Mismatch in record 1"),
            Inconsistency(detail="Unexpected null in column A"),
        ])
        Error.objects.bulk_create([
            Error(message="Failed to connect to service X"),
            Error(message="Index out of range in module Y"),
        ])
        Reachability.objects.bulk_create([
            Reachability(status="Node A is reachable"),
            Reachability(status="Node B is unreachable"),
        ])
        self.stdout.write(self.style.SUCCESS('Mock data loaded.'))
