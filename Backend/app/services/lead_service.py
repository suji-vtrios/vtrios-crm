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
            Lead.phone == phone
        )

        .order_by(
            Lead.id.desc()
        )

        .first()
    )

def create_lead(
    db,
    name,
    phone,
    source="WhatsApp"
):

    lead = Lead(

        name=name,

        phone=phone,

        source=source,

        status="New"
    )

    db.add(lead)

    db.commit()

    db.refresh(lead)

    return lead