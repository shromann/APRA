import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def participant_profile(df, column_name, cols):
    """
    Function to create and plot a bar chart for a specific column in the first sheet of an Excel file.

    Parameters:
    df (dataframe)
    column_name (str): The column name for which the bar chart is to be plotted.
    title (str): Title of the chart.
    xlabel (str): Label for the x-axis.
    ylabel (str): Label for the y-axis.
    """
    # Count the occurrences of each category in the column
    desc = df.iloc[0, :]
    data_counts = df.iloc[1:,:][column_name].value_counts()

    sns.set_theme(style="whitegrid")

    # Plotting the bar chart
    plt.figure(figsize=(10, 6), dpi=500)
    ax = data_counts.plot(kind='bar')
    plt.title(f'Participant Profile for {desc[column_name]} (n: {df.shape[0]})')
    plt.xlabel(desc[column_name])
    plt.ylabel('Number of Participants')

    plt.xticks(rotation=10)

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height() - 20),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.tight_layout()
    plt.savefig(f'./plots/{desc[column_name].replace("/","-")}_participant_profile.png')

def percentage_agreeable(df, column_name, cols):
    """
    Function to create and plot a line chart for percentage agreeable in different dimensions.

    Parameters:
    df (dataframe)
    column_name (str): The column name for which the line chart is to be plotted.
    """
    desc = df.iloc[0, :]

    def calculate_percentage_agreeable(row):
        agree_counts = row.isin(['Agree', 'Strongly agree']).sum()
        total_counts = row.notna().sum()
        return (agree_counts / total_counts) * 100 if total_counts > 0 else 0

    df_filtered = df.iloc[1:,:]
    
    percentage_agreeable = df_filtered.groupby(column_name)[cols].apply(lambda x: x.apply(calculate_percentage_agreeable))

    # Set the Seaborn whitegrid theme
    sns.set_theme(style="whitegrid")

    # Create a line plot using Seaborn
    plt.figure(figsize=(12, 8), dpi=500)
    for group in percentage_agreeable.index:
        sns.lineplot(data=percentage_agreeable.loc[group], label=group, marker='o')

    plt.title(f'Percentage Agreeable by {desc[column_name]} for Various Questions (n: {df_filtered.shape[0]})')
    plt.xlabel('Questions')
    plt.ylabel('Percentage Agreeable (%)')
    plt.xticks(rotation=45)
    plt.legend(title=desc[column_name])
    plt.tight_layout()

    plt.savefig(f'./plots/{desc[column_name].replace("/","-")}_percentage_agreeable.png')

def question_freq_percent(df):
    """
    Generates a bar chart showing frequency percentages of Likert scale responses for each survey question.

    This function processes a DataFrame of survey data to calculate and visualize the distribution of Likert 
    scale responses (Strongly Agree to Strongly Disagree) for each question. It excludes 'Not able to comment' 
    responses and assumes Likert responses start from the sixth column.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the survey data.

    Note:
    The plot is displayed directly and the function does not return any value.
    """


    # Filtering out the header row and the 'Unable to comment' responses
    survey_data_filtered = df[1:].replace('Not able to comment', pd.NA).dropna()

    # Selecting only the Likert scale response columns
    likert_columns = survey_data_filtered.columns[5:]

    # Calculating the frequency percentage for each Likert response in each question
    likert_response_counts = survey_data_filtered[likert_columns].apply(pd.Series.value_counts, normalize=True) * 100

    # Merging the question names and the response frequencies into a single DataFrame for plotting
    likert_response_melted = likert_response_counts.transpose().reset_index()
    likert_response_melted = likert_response_melted.melt(id_vars=["index"], var_name="Likert Response", value_name="Frequency Percentage")

    # Renaming the 'index' column to 'Question'
    likert_response_melted.rename(columns={'index': 'Question'}, inplace=True)

    # Set the aesthetic style of the plots
    sns.set_style("whitegrid")

    # Plotting the combined bar chart
    plt.figure(figsize=(15, 8), dpi=500)
    sns.barplot(data=likert_response_melted, x="Likert Response", y="Frequency Percentage", hue="Question", order=['Strongly agree', 'Agree', 'Neither agree nor disagree', 'Disagree', 'Strongly disagree'])
    plt.title(f"Frequency Percentage of Likert Responses per Question (n: {df.shape[0]})")
    plt.ylabel("Frequency Percentage (%)")
    plt.xlabel("Likert Response")
    plt.legend(title='Question', bbox_to_anchor=(0.8, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'./plots/question_freq_percent.png')
    plt.show()
