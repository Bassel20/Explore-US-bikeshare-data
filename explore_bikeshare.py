"""
***************************************************
*********   Author: Bassel Sherif       ***********
******      Date Created: 22-6-2022       *********
*********   Explore US Bike Share data  ***********
***************************************************
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

valid_cities = ['chicago', 'new york city', 'new york', 'washington']
valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_city():
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Choose a city (Chicago - New York City - Washington) \n').lower()
    if (city not in valid_cities):
        print('Invalid city, please try again \n')
        city = get_city()
    return city

def get_month():
    # get user input for month (all, january, february, ... , june)
    month = input('Enter Month (from January to June or type "all"): \n').lower()
    if (month not in valid_months):
        print('Invalid month, please try again \n')
        month = get_month()
    return month

def get_day():
     # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter day of the week (or type "all"): \n').lower()
    if (day not in valid_days):
        print('Invalid day, please try again \n')
        day = get_day()
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_city()
    month = get_month()
    day = get_day()
   
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loading data from csv file into data frame
    df = pd.read_csv(CITY_DATA[city])

    # converting Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # creating new columns for months and days
    # extracting month and day from start time column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filtering by month 
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = valid_months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filtering by day of the week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('Most common day: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print('Most common start hour: {}'.format(df['Hour'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('most common start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\nmost common end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('\nmost common start & end station combo: \n {}'.format(df.groupby(['Start Station','End Station']).size().nlargest(1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {} hours'.format((df['Trip Duration'].sum())/(60*60)))

    # display mean travel time
    print('\nAverage travel time: {} minutes'.format((df['Trip Duration'].mean())/(60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Types of users: \n{} '.format(df['User Type'].value_counts()))

    if(city == 'washington'):
        print('\nGender and Age data is not available for Washington\n')
    else:    
        # Display counts of gender
        print('\nGenders:\n{}'.format(df['Gender'].value_counts()))

        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('\nEarliest birth year: {}\n'.format(earliest))
        print('Most recent birth year: {}\n'.format(most_recent))
        print('Most common birth year: {}\n'.format(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        print('Would you like to see some raw data ?\npress Enter for yes, type "no" otherwise')
        counter = 0
        while (input()!='no'):
            counter += 5
            print(df.head(counter))


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
