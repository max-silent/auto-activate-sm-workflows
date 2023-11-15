import logging

log = logging.getLogger(__name__)


class ActivateInventoryPartMap:
    def __init__(self):
        log.info("Initialize subscription part mapping class")

    @staticmethod
    def activate_inventory_part_map(device_type, device_model=None):
        if device_type == "IAP":
            part_number = "JW242AR"
            return part_number
        if device_type == "SWITCH":
            part_number = "JL255A"
            return part_number
        if device_type == "GATEWAY":
            part_number = "7005-RW"
            return part_number
