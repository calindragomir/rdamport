from models import Employee

def generate_employee_records():
    """
    Generates employee content
    """
    e = Employee.objects.get_or_create(first_name='Mike' ,last_name='Jones', bank_account='6483627463912', is_supervisor=True)
    e = Employee.objects.get_or_create(first_name='Johnny' ,last_name='Costello', bank_account='88837463912', is_supervisor=False)
    e = Employee.objects.get_or_create(first_name='David' ,last_name='York', bank_account='1253627463912', is_supervisor=False)
    e = Employee.objects.get_or_create(first_name='Cathy' ,last_name='Levine', bank_account='1253876463912', is_supervisor=False)
    e = Employee.objects.get_or_create(first_name='Mary' ,last_name='Posky', bank_account='1253876463912', is_supervisor=False)
    e = Employee.objects.get_or_create(first_name='Victor' ,last_name='Nemeski', bank_account='875675453912', is_supervisor=True)
    e = Employee.objects.get_or_create(first_name='Ivan' ,last_name='Karpov', bank_account='435675453912', is_supervisor=False)
    e = Employee.objects.get_or_create(first_name='Christian' ,last_name='Leroy', bank_account='132455453912', is_supervisor=False)
