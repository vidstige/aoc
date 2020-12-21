from collections import defaultdict
import re
import sys

def parse(f):
    for line in f:
        match = re.match(r'(.*)\(contains (.+)\)', line)
        if match:
            ingredients_list, allergens_list = match.groups()
            yield set(ingredients_list.split()), set(allergens_list.split(', '))

def solve(items):
    a = {}
    for ingredients, allergens in items:
        for allergen in allergens:
            if allergen in a:
                a[allergen] = ingredients.intersection(a[allergen])
            else:
                a[allergen] = ingredients
    suspects = set().union(*a.values())
    #all_ingredients = set().union(*(i for i, a in items))
    #safe = all_ingredients - suspects
    all_allergens = set()
    for ingredients, allergens in items:
        all_allergens.update(allergens)

    singles = set.union(*[ingredients for ingredients in a.values() if len(ingredients) == 1])
    while len(singles) < len(all_allergens):
        for allergen, s in a.items():
            if len(s) > 1:
                s -= singles
        singles = set.union(*[ingredients for ingredients in a.values() if len(ingredients) == 1])
    return [(allergen, next(iter(ingredients))) for allergen, ingredients in a.items()]

        

food_items = list(parse(sys.stdin))
mapping = solve(food_items)
print(','.join(ingredient for _, ingredient in sorted(mapping)))

