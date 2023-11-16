from typing import Optional
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
import structlog

logger = structlog.get_logger()


class Repository:
    @staticmethod
    def create_record(model_class, **kwargs) -> Optional[models.Model]:
        log = logger.bind(model_class=model_class.__name__, action="create_record", data=kwargs)
        log.info("Creating record")
        try:
            record = model_class.objects.create(**kwargs)
            log.info("Record created", record_id=record.id)
            return record
        except Exception as e:
            log.exception("Failed to create record")
        return None

    @staticmethod
    def update_or_create_record(model_class, defaults=None, **kwargs) -> Optional[models.Model]:
        log = logger.bind(
            model_class=model_class.__name__, action="update_or_create_record", data=kwargs, defaults=defaults
        )
        log.info("Updating or creating record")
        defaults = defaults or {}
        try:
            record, created = model_class.objects.update_or_create(defaults=defaults, **kwargs)
            action = "Record created" if created else "Record updated"
            log.info(action, record_id=record.id)
            return record
        except Exception as e:
            log.exception("Failed to update or create record")
        return None

    @staticmethod
    def get_or_create_record(model_class, defaults=None, **kwargs) -> Optional[models.Model]:
        log = logger.bind(
            model_class=model_class.__name__, action="get_or_create_record", data=kwargs, defaults=defaults
        )
        log.info("Getting or creating record")
        defaults = defaults or {}
        try:
            record, created = model_class.objects.get_or_create(defaults=defaults, **kwargs)
            action = "Record created" if created else "Record found"
            log.info(action, record_id=record.id)
            return record
        except Exception as e:
            log.exception("Failed to get or create record")
            return None

    @staticmethod
    def get_record(model_class, **kwargs) -> Optional[models.Model]:
        log = logger.bind(model_class=model_class.__name__, action="get_record", data=kwargs)
        log.info("Getting record")
        try:
            record = model_class.objects.get(**kwargs)
            log.info("Record found", record_id=record.id)
            return record
        except ObjectDoesNotExist as e:
            log.error("Failed to get record")
        except MultipleObjectsReturned as e:
            log.error("Multiple records found")
        except Exception as e:
            log.exception("An unexpected error occurred while getting record")
        return None

    @staticmethod
    def update_record(model_class, record_id: int, **kwargs) -> Optional[models.Model]:
        log = logger.bind(model_class=model_class.__name__, action="update_record", record_id=record_id, data=kwargs)
        log.info("Updating record")
        try:
            record = model_class.objects.get(id=record_id)
            for attr, value in kwargs.items():
                setattr(record, attr, value)
            record.save()
            log.info("Record updated", record_id=record.id)
            return record
        except ObjectDoesNotExist as e:
            log.exception("Failed to update record")
        except Exception as e:
            log.exception("An unexpected error occurred while updating record")
        return None

    @staticmethod
    def delete_record(model_class, record_id: int) -> bool:
        log = logger.bind(model_class=model_class.__name__, action="delete_record", record_id=record_id)
        log.info("Deleting record")
        try:
            model_class.objects.filter(id=record_id).delete()
            log.info("Record deleted", record_id=record_id)
            return True
        except Exception as e:
            log.exception("Failed to delete record")
        return False

    @staticmethod
    def filter_records(model_class, **kwargs) -> models.QuerySet:
        log = logger.bind(model_class=model_class.__name__, action="filter_records", data=kwargs)
        log.info("Filtering records")
        try:
            records = model_class.objects.filter(**kwargs)
            log.info("Records found", record_count=len(records))
            return records
        except Exception as e:
            log.exception("Failed to filter records")
        return models.QuerySet(model_class)  # Return empty queryset

    @staticmethod
    def bulk_create_records(model_class, records_data_list):
        log = logger.bind(
            model_class=model_class.__name__, action="bulk_create_records", record_count=len(records_data_list)
        )
        log.info("Bulk creating records")
        try:
            records = model_class.objects.bulk_create([model_class(**data) for data in records_data_list])
            log.info(f"{len(records)} records created")
            return records
        except Exception as e:
            log.exception("Failed to bulk create records")
            return None

    @staticmethod
    def bulk_update_records(model_class, records, update_fields):
        log = logger.bind(model_class=model_class.__name__, action="bulk_update_records", update_fields=update_fields)
        log.info("Bulk updating records")
        try:
            model_class.objects.bulk_update(records, update_fields)
            log.info("Records updated")
            return True
        except Exception as e:
            log.exception("Failed to bulk update records")
            return False

    @staticmethod
    def get_all_records(model_class):
        log = logger.bind(model_class=model_class.__name__, action="get_all_records")
        log.info("Retrieving all records")
        try:
            records = model_class.objects.all()
            log.info(f"{len(records)} records found")
            return records
        except Exception as e:
            log.exception("Failed to retrieve all records")
            return None
