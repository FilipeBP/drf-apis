from clients.exceptions import AddressConflitError, AddressNotFound


def remove_secondary_addresses_from_client(client, addresses_ids):
    missing_ids = get_missing_ids(client, addresses_ids)

    if missing_ids:
        raise AddressNotFound(addresses_ids)

    client.secondary_addresses.remove(*addresses_ids)
    client.save()


def get_missing_ids(client, addresses_ids):
    existing_ids = client.secondary_addresses.filter(id__in=addresses_ids).values_list('id', flat=True)
    existing_ids = list(existing_ids)
    return list(set(existing_ids) ^ set(addresses_ids))


def add_secondary_addresses_to_client(client, addresses_ids):
    if client.main_address_id in addresses_ids:
        raise AddressConflitError()

    client.secondary_addresses.add(*addresses_ids)
    client.save()


def set_main_address_to_client(client, address_id):
    if client.secondary_addresses.filter(id=address_id).exists():
        client.secondary_addresses.remove(address_id)

    client.main_address_id = address_id
    client.save()
