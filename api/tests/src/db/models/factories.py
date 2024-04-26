"""Factories for generating test data.

These factories are used to generate test data for the tests. They are
used both for generating in memory objects and for generating objects
that are persisted to the database.

The factories are based on the `factory_boy` library. See
https://factoryboy.readthedocs.io/en/latest/ for more information.
"""
import random
from datetime import datetime
from typing import Optional

import factory
import factory.fuzzy
import faker
from faker.providers import BaseProvider
from sqlalchemy.orm import scoped_session

import src.adapters.db as db
import src.db.models.opportunity_models as opportunity_models
import src.db.models.staging as staging
import src.db.models.transfer.topportunity_models as transfer_topportunity_models
import src.util.datetime_util as datetime_util
from src.constants.lookup_constants import (
    ApplicantType,
    FundingCategory,
    FundingInstrument,
    OpportunityCategory,
    OpportunityCategoryLegacy,
    OpportunityStatus,
)


def sometimes_none(factory_value, none_chance: float = 0.5):
    if random.random() > none_chance:
        return factory_value

    return None


class CustomProvider(BaseProvider):
    """
    This class is a custom faker provider that can be used to generate
    fake data for our specific scenarios.

    The name of the functions defined in this class is the name of the individual provider.
    For example, the "agency" method below can be called by doing either of the following::

        fake.agency()

        factory.Faker("agency")

    Below we register this provider class with both the faker instance we setup, as well as
    the underlying one backing the factory's faker instance.

    See: https://faker.readthedocs.io/en/master/#how-to-create-a-provider
    """

    # Ideally use agencies here that actually exist so anyone
    # using data generated by this for front-end dev actually
    # has valid values
    AGENCIES = ["USAID", "ARPAH", "DOC", "DOC-EDA"]

    # Various words we can use when building the agency names
    # Stuff that sounds like it might be an agency, even if its not exactly the name
    AGENCY_WORDS = [
        "Agriculture",
        "Commerce",
        "Defense",
        "Education",
        "Economics",
        "Energy",
        "Health",
        "Housing",
        "Justice",
        "Labor",
        "State",
        "Interior",
        "Transportation",
        "Science",
        "Arts",
    ]

    AGENCY_NAME_FORMATS = [
        "Department of {{agency_word}}",
        "Department of the {{agency_word}}",
        "Agency for {{agency_word}}",
        "National {{agency_word}} Administration",
    ]

    AGENCY_CONTACT_DESC_FORMATS = [
        "{{name}}\n{{job}}\n555-###-####\n{{email}}",
        "{{relevant_url}} Contact Center\nHours of operation are 24 hours a day, 7 days a week.\n{{email}}",
        "{{agency}} Webmaster\n{{email}}",
    ]

    # Rather than generate any random URL in our data, use those
    # that are vaguely relevant to avoid linking to anything outside
    # of the grants ecosystem that could cause confusion in test data
    # (ie. either a website we work with, or a very generic one)
    RELEVANT_URLS = ["google.com", "grants.gov", "simpler.grants.gov", "sam.gov"]

    ADDITIONAL_INFO_DESC_FORMATS = [
        "Full Announcement",
        "Grants.gov",
        "Link to grant on {{relevant_url}}",
        "Program Announcement",
        "Click on the link to see the full announcement.",
        "Division of {{company}}",
    ]

    # Opportunity title uses several other existing providers
    # to generate titles. Anything in {{ }} is calling a provider
    # with that name.
    OPPORTUNITY_TITLE_FORMATS = [
        "Research into {{job}} industry",
        "Embassy program for {{job}} in {{country}}",
        "{{name}} Foundation Grant for {{bs}}",
        "{{company}} {{year}} award",
    ]

    SUMMARY_DESCRIPTION_FORMATS = [
        "{{agency}} is looking to further investigate this topic. {{paragraph}}",
        "<p>{{paragraph}}</p><p><br></p><p>{{paragraph}}</p>",
        "The purpose of this Notice of Funding Opportunity (NOFO) is to support research into {{job}} and how we might {{catch_phrase}}.",
    ]

    # In the formatting, ? becomes a random letter, # becomes a random digit
    OPPORTUNITY_NUMBER_FORMATS = [
        "???-###-FY{{year}}-###",
        "{{agency}}-##-###",
        "???#######",
        "??-##-???-###",
        "{{word}}-###-##",
    ]

    def agency(self) -> str:
        return self.random_element(self.AGENCIES)

    def agency_word(self) -> str:
        return self.random_element(self.AGENCY_WORDS)

    def agency_name(self) -> str:
        pattern = self.random_element(self.AGENCY_NAME_FORMATS)
        return self.generator.parse(pattern)

    def agency_contact_description(self) -> str:
        # bothify turns any ? into letters, and # into digits
        pattern = self.bothify(self.random_element(self.AGENCY_CONTACT_DESC_FORMATS))
        return self.generator.parse(pattern)

    def relevant_url(self):
        return self.random_element(self.RELEVANT_URLS)

    def additional_info_desc(self):
        pattern = self.random_element(self.ADDITIONAL_INFO_DESC_FORMATS)
        return self.generator.parse(pattern)

    def opportunity_number(self) -> str:
        # bothify turns any ? into letters, and # into digits
        pattern = self.bothify(self.random_element(self.OPPORTUNITY_NUMBER_FORMATS))
        return self.generator.parse(pattern).upper()

    def opportunity_title(self) -> str:
        pattern = self.random_element(self.OPPORTUNITY_TITLE_FORMATS)
        return self.generator.parse(pattern)

    def summary_description(self) -> str:
        pattern = self.random_element(self.SUMMARY_DESCRIPTION_FORMATS)
        return self.generator.parse(pattern)


fake = faker.Faker()
fake.add_provider(CustomProvider)
factory.Faker.add_provider(CustomProvider)

_db_session: Optional[db.Session] = None


def get_db_session() -> db.Session:
    # _db_session is only set in the pytest fixture `enable_factory_create`
    # so that tests do not unintentionally write to the database.
    if _db_session is None:
        raise Exception(
            """Factory db_session is not initialized.

            If your tests don't need to cover database behavior, consider
            calling the `build()` method instead of `create()` on the factory to
            not persist the generated model.

            If running tests that actually need data in the DB, pull in the
            `enable_factory_create` fixture to initialize the db_session.
            """
        )

    return _db_session


# The scopefunc ensures that the session gets cleaned up after each test
# it implicitly calls `remove()` on the session.
# see https://docs.sqlalchemy.org/en/20/orm/contextual.html
Session = scoped_session(lambda: get_db_session(), scopefunc=lambda: get_db_session())


class Generators:
    Now = factory.LazyFunction(datetime.now)
    UtcNow = factory.LazyFunction(datetime_util.utcnow)
    UuidObj = factory.Faker("uuid4", cast_to=None)
    PhoneNumber = factory.Sequence(lambda n: f"123-456-{n:04}")


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class OpportunityFactory(BaseFactory):
    class Meta:
        model = opportunity_models.Opportunity

    opportunity_id = factory.Sequence(lambda n: n)

    opportunity_number = factory.Faker("opportunity_number")
    opportunity_title = factory.Faker("opportunity_title")

    agency = factory.Faker("agency")

    category = factory.fuzzy.FuzzyChoice(OpportunityCategory)
    # only set the category explanation if category is Other
    category_explanation = factory.Maybe(
        decider=factory.LazyAttribute(lambda o: o.category == OpportunityCategory.OTHER),
        yes_declaration=factory.Faker("sentence", nb_words=3),
        no_declaration=None,
    )

    is_draft = False  # Because we filter out drafts, just default these to False

    revision_number = 0  # We'll want to consider how we handle this when we add history

    opportunity_assistance_listings = factory.RelatedFactoryList(
        "tests.src.db.models.factories.OpportunityAssistanceListingFactory",
        factory_related_name="opportunity",
        size=lambda: random.randint(1, 3),
    )

    # By default we'll add a current opportunity summary which will be POSTED
    # if you'd like to easily modify the values, see the possible traits below in the
    # Params class section
    current_opportunity_summary = factory.RelatedFactory(
        "tests.src.db.models.factories.CurrentOpportunitySummaryFactory",
        factory_related_name="opportunity",
    )

    class Params:
        # These are common scenarios we might want for an opportunity.
        # Simply pass the in `trait_name=True` to the factory when making an object
        # and all of these will be set for you on the relevant models
        # See: https://factoryboy.readthedocs.io/en/stable/reference.html#traits

        no_current_summary = factory.Trait(current_opportunity_summary=None)

        # We set a trait for the OpportunitySummaryFactory for each of these as well as set the opportunity status
        is_posted_summary = factory.Trait(current_opportunity_summary__is_posted_summary=True)
        is_forecasted_summary = factory.Trait(
            current_opportunity_summary__is_forecasted_summary=True
        )
        is_closed_summary = factory.Trait(current_opportunity_summary__is_closed_summary=True)
        is_archived_non_forecast_summary = factory.Trait(
            current_opportunity_summary__is_archived_non_forecast_summary=True
        )
        is_archived_forecast_summary = factory.Trait(
            current_opportunity_summary__is_archived_forecast_summary=True
        )

        # Set all nullable fields to null
        all_fields_null = factory.Trait(
            agency=None,
            category=None,
            category_explanation=None,
            current_opportunity_summary=None,
            opportunity_assistance_listings=None,
        )

        # Set the timestamps in the past rather than using the default of "now"
        timestamps_in_past = factory.Trait(
            created_at=factory.Faker("date_time_between", start_date="-5y", end_date="-3y"),
            updated_at=factory.Faker("date_time_between", start_date="-3y", end_date="-1y"),
        )


