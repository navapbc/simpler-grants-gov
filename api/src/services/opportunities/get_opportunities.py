from sqlalchemy import select

import src.adapters.db as db
from src.api.route_utils import raise_flask_error
from src.db.models.opportunity_models import Opportunity


def get_opportunity(db_session: db.Session, opportunity_id: int) -> Opportunity:
    # For now, only non-drafts can be fetched
    opportunity: Opportunity | None = db_session.execute(
        select(Opportunity)
        .where(Opportunity.opportunity_id == opportunity_id)
        .where(Opportunity.is_draft.is_(False))
    ).scalar_one_or_none()

    if opportunity is None:
        raise_flask_error(404, message=f"Could not find Opportunity with ID {opportunity_id}")

    return opportunity
