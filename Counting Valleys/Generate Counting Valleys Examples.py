import random
import pandas as pd
import matplotlib.pyplot as plt

def get_random_step() -> int:
    """Generate a random integer 0 or 1.

    Returns:
        int: Either 0 or 1.
    """
    return random.randrange(0, 2)

def generate_up_down_string(length: int) -> str:
    """Generate a string consisting of 'U' (up) and 'D' (down) steps.

    Args:
        length (int): The length of the string to generate.

    Returns:
        str: A string of 'U' and 'D' characters of specified length.
    """
    steps = ''
    while len(steps) < length:
        steps += get_random_step() * 'U' + get_random_step() * 'D'
    return steps[:length]


def create_elevation_dataframe(up_down_string: str) -> pd.DataFrame:
    """Create a DataFrame from a string of 'U' and 'D' steps showing elevation changes.

    Args:
        up_down_string (str): A string of 'U' and 'D' representing steps up and down.

    Returns:
        pd.DataFrame: DataFrame with columns for the step index, elevation, and step direction.
    """
    elevation_array = [0]
    elevation = 0
    for step in up_down_string:
        if step == 'U':
            elevation += 1
        else:
            elevation -= 1
        elevation_array.append(elevation)
    
    return pd.DataFrame({
        'x': range(len(up_down_string) + 1),
        'Elevation': elevation_array,
        'UD': [pd.NA] + list(up_down_string)
    })


def plot_elevation_line(df: pd.DataFrame, elevation: int) -> str:
    """Generate a string representing the elevation change line for a specific elevation.

    Args:
        df (pd.DataFrame): The elevation DataFrame.
        elevation (int): The specific elevation level to plot.

    Returns:
        str: A string representing the elevation line.
    """
    filtered_df = df[((df['Elevation'] == elevation) & (df['UD'] == 'U')) | 
                     ((df['Elevation'] == elevation - 1) & (df['UD'] == 'D')) & # 'D' values need to be offset to align correctly
                     (df['x'] > 0)].reset_index(drop=True) # Required to pull data points in order after filtering
    elevation_line = ''
    last_x = 0
    
    for i in range(len(filtered_df)):
        x_position = filtered_df.loc[i, 'x']
        step_direction = filtered_df.loc[i, 'UD']
        symbol = '/' if step_direction == 'U' else '\\' # '\' needs an extra \ as an escape character
        elevation_line += ' ' * (x_position - last_x - 1) + symbol
        last_x = x_position
    
    return elevation_line


def plot_elevation_range(df: pd.DataFrame, min_elevation: int, max_elevation: int) -> None:
    """Print elevation lines for a range of elevations.

    Args:
        df (pd.DataFrame): The elevation DataFrame.
        min_elevation (int): The minimum elevation level to plot.
        max_elevation (int): The maximum elevation level to plot.
    """
    for elevation in range(max_elevation, min_elevation , -1):
        print(plot_elevation_line(df, elevation))


    
n = 20 # Step length

UDstr  = generate_up_down_string(n)
df = create_elevation_dataframe(UDstr)

print(UDstr)

plot_elevation_range(df,min(df['Elevation']),max(df['Elevation'])) # Plot as a string with no empty space


plt.figure(figsize=(10, 5)) 
plt.plot(df['x'], df['Elevation'])  # Line plot

# Filtering for points where elevation is zero to mark hill and valley ends
zero_pointsU = df[(df['Elevation'] == 0) & (df['UD']=='U')]
zero_pointsD = df[(df['Elevation'] == 0) & (df['UD']=='D')]

# Plotting hill and valley ends with different colours
plt.scatter(zero_pointsU['x'], zero_pointsU['Elevation'], color='green', s=100, edgecolors='black', label='Zero Elevation', zorder=5)
plt.scatter(zero_pointsD['x'], zero_pointsD['Elevation'], color='red', s=100, edgecolors='black', label='Zero Elevation', zorder=5)

# Remove whitespace around axes
plt.xlim(min(df['x']), max(df['x']))
plt.ylim(min(df['Elevation']), max(df['Elevation']))

plt.title('Elevation vs. X')
plt.xlabel('X')
plt.ylabel('Elevation')

plt.grid(True)

plt.axhline(y=0, color='black', linestyle='--', label='x=0 Line') 

# Show the plot
plt.show()

