## Introduction

Below are two memos that I wrote announcing a long-awaited feature in an open
source, publicly available Python SDK that my last company both maintained and
heavily utilized to deploy certain enterprise integrations. The first memo
describes the feature's arrival and how to use it. The second memo, circulated
a few sprints later, follows up on additional enhancements.

I edited both passages and their accompanying data to obscure any reference to
internal procedure or other sensitive knowledge (which would furthermore be
obsolete at this point).

## Rollout

### Message

Hello, Customer Team!

As you may know, the team and I have been improving the platform to provide more
detailed error messages during the Machine Learning workflow's CSV data
validation stage. Think less "this CSV file is invalid; good luck figuring
out how", and more "in row 4, column 6, you provided a string where a number was
expected". As of the next release, the Python client will show these specific
troubleshooting messages when the CSV is being read in and uploaded to train
Predictors.

Specifically, the update will introduce two new validations that may affect
customer projects. We wanted to notify you in case you need to tweak those
projects accordingly or answer customers' questions.

Consider the example CSV attached below. Suppose you attempt the following
column definitions:

```python
training_data_data_source = CSVDataSource(
    file_link=training_data_file_link,
    column_definitions={
        "pressure": RealDescriptor("Pressure", lower_bound=1, upper_bound=5, units="Pa"),
        "time": RealDescriptor("time", lower_bound=0, upper_bound=100, units="s"),
        "sprinkles": CategoricalDescriptor("sprinkles", {"yellow", "pink", "purple"}),
        "temperature": RealDescriptor("temperature", lower_bound=0, upper_bound=10, units="F"),
        "yummy_index": RealDescriptor("temperature", lower_bound=0, upper_bound=300, units="")
    }
)
```

This will now cause our system to display two errors:

(1) `ColumnNotFound`

<ul>

```
No column named 'pressure' in 'cake.csv'
```

To fix,

