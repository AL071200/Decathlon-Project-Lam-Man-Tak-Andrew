import math

import pandas as pd
from datetime import datetime
import openpyxl

df = pd.read_csv(r'C:\Users\Andrew\Downloads\man_hours.csv')
df_copy = df.copy()
df_copy.to_csv(r'C:\Users\Andrew\Downloads\man_hours.csv', index=False)


# Create new column called duration


# Create a new duration column
def convert_to_24(time):
    time_24 = datetime.strptime(time, '%I:%M %p')
    hour = time_24.hour
    minutes = time_24.minute

    min_as_hour = minutes / 60
    return hour + min_as_hour


def time_diff(start_time, end_time):
    return end_time - start_time


# Check if there are any other shifts in the same day and add in if needed


# Create hour and minute column
df_copy['Start'] = df_copy['Start'].apply(convert_to_24)
df_copy['End'] = df_copy['End'].apply(convert_to_24)

# Use the time diff function to calculate the difference in decimal form
#df_copy['Duration'] = df_copy.apply(lambda column: time_diff(column['Start'], column['End']), axis=1)
#df_copy = df_copy.loc[df_copy['Duration'] != 0]

# Employee followed by store duration and position
new_rows = []
for index, row in df_copy.iterrows():
    if row['End'] < row['Start'] or row['End'] == 24:
        # Add a day to the 'Date' column and convert it back to '12-Feb-24' format
        df_copy.loc[index, 'Date'] = pd.to_datetime(row['Date'], format='%d-%b-%y') + pd.DateOffset(days=1)
        duration_b24 = 24 - row['Start']
        duration_a24 = time_diff(0,row['End'])
        duration_a24_floor = math.floor(duration_a24)
        thereof_24 = row['End']- duration_a24_floor
        #Before 24 hour row

        b24_row = pd.DataFrame([row], columns=df_copy.columns)
        b24_row['Duration'] = duration_b24
        #After 24 hour row
        a24_row = pd.DataFrame([row], columns=df_copy.columns)
        a24_row['Start'] = 0
        a24_row['Duration']= duration_a24_floor
        a24_row['Date'] = pd.to_datetime(row['Date']) + pd.DateOffset(days=1)
        #After 24 part thereof
        a24_row_t= pd.DataFrame([row], columns=df_copy.columns)
        a24_row_t['Start'] = duration_a24_floor
        a24_row_t['Duration'] = thereof_24
        a24_row_t['Date'] = pd.to_datetime(row['Date']) + pd.DateOffset(days=1)
        if thereof_24 == 0:
            new_rows.extend([b24_row, a24_row])
        else:

            new_rows.extend([b24_row, a24_row, a24_row_t])

    elif row['End'] == row['Start']:

        df=df.drop(index)
    else:
        hrs_worked = time_diff(row['Start'],row['End'])
        hrs_floor = math.floor(hrs_worked)
        split_time = row['Start'] + hrs_floor
        hr_diff = row['End'] - split_time
        #Integer hour row
        Int_hour_row = pd.DataFrame([row],columns = df_copy.columns)
        Int_hour_row['Duration']= hrs_floor
        #Thereof row
        Thereof_row = pd.DataFrame([row],columns=df_copy.columns)
        Thereof_row['Start'] = split_time
        Thereof_row['Duration']= hr_diff
        if hr_diff == 0:
            new_rows.append(Int_hour_row)
        else:
            new_rows.extend([Int_hour_row, Thereof_row])


# Drop the original rows
# Convert each DataFrame in new_rows to a single row DataFrame
new_rows = [df.reset_index(drop=True) for df in new_rows]


# Create a new DataFrame from the list of new rows
new_df = pd.concat(new_rows, ignore_index=True)
new_df = new_df.drop(columns=['End'])
# Save the new DataFrame to a new CSV file
#Change the name of Start
new_df = new_df.rename(columns={'Start': 'Hour'})
# Convert the 'Date' column to datetime
new_df['Date'] = pd.to_datetime(new_df['Date'], format='%d-%b-%y')

# Format the 'Date' column to 'YYYY-MM-DD', convert it to a string and add '=' prefix
new_df['Date'] = new_df['Date'].dt.strftime('%Y-%m-%d')


#Reorder the columns that are needed
new_df = new_df.reindex(columns=['Employee','Store','Date','Hour','Duration','Position'])
# Save the new DataFrame to a new CSV file
new_df.to_csv(r'C:\Users\Andrew\Downloads\manhour_formatted.csv', index=False)

# Save the new DataFrame to a new CSV file
#new_df.to_csv(r'C:\Users\Andrew\Downloads\test.csv', index=False)
