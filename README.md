# 🍲 Recipys 🍲
Get recipe ideas directly from your CLI. Use meal type and/or ingredients to narrow your search.

## Details
This app will provide you with a recipe scraped from the web. The recipe is presented in a table format with ingredients and steps. If you are struggling to find ideas for your next meal or want to know what you can do with the ingredients you have at home, give *recipys* a try.

## Installation
The tool is available as a `pip` package. Download it with the following command:
```
pip install connect-4-cli
```

Preferably, install in [virtual environment](https://docs.python.org/3/library/venv.html).

## How to Use
Run the following command to get a random recipe:
```
recipys random
```

To filter per meal type, choose one of the following arguments: `breakfast`, `lunch`, `dinner`, `dessert`. The result will be random but narrowed to your filter. For example:
```
recipys breakfast
```

If you want to narrow the search with specific ingredients, specify them writing as many ingredients as you want after the `with` keyword. For example:
```
recipys with cheese onion bacon
```

You can also combine meal type and ingredients in your search. Make sure to specify the ingredients *after* the meal type. For example:
```
recipys dessert with chocolate banana
```