class OpportunitySummaryFactory(BaseFactory):
    class Meta:
        model = opportunity_models.OpportunitySummary

    opportunity = factory.SubFactory(OpportunityFactory)
    opportunity_id = factory.LazyAttribute(lambda s: s.opportunity.opportunity_id)

    summary_description = factory.Faker("summary_description")
    is_cost_sharing = factory.Faker("boolean")

    # By default generate non-forecasts which affects several fields
    is_forecast = False

    # Forecasted records don't have a close date
    close_date = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: s.is_forecast),
        # If forecasted, don't set a close date
        yes_declaration=None,
        # otherwise a future date
        no_declaration=factory.Faker("date_between", start_date="+2w", end_date="+3w"),
    )
    close_date_description = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: s.close_date is None),
        yes_declaration=None,
        no_declaration=factory.Faker("paragraph", nb_sentences=1),
    )

    # Just a random recent post date
    post_date = factory.Faker("date_between", start_date="-3w", end_date="now")

    # By default set to a date in the future
    archive_date = factory.Faker("date_between", start_date="+3w", end_date="+4w")

    unarchive_date = None

    expected_number_of_awards = factory.Faker("random_int", min=1, max=25)
    estimated_total_program_funding = factory.Faker(
        "random_int", min=10_000, max=10_000_000, step=5_000
    )
    award_floor = factory.LazyAttribute(
        lambda s: s.estimated_total_program_funding // s.expected_number_of_awards
    )
    award_ceiling = factory.LazyAttribute(lambda s: s.estimated_total_program_funding)

    additional_info_url = factory.Faker("relevant_url")
    additional_info_url_description = factory.Faker("additional_info_desc")

    funding_category_description = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: fake.boolean()),  # random chance to include value
        yes_declaration=factory.Faker("paragraph", nb_sentences=1),
        no_declaration=None,
    )
    applicant_eligibility_description = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: fake.boolean()),  # random chance to include value
        yes_declaration=factory.Faker("paragraph", nb_sentences=5),
        no_declaration=None,
    )

    agency_code = factory.Faker("agency")
    agency_name = factory.Faker("agency_name")
    agency_phone_number = Generators.PhoneNumber
    agency_contact_description = factory.Faker("agency_contact_description")
    agency_email_address = factory.Faker("email")
    agency_email_address_description = factory.LazyAttribute(
        lambda s: f"Contact {s.agency_name} via email"
    )

    # Forecasted values are only set if is_forecast=True
    forecasted_post_date = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: s.is_forecast),
        # If forecasted, set it in the future
        yes_declaration=factory.Faker("date_between", start_date="+2w", end_date="+3w"),
        # otherwise don't set
        no_declaration=None,
    )
    forecasted_close_date = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: s.is_forecast),
        # If forecasted, set it in the future
        yes_declaration=factory.Faker("date_between", start_date="+6w", end_date="+12w"),
        # otherwise don't set
        no_declaration=None,
    )
    forecasted_close_date_description = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: s.forecasted_close_date is None),
        yes_declaration=None,
        no_declaration=factory.Faker("paragraph", nb_sentences=1),
    )
    forecasted_award_date = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: s.is_forecast),
        # If forecasted, set it in the future
        yes_declaration=factory.Faker("date_between", start_date="+26w", end_date="+30w"),
        # otherwise don't set
        no_declaration=None,
    )
    forecasted_project_start_date = factory.Maybe(
        decider=factory.LazyAttribute(lambda s: s.is_forecast),
        # If forecasted, set it in the future
        yes_declaration=factory.Faker("date_between", start_date="+30w", end_date="+52w"),
        # otherwise don't set
        no_declaration=None,
    )
    fiscal_year = factory.LazyAttribute(
        lambda s: s.forecasted_project_start_date.year if s.forecasted_project_start_date else None
    )

    is_deleted = False

    # Generally, current summaries won't have the revision number set
    revision_number = None

    funding_instruments = factory.Faker(
        "random_elements",
        length=random.randint(1, 3),
        elements=[f for f in FundingInstrument],
        unique=True,
    )
    funding_categories = factory.Faker(
        "random_elements",
        length=random.randint(1, 3),
        elements=[f for f in FundingCategory],
        unique=True,
    )
    applicant_types = factory.Faker(
        "random_elements",
        length=random.randint(1, 3),
        elements=[a for a in ApplicantType],
        unique=True,
    )

    class Params:
        # These are common overrides we might want for an opportunity summary.
        # Simply pass the in `trait_name=True` to the factory when making an object
        # and all of these will be set for you, overriding the above defaults
        # See: https://factoryboy.readthedocs.io/en/stable/reference.html#traits

        # The default state of values above assumes an "active" summary that has been
        # posted, so only need to configure the is_forecast field for these two
        is_posted_summary = factory.Trait(is_forecast=False)
        is_forecasted_summary = factory.Trait(is_forecast=True)

        # For these scenarios, adjust a few dates to make more sense
        is_closed_summary = factory.Trait(
            is_forecast=False,
            post_date=factory.Faker("date_between", start_date="-6w", end_date="-5w"),
            close_date=factory.Faker("date_between", start_date="-3w", end_date="-1w"),
        )

        is_archived_non_forecast_summary = factory.Trait(
            is_forecast=False,
            post_date=factory.Faker("date_between", start_date="-6w", end_date="-5w"),
            close_date=factory.Faker("date_between", start_date="-3w", end_date="-2w"),
            archive_date=factory.Faker("date_between", start_date="-2w", end_date="-1w"),
        )
        is_archived_forecast_summary = factory.Trait(
            is_forecast=True,
            post_date=factory.Faker("date_between", start_date="-6w", end_date="-5w"),
            archive_date=factory.Faker("date_between", start_date="-2w", end_date="-1w"),
        )

        is_non_public_non_forecast_summary = factory.Trait(
            is_forecast=False,
            post_date=factory.Faker("date_between", start_date="+3w", end_date="+4w"),
        )
        is_non_public_forecast_summary = factory.Trait(
            is_forecast=True,
            post_date=factory.Faker("date_between", start_date="+3w", end_date="+4w"),
        )

        # Set all nullable fields to null
        all_fields_null = factory.Trait(
            summary_description=None,
            is_cost_sharing=None,
            post_date=None,
            close_date=None,
            close_date_description=None,
            archive_date=None,
            unarchive_date=None,
            expected_number_of_awards=None,
            estimated_total_program_funding=None,
            award_floor=None,
            award_ceiling=None,
            additional_info_url=None,
            additional_info_url_description=None,
            forecasted_post_date=None,
            forecasted_close_date=None,
            forecasted_close_date_description=None,
            forecasted_award_date=None,
            forecasted_project_start_date=None,
            fiscal_year=None,
            modification_comments=None,
            funding_category_description=None,
            applicant_eligibility_description=None,
            agency_code=None,
            agency_name=None,
            agency_phone_number=None,
            agency_contact_description=None,
            agency_email_address=None,
            agency_email_address_description=None,
            is_deleted=None,
            funding_instruments=[],
            funding_categories=[],
            applicant_types=[],
        )

        no_link_values = factory.Trait(
            link_funding_instruments=[],
            link_funding_categories=[],
            link_applicant_types=[],
        )


