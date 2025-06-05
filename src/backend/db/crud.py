from sqlalchemy.orm import Session
from abc import ABC
# Interface for CRUD operations on SQLAlchemy models
class BaseController(ABC):
    def __init__(self, db: Session):
        self.db = db

    def create(self, model):
        """
        Create a new record in the database.

        Args:
            model: An instance of the SQLAlchemy model to be created.

        Returns:
            The created model instance.
        """
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model
    
    def get(self, model_class, **kwargs):
        """
        Retrieve a record from the database.

        Args:
            model_class: The SQLAlchemy model class to query.
            **kwargs: Filter criteria for the query.

        Returns:
            The first matching record or None if not found.
        """
        return self.db.query(model_class).filter_by(**kwargs).first()
    
    def get_all(self, model_class):
        """
        Retrieve all records of a specific model from the database.

        Args:
            model_class: The SQLAlchemy model class to query.

        Returns:
            A list of all records of the specified model.
        """
        return self.db.query(model_class).all()
    
    def update(self, model, **kwargs):
        """
        Update an existing record in the database.

        Args:
            model: An instance of the SQLAlchemy model with updated data.
            **kwargs: Additional fields to update.

        Returns:
            The updated model instance.
        """
        for key, value in kwargs.items():
            setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, model, **kwargs):
        """
        Delete a record from the database.

        Args:
            model: An instance of the SQLAlchemy model to be deleted.
            **kwargs: Additional fields to filter the record to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        existing_model = self.get(model.__class__, id=kwargs.get('id'))
        import logging
        logging.warning(f"Attempting to delete model: {existing_model} with kwargs: {kwargs}")
        if existing_model:
            self.db.delete(existing_model)
            self.db.commit()
            return True
        raise ValueError(f"Record with {kwargs} not found for deletion")