def build_recipes(recipes, first, second):
    if len(recipes) % 10000 < 2:
        print(len(recipes))
    created = recipes[first] + recipes[second]
    if created < 10:
        recipes.append(created)
    else:
        recipes.append(1)
        recipes.append(created - 10)
    first = (first + recipes[first] + 1) % len(recipes)
    second = (second + recipes[second] + 1) % len(recipes)
    return first, second

recipes = [3, 7]
first = 0
second = 1
target = 236021
while len(recipes) < target + 10:
    first, second = build_recipes(recipes, first, second)
print(recipes[target:target+10])

recipes = [3, 7]
first = 0
second = 1
target_list = [2,3,6,0,2,1]
while recipes[-len(target_list):] != target_list and recipes[-len(target_list)-1:-1] != target_list:
    first, second = build_recipes(recipes, first, second)
if recipes[-len(target_list):] == target_list:
    print(len(recipes) - len(target_list))
else:
    print(len(recipes) - len(target_list) - 1)