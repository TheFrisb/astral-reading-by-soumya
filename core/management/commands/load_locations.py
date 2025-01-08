import csv

from django.core.management.base import BaseCommand

from core.models import Location


class Command(BaseCommand):
    help = "Load locations data from a tab-delimited text file into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the tab-delimited text file containing location data.",
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]

        try:
            with open(file_path, encoding="utf-8") as file:
                reader = csv.reader(file, delimiter="\t")
                locations = []
                batch_size = 100
                count = 0

                for row in reader:
                    if len(row) < 11:
                        self.stdout.write(
                            self.style.WARNING(f"Skipping invalid row: {row}")
                        )
                        continue

                    country_code = row[0]
                    postal_code = row[1]
                    town = row[2]
                    state_name = row[3]
                    latitude = row[9]
                    longitude = row[10]

                    string_repr = f"{town} {state_name} {postal_code} {country_code}"

                    locations.append(
                        Location(
                            country_code=country_code,
                            postal_code=postal_code,
                            town=town,
                            state_name=state_name,
                            latitude=float(latitude),
                            longitude=float(longitude),
                            full_address=string_repr,
                        )
                    )

                    if len(locations) >= batch_size:
                        Location.objects.bulk_create(locations)
                        count += len(locations)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully loaded {count} locations so far."
                            )
                        )
                        locations = []

                if locations:
                    Location.objects.bulk_create(locations)
                    count += len(locations)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Finished loading {count} locations into the database."
                    )
                )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
