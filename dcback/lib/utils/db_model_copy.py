



product2_fields = {
    field.name
    for field in LoginStatistic2._meta.fields
    if field.name != "id"
}

rows = []

for p in LoginStatistic.objects.all():
    data = {
        field: getattr(p, field)
        for field in product2_fields
        if hasattr(p, field)
    }

    rows.append(LoginStatistic2(**data))

LoginStatistic2.objects.bulk_create(rows)