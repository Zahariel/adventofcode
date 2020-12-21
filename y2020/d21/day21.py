import re
import functools
import operator
from collections import defaultdict

import chooser

class Recipe:
    def __init__(self, ingredients, allergens):
        self.ingredients = set(ingredients)
        self.allergens = set(allergens)

    def __repr__(self):
        return f"Recipe({self.ingredients}, {self.allergens})"


def parse(line):
    ingredients, allergens = re.fullmatch(r"([a-z\s]+) \(contains ([a-z\s,]+)\)", line).groups()
    return Recipe(ingredients.split(), allergens.split(", "))


with open("input.txt") as f:
    recipes = [parse(line.strip()) for line in f]


# part 1
recipes_by_allergen = defaultdict(list)

for recipe in recipes:
    for allergen in recipe.allergens:
        recipes_by_allergen[allergen].append(recipe)

possibilities = {allergen: functools.reduce(operator.and_, (recipe.ingredients for recipe in recipes_by_allergen[allergen])) for allergen in recipes_by_allergen}

print(possibilities)

all_allergen_ingredients = functools.reduce(operator.or_, possibilities.values())

safe_count = sum(1 for recipe in recipes for ingredient in recipe.ingredients if ingredient not in all_allergen_ingredients)
print(safe_count)

# part 2
real_allergens = chooser.choose_dict(possibilities)

print(real_allergens)
print(",".join(real_allergens[key] for key in sorted(real_allergens)))