class CurrentOpportunitySummaryFactory(BaseFactory):
    class Meta:
        model = opportunity_models.CurrentOpportunitySummary

    opportunity = factory.SubFactory(OpportunityFactory)
    opportunity_id = factory.LazyAttribute(lambda a: a.opportunity.opportunity_id)

    opportunity_summary = factory.SubFactory(
        OpportunitySummaryFactory, opportunity=factory.SelfAttribute("..opportunity")
    )
    opportunity_summary_id = factory.LazyAttribute(
        lambda a: a.opportunity_summary.opportunity_summary_id
    )

    opportunity_status = OpportunityStatus.POSTED

    class Params:
        is_posted_summary = factory.Trait(
            opportunity_status=OpportunityStatus.POSTED, opportunity_summary__is_posted_summary=True
        )
        is_forecasted_summary = factory.Trait(
            opportunity_status=OpportunityStatus.FORECASTED,
            opportunity_summary__is_forecasted_summary=True,
        )
        is_closed_summary = factory.Trait(
            opportunity_status=OpportunityStatus.CLOSED, opportunity_summary__is_closed_summary=True
        )
        is_archived_non_forecast_summary = factory.Trait(
            opportunity_status=OpportunityStatus.ARCHIVED,
            opportunity_summary__is_archived_non_forecast_summary=True,
        )
        is_archived_forecast_summary = factory.Trait(
            opportunity_status=OpportunityStatus.ARCHIVED,
            opportunity_summary__is_archived_forecast_summary=True,
        )


