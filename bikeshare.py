#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Bikeshare data analytics project for Udacity programming for data science in Pthon.
## By Ben Waldron November 2021


import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_user_input(request_string, acceptable_answers):
    '''
    Returns (str) keyboard response to question posed in request_string, in lowercase

    Args    (str)  request_string      - message to display requesting input
            (list) acceptable_answers  - accepable answers  (lower case)


    '''
    user_input = ''

    #format complex string for display
    input_request = request_string+'\nOptions: '+str(acceptable_answers).strip('[]')+'\n:'

    while user_input not in acceptable_answers:
        user_input = input(input_request).lower()

    return user_input



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    months_options = ['all','january','february','march','april','may','june','july','august','september','october','november','december']
    days_options = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    print('Hello! Let\'s explore some US bikeshare data!')

    #capture keyboard input.  list of options are the keys of the CITY_DATA dictionary
    city = get_user_input('\nEnter name of city to analyse: ', list(CITY_DATA.keys()))


    # get user input for month (all, january, february, ... , december)
    month = get_user_input('\nWhich month would you like to ananlyse the {} data for (or all) : '.format(city.title()), months_options)


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input('\nWhich day of the week (or all) would you like to analyse: ',days_options)

    print('+'*40,'\nThank you -----> Fetching Bikeshare data for ',city.title())
    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day, month as 1-12
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['start_time_month'] = pd.DatetimeIndex(df['Start Time']).month
    df['start_time_day_of_week'] = pd.DatetimeIndex(df['Start Time']).day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october',
                  'november','december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[(df['start_time_month'] == month)]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[(df['start_time_day_of_week'] == day.title())]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args (dataframe)  df  - filtered bikeshare dataset
    Output - print to screen time summary statistics
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October',
                  'November','December']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    common_month = (df['start_time_month'].mode())[0]


    # display the most common day of week
    common_day = (df['start_time_day_of_week'].mode())[0]

    # display the most common start hour
    df['start_hour'] = pd.DatetimeIndex(df['Start Time']).hour
    most_common_start_hour = (df['start_hour']).mode()[0]


    print('The most common month for travel is: {}.\nThe most common day of the week to travel is: {}. \nThe most common hour of travel is: {}:00 hrs.'.format(months[common_month-1], common_day, most_common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = (df['Start Station'].mode())[0]

    # display most commonly used end station
    common_end_station = (df['End Station'].mode())[0]

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station']+' to '+df['End Station']
    most_common_station_combination = (df['Station Combination']).mode()[0]

    print("The most common starting station is: {}.\nThe most common end station is: {}.\nThe most common trip is: {}.".format(common_start_station,common_end_station,most_common_station_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration_in_seconds = int(df['Trip Duration'].sum())
    total_trip_duration = str(timedelta(seconds=total_trip_duration_in_seconds))

    # display mean travel time
    mean_travel_time_seconds = df['Trip Duration'].mean()
    mean_travel_time = str(timedelta(seconds=round(mean_travel_time_seconds)))

    print('The total travel time in selected period is (in seconds): ',total_trip_duration_in_seconds)
    print('The average travel time per trip is (in seconds): {:.2f}'.format(mean_travel_time_seconds))
    print('\nThe total travel time in selected period is (Days, Hours:Min:Sec): {}\nThe average travel time per trip is (Hours:Min:Sec): {}.'.format(total_trip_duration,mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()

    # Display counts of gender.
    #If no applicable data in dataset, display error message
    try:
        gender_counts = df['Gender'].value_counts()
        print('Breakdown of trip count by User Type:\n',user_type_counts.to_string())

    except:
        print('\nSorry. No gender data in dataset.\n')

    # Display earliest, most recent, and most common year of birth
    #If no applicable data in dataset, display error message
    try:
        earliest_birthyear = round(df['Birth Year'].min(skipna=True))
        latest_birthyear = round(df['Birth Year'].max(skipna=True))
        most_common_birthyear = round(df['Birth Year'].mode()[0])
        print('\nBreakdown of trip count by Gender:\n',gender_counts.to_string())
        print('\nEarliest birth year is: {}.\nLatest birth year is: {}.\nMost common birth year is: {}.'.format(earliest_birthyear,latest_birthyear,most_common_birthyear))

    # If no applicable data in dataset, display error message
    except:
        print('\nSorry.  No Birth year data in dataset.\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    '''Displays raw data in 5 line increments
    Arg (DataFrame) - Data Frame to display

    Output is raw data to console in 5 line increments until user enters "no" or end of data
    '''
    print('\nDisplaying Raw Data\n')

    user_input = get_user_input('Would you like to display 5 lines of raw data?', ['yes','no'])
    row_index = 0

    # display raw data, removing the columns which were added to original data using .drop()
    while user_input != 'no':

    # check that there are enough rows left to display 5 more, then display them
        if (row_index+5) <= df.shape[0]:
            print(df.drop(['start_time_month','start_time_day_of_week','Station Combination','start_hour'], axis=1).iloc[row_index:(row_index+5),:])
            row_index += 5
            user_input = get_user_input('\nWould you like to display another 5 lines?', ['yes','no'])
        else:
            # if less than 5 remaining lines print the remaining lines of the dataframe
            print(df.drop(['start_time_month','start_time_day_of_week','Station Combination','start_hour'], axis=1).iloc[row_index:,:])
            print('\nThere are no more lines of data to display')
            user_input = 'no'  #force drop out of the while loop


    print('\nThankyou\n')
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #if df is empty (likley because month or day is not in dataset, dont attempt analysis)
        if df.shape[0] >= 1:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)
        else:
            print('Sorry. There is no data for {} for {}, for {} (days)'.format(city,month,day).title())

        restart = get_user_input('\nWould you like to start again ?',['yes','no'])
        if restart.lower() != 'yes':
            break

    print('\nThank you for exploring Bikeshare data')
    print('-'*40)
if __name__ == "__main__":
	main()


# In[ ]:
