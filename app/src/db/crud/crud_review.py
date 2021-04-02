from dependency_injector.providers import Factory
from src.db.crud.crud_base import CRUDBase
from src.db.models.review import Review as ReviewDbModel
from src.schemas.review import Review, ReviewCreate, ReviewUpdate


class CRUDReview(CRUDBase[ReviewDbModel, Review, ReviewCreate, ReviewUpdate]):
    pass


CRUDReviewFactory = Factory(CRUDReview, model=ReviewDbModel, schema=Review)