class OpportunityAssistanceListingFactory(BaseFactory):
    class Meta:
        model = opportunity_models.OpportunityAssistanceListing

    opportunity = factory.SubFactory(OpportunityFactory)
    opportunity_id = factory.LazyAttribute(lambda a: a.opportunity.opportunity_id)

    program_title = factory.Faker("company")
    assistance_listing_number = factory.LazyFunction(
        lambda: f"{fake.random_int(min=1, max=99):02}.{fake.random_int(min=1, max=999):03}"
    )


class LinkOpportunitySummaryFundingInstrumentFactory(BaseFactory):
    class Meta:
        model = opportunity_models.LinkOpportunitySummaryFundingInstrument

    opportunity_summary = factory.SubFactory(OpportunitySummaryFactory)
    opportunity_summary_id = factory.LazyAttribute(
        lambda f: f.opportunity_summary.opportunity_summary_id
    )

    # We use an iterator here to keep the values unique when generated by the opportunity factory
    funding_instrument = factory.Iterator(FundingInstrument)


class LinkOpportunitySummaryFundingCategoryFactory(BaseFactory):
    class Meta:
        model = opportunity_models.LinkOpportunitySummaryFundingCategory

    opportunity_summary = factory.SubFactory(OpportunitySummaryFactory)
    opportunity_summary_id = factory.LazyAttribute(
        lambda f: f.opportunity_summary.opportunity_summary_id
    )

    # We use an iterator here to keep the values unique when generated by the opportunity factory
    funding_category = factory.Iterator(FundingCategory)


class LinkOpportunitySummaryApplicantTypeFactory(BaseFactory):
    class Meta:
        model = opportunity_models.LinkOpportunitySummaryApplicantType

    opportunity_summary = factory.SubFactory(OpportunitySummaryFactory)
    opportunity_summary_id = factory.LazyAttribute(
        lambda f: f.opportunity_summary.opportunity_summary_id
    )

    # We use an iterator here to keep the values unique when generated by the opportunity factory
    applicant_type = factory.Iterator(ApplicantType)


