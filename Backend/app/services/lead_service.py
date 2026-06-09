from app.models.lead import Lead


def get_lead_by_phone(
    db,
    phone
):

    return (

        db.query(
            Lead
        )

        .filter(
            Lead.phone
            == phone
        )

        .first()
    )