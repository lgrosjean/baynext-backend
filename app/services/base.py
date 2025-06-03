from pydantic import BaseModel
from sqlmodel import Session, select


class BaseService:
    """
    Base service class for managing database operations.
    """

    def __init__(self, session: Session, project_id: str):
        self.session = session
        self.project_id = project_id

    def __init_subclass__(cls, model_class: type[BaseModel]):
        """
        Initialize the subclass with the model class.
        """
        cls.model_class = model_class

    def create(self, model: type[BaseModel]):
        """
        Create a new record in the database.
        """
        db_model = self.model_class.model_validate(model)
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model

    def get(self, model_id):
        """
        Retrieve a record from the database by ID.
        """
        return self.session.get(self.model_class, model_id)

    def update(self, model):
        """
        Update an existing record in the database.
        """
        self.session.commit()
        self.session.refresh(model)
        return model

    def delete(self, model):
        """
        Delete a record from the database.
        """
        self.session.delete(model)
        self.session.commit()

    def list(self):
        """
        List all records of a given model class.
        """
        return self.session.exec(select(self.model_class)).all()


def make_service(model_class: BaseModel):
    """
    Factory function to create a service class for a given model class.
    """

    class ModelService(BaseService, model_class=model_class):
        pass

    return ModelService