####################################
# Staging Table Factories
####################################


class StagingTopportunityFactory(BaseFactory):
    class Meta:
        model = staging.opportunity.Topportunity

    opportunity_id = factory.Sequence(lambda n: n)

    oppnumber = factory.Faker("opportunity_number")
    opptitle = factory.Faker("opportunity_title")

    owningagency = factory.Faker("agency")

    oppcategory = factory.fuzzy.FuzzyChoice(OpportunityCategoryLegacy)
    # only set the category explanation if category is Other
    category_explanation = factory.Maybe(
        decider=factory.LazyAttribute(lambda o: o.oppcategory == OpportunityCategoryLegacy.OTHER),
        yes_declaration=factory.Faker("sentence", nb_words=5),
        no_declaration=None,
    )

    is_draft = "N"

    revision_number = 0

    created_date = factory.Faker("date_time_between", start_date="-10y", end_date="-5y")
    last_upd_date = sometimes_none(
        factory.Faker("date_time_between", start_date="-5y", end_date="today")
    )

    # Default to being a new insert/update
    is_deleted = False
    transformed_at = None

    class Params:
        already_transformed = factory.Trait(
            transformed_at=factory.Faker("date_time_between", start_date="-7d", end_date="-1d")
        )


####################################
# Transfer Table Factories
####################################


class TransferTopportunityFactory(BaseFactory):
    class Meta:
        model = transfer_topportunity_models.TransferTopportunity

    opportunity_id = factory.Sequence(lambda n: n)

    oppnumber = factory.Sequence(lambda n: f"ABC-{n}-XYZ-001")
    opptitle = factory.LazyFunction(lambda: f"Detailed research into {fake.job()} industry")

    owningagency = factory.Faker("agency")

    oppcategory = factory.fuzzy.FuzzyChoice(OpportunityCategoryLegacy)
    # only set the category explanation if category is Other
    category_explanation = factory.Maybe(
        decider=factory.LazyAttribute(lambda o: o.oppcategory == OpportunityCategoryLegacy.OTHER),
        yes_declaration=factory.Sequence(lambda n: f"Category as chosen by order #{n * n - 1}"),
        no_declaration=None,
    )

    is_draft = "N"  # Because we filter out drafts, just default these to False

    revision_number = 0

    # Make sure updated_at is after created_at just to make the data realistic
    created_at = factory.Faker("date_time")
    updated_at = factory.LazyAttribute(
        lambda o: fake.date_time_between(start_date=o.created_at, end_date="now")
    )

    created_date = factory.LazyAttribute(lambda o: o.created_at.date())
    last_upd_date = factory.LazyAttribute(lambda o: o.updated_at.date())


####################################
# Foreign Table Factories
####################################


class ForeignTopportunityFactory(factory.DictFactory):
    """
    NOTE: This generates a dictionary - and does not connect to the database directly
    """

    opportunity_id = factory.Sequence(lambda n: n)

    oppnumber = factory.Sequence(lambda n: f"F-ABC-{n}-XYZ-001")
    opptitle = factory.LazyFunction(lambda: f"Research into {fake.job()} industry".replace("'", ""))

    owningagency = factory.Iterator(["F-US-ABC", "F-US-XYZ", "F-US-123"])

    oppcategory = factory.fuzzy.FuzzyChoice(OpportunityCategoryLegacy)
    # only set the category explanation if category is Other
    category_explanation = factory.Maybe(
        decider=factory.LazyAttribute(lambda o: o.oppcategory == OpportunityCategoryLegacy.OTHER),
        yes_declaration=factory.Sequence(lambda n: f"Category as chosen by order #{n * n - 1}"),
        no_declaration=None,
    )

    is_draft = "N"  # Because we filter out drafts, just default these to False

    revision_number = 0

    created_date = factory.Faker("date_between", start_date="-10y", end_date="-5y")
    last_upd_date = factory.Faker("date_between", start_date="-5y", end_date="today")