- add a column named "pressure", or
- change "pressure" to "press" (if that's what you meant), or
- remove this column definition altogether.
</ul>

(2) `DuplicateDescriptor`

<ul>

```
Multiple columns map to descriptor key 'temperature'
```

To fix, change the last descriptor key to `yummy_index`.
</ul>

During this sprint, the team actually found a descriptor that referred to a
column that didn't exist in the data, as well as a descriptor key naming
collision! Luckily, those issues only popped up in internal tests, but if we
made those mistakes, then there's a chance that a client project out there
could have the same mistakes. Hence the heads up.

We're aware that CSV data validation also occurs when CSV files are uploaded
to create Enumerated Design Spaces. We plan to turn on the same specific error
messaging for that use case in the coming weeks.

I hope this was helpful. Please reach out with any questions!


### Data

| time     | sprinkles | temperature | yummy_index | press |
| :--------|:----------| :-----------|------------:|------:|
| 540      | yellow    | 200         | 101.99      | 2     |
| 332.5    | pink      | 215         |             | 3     |
| 198.6    | purple    | 300         | 202.88      | 4     |
| 266      | rainbow   | 325         | 79.00       | 5     |
| 380      | yellow    | 350 F       | 158.2       | 1     |
| 475      | pink      | 375         | delicious   | 1     |
| 198.6    | purple    | 400         | 289.90      | 2     |
| 304      | pink      | 425         | scrumptious | 5     |


I hope this was helpful; please reach out if you have questions. Thank you!


## Follow-up

### Message

Hello, Esteemed Customer Team!

As of today's production release, CSV data source validations are now activated
for when you create Design Spaces, too! These are the same validations that
appear when you upload a CSV to create a Predictor.

Suppose you are using the attached spreadsheet to enumerate a Design Space of
dessert recipe candidates to maximize Top Chef scores. You already uploaded it
into your Python script as `candidates_file_link`. Next, you try:

```python
from citrine.informatics.design_spaces import DataSourceDesignSpace

candidates_data_source = CSVDataSource(
    file_link=candidates_file_link,
    column_definitions={
        "Minutes": RealDescriptor("Minutes", lower_bound=0, upper_bound=600, units="s"),
        "Cocoa": RealDescriptor("Cocoa", lower_bound=0, upper_bound=300, units=""),
        "Sprinkles": CategoricalDescriptor("Sprinkles", categories=["red", "pink", "purple"]),
        "Temp": RealDescriptor("Temp", lower_bound=0, upper_bound=300, units=""),
        "Yogurt": RealDescriptor("Cocoa", lower_bound=0, upper_bound=300, units=""),
        "Pressure": RealDescriptor("Pressure", lower_bound=0, upper_bound=10000, units=""),
        "Honey": RealDescriptor("Honey", lower_bound=0, upper_bound=10000, units=""),
        "RPM": RealDescriptor("RPM", lower_bound=0, upper_bound=365, units=""),
        "Proprietary": ChemicalFormulaDescriptor(key="Proprietary"),
        "Secret Ingredient": MolecularStructureDescriptor(key="Secret Ingredient")
    }
)

design_space = project.design_spaces.register(
    DataSourceDesignSpace(
        name="Cake Candidate Recipes",
        description="",
        data_source=candidates_data_source,
    )
)

wait_while_validating(collection=project.design_spaces, module=design_space, print_status_info=True)
```

Notice that both the spreadsheet and the column definitions are riddled with
errors! Before today, the `wait_while_validating()` function would have failed
to create that design space and returned an `INVALID` status without saying
what, exactly, went wrong. But starting today, it will output:

```
Status = INVALID                  Elapsed time  =   0s
Status info:
["No column named 'Pressure' in 'cake-candidates-demo.csv'",
 "Multiple columns map to descriptor key 'Cocoa'",
 "File 'dessert-candidates.csv' at row 1, column 'Minutes': '700' is outside "
 'the specified bounds.',
 "File 'dessert-candidates.csv' at row 2, column 'RPM': 'fast' is not a "
 'number.',
 "File 'dessert-candidates.csv' at row 3, column 'RPM': 'slow' is not a "
 'number.',
 "File 'dessert-candidates.csv' at row 4, column 'Sprinkles': 'blue' is not "
 'a valid category.',
 "File 'dessert-candidates.csv' at row 8, column 'Proprietary': "
 "'walnuts' is not a valid chemical formula.",
 "File 'dessert-candidates.csv' at row 11, column 'Sprinkles': 'green' is "
 'not a valid category.',
 "File 'dessert-candidates.csv' at row 12, column 'Secret Ingredient': 'cayenne "
 "pepper' is not a valid molecular structure.",
 "File 'dessert-candidates.csv' at row 20, column 'Temp': '-228' is "
 'outside the specified bounds.']
```

Hurray! Actionable Information! This example demonstrates all validation types
that the system performs now.

Please reach out with feedback, questions, and suggestions. Thank you for all
the amazing work that you do.

Your Humble Colleagues,
AI Engine & Research Team


### Data



| Minutes | Cocoa   | Sprinkles   | Temp  | Yogurt | Butter  | Honey   | RPM  | Proprietary | Secret Ingredient                                                              |
|--------:|--------:|:------------| -----:|-------:| -------:|--------:|-----:|:----------- |:---------------------------------------------------------------------------|
| 700     | 118.8   | red         | 181.1 | 8.9    | 852.1   | 781.5   | 56   | Ca1.89      | N=1C=CC=2SC=3C=4N=CC(=CC4NC3C2C1)C=5[Se]C=CC5
| 230     | 0       | pink        | 195.5 | 100    | 1029.4  | 758.6   | fast | Ge12.53     | N=1SN=C2C1C=CC=3[Se]C=4C=5C=CC(=CC5NC4C23)C=6SC=C7NC=CC67
| 238.1   | 0       | purple      | 186.7 | 7      | 949.9   | 847     | slow | Pd0.5       | N=1SN=C2C1C=CC=C2C3=CC=4[Se]C=5C=6N=CC=CC6C=NC5C4N3
| 475     | 118.8   | blue        | 181.1 | 8.9    | 852.1   | 781.5   | 91   | Rb0.5       | N=1SN=C2C1C=CC3=CC=C4C(N=CC=5C=C(C6=NSN=C6C54)C7=CC=CC7)=C23
| 166.1   | 0       | red         | 176.5 | 4.5    | 1058.6  | 780.1   | 56   | Fe0.735     | N=1C=NC(=NC1)C=2N=CC3=C(C2)C=4C=CC=CC4C5=C3C6=CSC=C6C=7C=CCC75
| 212.1   | 0       | red         | 180.3 | 5.7    | 1057.6  | 779.3   | 100  | Zn2.155     | N=1SN=C2C1C=3C=CNC3C=4C5=COC=C5C=6C=C(C=7SC=C8C=CNC87)CC6C24
| 237.5   | 237.5   | pink        | 228   | 0      | 932     | 594     | 365  | Mg0.88      | N=1SN=C2C1C=CC=3OC4=C(OC=5C=C(C=6SC=C7OC=CC76)C8=CNC=C8C54)C32
| 380     | 95      | red         | 228   | 0      | 932     | 594     | 7    | walnuts     | N=1C=CC=2C(C1)=C3SC=4C=C(C=5SC=C6C5C=CC6)C7=COC=C7C4C3=C8C=CC=CC28
| 198.6   | 132.4   | pink        | 192   | 0      | 978.4   | 825.5   | 180  | V0.732      | N=1SN=C2C1C=CC=3N=CC4=C(C5=NSN=C5C=6C=C(C=7[Se]C=CC7)CC46)C32
| 388.6   | 97.1    | purple      | 157.9 | 12.1   | 852.1   | 925.7   | 56   | N0.03       | N=1C=C2C(=CC1C=3SC=C4C=C[Se]C43)C5=COC=C5C=6C2=C7C=CC=CC7=C8C=CCC86
| 266     | 114     | green       | 228   | 0      | 932     | 670     | 90   | Cu2.64      | N=1SN=C2C1C(=CC3=NC=C4C=5C=CC=CC5C6=CSC=C6C4=C32)C=7SC=C8C=C[Se]C87
| 230     | 0       | red         | 195.5 | 4.6    | 1029.4  | 758.6   | 3    | Rh0.25      | cayenne pepper
| 425     | 106.3   | pink        | 151.4 | 18.6   | 936     | 803.7   | 7    | Al12        | S1C=C2C(C=CC2)=C1C=3C=C4NC=5C=6[Se]C=CC6[SiH2]C5C4=C7C=CC=CC73
| 190     | 190     | purple      | 228   | 0      | 932     | 670     | 90   | K32.128     | N=1SN=C2C1C=CN=C2C=3SC(=C4OC=CC43)C5=CC=C(N5)C6=CC=CC7=CSC=C76
| 194.7   | 0       | red         | 165.6 | 7.5    | 1006.4  | 905.9   | 14   | Te21.53     | N=1C=NC(=NC1)C=2N=CC=3C=4N=CC=CC4C5=NSN=C5C3C2
| 139.6   | 209.4   | pink        | 192   | 0      | 1047    | 806.9   | 28   | Lu2         | S1C=CC=C1C=2[Se]C(=CC2)C=3SC(C=4SC=C5SC=CC54)=C6C=C[Se]C36
| 427.5   | 47.5    | purple      | 228   | 0      | 932     | 594     | 90   | Ba2         | O1C=C2C=CC=3C4=CCC=C4C5=C(C6=CSC=C6C=7C=C(C=8SC=CC8)CC75)C3C2=C1
| 266     | 114     | red         | 228   | 0      | 932     | 670     | 180  | Ni5.09      | N1=CC=CC=C1C2=CC=3NC=4C5=C(C=CC6=C[SiH2]C=C65)C7=COC=C7C4C3C8=C[SiH2]C=C28
| 213.8   | 98.1    | pink        | 181.7 | 6.7    | 1066    | 785.5   | 56   | Sb1.5       | O1C=2C=CC3=C[SiH2]C=C3C2C=4C=CC=5C=C(NC5C14)C=6SC=C7C=CNC76
| 380     | 95      | purple      | -228  | 0      | 932     | 594     | 180  | La0.275     | N=1SN=C2C1C=CC=C2C3=NC=C(C=4N=CC(=CC4)C5=CC=CC6=CCC=C65)C7=NSN=C73
