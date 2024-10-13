
import panel as pn
import pandas as pd
import matplotlib.pyplot as plt

# Load Panel extension
pn.extension()

# Example dataset (Replace with your own data)
url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'
df = pd.read_csv(url)

# Widgets for user interaction
dropdown = pn.widgets.Select(name='Select Column', options=list(df.columns))
slider = pn.widgets.IntSlider(name='Bins', start=5, end=50, step=5, value=10)
checkbox_grid = pn.widgets.Checkbox(name='Show Gridlines', value=True)
multi_select = pn.widgets.MultiSelect(name='Columns', options=list(df.columns), size=4)

# Plotting function that updates based on widget input
@pn.depends(dropdown, slider, checkbox_grid)
def create_plot(column, bins, grid):
    plt.figure(figsize=(8, 6))
    df[column].hist(bins=bins, grid=grid)
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    return plt.gcf()

# Function to show correlations based on multi-select columns
@pn.depends(multi_select)
def show_correlations(selected_columns):
    if len(selected_columns) > 1:
        corr = df[selected_columns].corr()
        return pn.pane.DataFrame(corr)
    else:
        return "Please select at least two columns."

# Organize into tabs
dashboard = pn.Tabs(
    ('Overview', pn.Column(df.head(), df.describe())),
    ('Interactive Plot', pn.Column(dropdown, slider, checkbox_grid, pn.panel(create_plot))),
    ('Correlation Matrix', pn.Column(multi_select, show_correlations))
)

# Show dashboard layout (use dashboard.show() for deployment)
dashboard.servable()
