import argparse
from sqlalchemy.orm import Session
from models import Recipe, Ingredient
from db import get_db, init_db

init_db()

def add_recipe(name, description, ingredients):
    db = next(get_db())
    recipe = Recipe(name=name, description=description)
    for ingredient_data in ingredients:
        parts= ingredient_data.split(':')
        if len(parts) == 2:
            ingredient_name, quantity = parts
        elif len(parts) == 1:
            ingredient_name = parts[0]
            quantity = '1 unit'
        else:
            print(f"Error: Invalid ingredient format '{ingredient_data}'")
        ingredient = Ingredient(name=ingredient_name, quantity=quantity)
        recipe.ingredients.append(ingredient)
    db.add(recipe)
    db.commit()
    print(f"Added recipe: {recipe.name} with ID: {recipe.id}")
    for ingredient in recipe.ingredients:
        print(f"    Ingredient: {ingredient.name}, Quantity: {ingredient.quantity}")
        
        
def update_recipe(recipe_id, name=None, description=None):
    db = next(get_db())
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        if name:
            recipe.name = name
        if description:
            recipe.description = description
        db.commit()
        print(f"Recipe '{recipe.name}' updated successfully.")
    else:
        print(f"Recipe with id '{recipe_id}' not found.")

def delete_recipe(recipe_id):
    db = next(get_db())
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
        print(f"Recipe '{recipe.name}' deleted successfully.")
    else:
        print(f"Recipe with id '{recipe_id}' not found.")

def search_recipe(search_term):
    db = next(get_db())
    results = db.query(Recipe).filter(Recipe.name.ilike(f"%{search_term}%")).all()
    if results:
        for recipe in results:
            print(f"ID: {recipe.id}, Name: {recipe.name}, Description: {recipe.description}")
            for ingredient in recipe.ingredients:
                print(f"    - {ingredient.name}: {ingredient.quantity}")
    else:
        print(f"No recipes found for search term '{search_term}'.")

def main():
    parser = argparse.ArgumentParser(description="Recipe Manager CLI")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new recipe')
    add_parser.add_argument('--name', required=True, help='Name of the recipe')
    add_parser.add_argument('--description', help='Description of the recipe')
    add_parser.add_argument('--ingredients', nargs='+', required=True, help="Ingredients in format 'name:quantity'")

    update_parser = subparsers.add_parser('update', help='Update a recipe')
    update_parser.add_argument('--id', required=True, type=int, help='Recipe ID to update')
    update_parser.add_argument('--name', help='New name of the recipe')
    update_parser.add_argument('--description', help='New description of the recipe')

    delete_parser = subparsers.add_parser('delete', help='Delete a recipe')
    delete_parser.add_argument('--id', required=True, type=int, help='Recipe ID to delete')

    search_parser = subparsers.add_parser('search', help='Search for a recipe')
    search_parser.add_argument('--term', required=True, help='Search term for recipe name')

    args = parser.parse_args()

    if args.command == 'add':
        add_recipe(args.name, args.description, args.ingredients)
    elif args.command == 'update':
        update_recipe(args.id, args.name, args.description)
    elif args.command == 'delete':
        delete_recipe(args.id)
    elif args.command == 'search':
        search_recipe(args.term)

if __name__ == "__main__":
    main()

print("****WELCOME TO TASTY FOODS****")
print("To add a meal, use keyword 'add --name"" --description"" --ingredients""'")
print("To update a meal, use keyword 'update --id --name"" --description"" --ingredients""'")
print("To delete a meal, use keyword delete --id''")
print("To search for a meal, use keyword search --term''")