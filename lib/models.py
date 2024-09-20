from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Recipe(name='{self.name}', description='{self.description}')>"


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(String)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship("Recipe", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient(name='{self.name}', quantity='{self.quantity}')>"
