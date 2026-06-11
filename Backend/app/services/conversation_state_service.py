STAGES = [
    "GREETING",
    "DISCOVERY",
    "ASSESSMENT",
    "RECOMMENDATION",
    "OBJECTION",
    "ENROLLMENT",
    "FOLLOWUP",
    "CLOSED"
]


def move_to_stage(
    db,
    session,
    stage
):

    if stage not in STAGES:
        raise ValueError(
            f"Invalid stage: {stage}"
        )

    session.current_stage = stage

    db.commit()

    db.refresh(session)

    return session


def get_stage(
    session
):

    return session.current_stage