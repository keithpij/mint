"""
Demo of a basic pie chart plus a few additional features.

In addition to the basic pie chart, this demo shows a few optional features:

    * slice labels
    * auto-labeling the percentage
    * offsetting a slice with "explode"
    * drop-shadow
    * custom start angle

Note about the custom start angle:

The default ``startangle`` is 0, which would start the "Frogs" slice on the
positive x-axis. This example sets ``startangle = 90`` such that everything is
rotated counter-clockwise by 90 degrees, and the frog slice starts on the
positive y-axis.
"""
import matplotlib.pyplot as plt

def category_pie_chart(categories):
    ''' Pie chart, where the slices will be ordered and plotted counter-clockwise.'''

    # Create a list of totals for each category.
    labels = []
    sizes = []
    explode = []
    for category_name in categories.keys():
        labels.append(category_name)
        total = 0
        for transaction in categories[category_name]:
            total += transaction.amount
        sizes.append(total)
        explode.append(0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
