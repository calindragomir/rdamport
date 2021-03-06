import string
import random

def random_id_generator(length):
    """
    Generates a random id of specified length
    Uses ASCII uppercase caracthers and digits
    """

    population = string.ascii_uppercase + string.digits
    size = int(length)

    random_id = ('').join(random.sample(population, size))

    return random_id

def check_if_id_exists(id, model, pk_name='pk'):
    """
    Checks if a given id already exists as a primary key value of a model
    """
    records = model.objects.all()
    for record in records:
        try:
            if getattr(record, pk_name) == id:
                return True
        except AttributeError:
            raise Exception('Specified primary key field does not exist')

    return False

def get_unique_id(length, model, primary_key_name):
    """
    Returns an unique id of the specified length
    Ensures that the returned id is not already a primary key in the model
    """
    ATTEMPTS = 10

    while ATTEMPTS:
        unique_id = random_id_generator(length)
        id_already_exists = check_if_id_exists(unique_id, model, primary_key_name)

        if not id_already_exists:
            break

        ATTEMPTS -= 1

    if ATTEMPTS == 0:
        raise Exception('Could not generate an unique number \
        from {attempts_no} attempts'.format(attempts_no=ATTEMPTS))

    return unique_id

def get_available_elements(model, attribute, related_model=None):
    """
    Returns elements that do not have a specific attribute set.
    If the checked attribute is a related model, that model has to be
    specified as an argument
    """

    model_instances = model.objects.all()
    available_elements = []

    # Retrieve elements that don't have the specified attribute
    for element in model_instances:
        if related_model:
            try:
                item = getattr(element, attribute)
            except related_model.DoesNotExist:
                available_elements.append(element)
        else:
            if not getattr(element, attribute):
                available_elements.append(element)

    return available_elements

def get_connected_elements(origin_model, attribute, destination_instance):
    """
    Returns all elements from origin model connected to the
    destination model through a specified attribute
    """

    model_instances = origin_model.objects.all()
    connected_elements = []

    # Retrieve elements that don't have the specified attribute
    for element in model_instances:
        refered_instance = getattr(element, attribute)
        if refered_instance == destination_instance:
            connected_elements.append(element)

    return connected_elements
