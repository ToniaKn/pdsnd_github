import time
import pandas as pd
import numpy as np
import calendar


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    accepted_cities = ['chicago', 'new york city', 'washington']
    x = True
    while x:
        city = str(input('Enter a city: '))
        x = city.lower() not in accepted_cities
        if x:
            print('Wrong City name - Choose among chicago, new york city and washington')
    accepted_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    y = True
    while y:
        month = str(input('Enter a month: '))
        y = month.lower() not in accepted_months
        if y:
            print('Wrong month - january, february, march, april, may , june or "all" for all months')
    accepted_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    z = True
    while z:
        day = str(input('Enter a day: '))
        z = day.lower() not in accepted_days
        if z:
            print('Wrong day - Give any day of week or "all" for all days')
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


CITY_DATA = {'chicago': pd.read_csv('chicago.csv'),
             'new york city': pd.read_csv('new_york_city.csv'),
             'washington': pd.read_csv('washington.csv')}


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    df = pd.DataFrame(CITY_DATA[city])
    df['Start Time'] =pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['month_abbr'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print('The most common month: ' + str(df['month_abbr'].mode()[0]))
    print('The most common day of week: ' + str(df['day_of_week'].mode()[0]))
    print('The most common start hour: ' + str(df['hour'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('The most commonly used start station: ' + str(df['Start Station'].mode()[0]))
    print('The most commonly used end station: ' + str(df['End Station'].mode()[0]))
    df['Start_End_Station'] = df['Start Station'] + ' --> ' + df['End Station']
    print('The most frequent combination of start station and end station trip: ' + str(df['Start_End_Station'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print('Total travel time: ' + str(df['Trip Duration'].sum()))
    print('Mean travel time: ' + str(df['Trip Duration'].mean()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('Counts of user types:\n' + str(df['User Type'].value_counts()))
    if city != 'washington':
        print('Counts of gender:\n' + str(df['Gender'].value_counts()))
        print('Earliest year of birth: ' + str(int(df['Birth Year'].min())))
        print('Most recent year of birth: ' + str(int(df['Birth Year'].max())))
        print('Most common year of birth: ' + str(int(df['Birth Year'].mode()[0])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data_function(df, city):
    """Displays raw data upon user request - 5 Rows per time"""
    show_5_first = input('\nWould you like to see raw data? Enter yes or no.\n')
    if show_5_first.lower() == 'yes':
        i = 0
        while True:
            if city == 'washington':
                print(df.iloc[i:i+5,:][['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station',
                                        'User Type']])
            else:
                print(df.iloc[i:i + 5, :][['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station',
                                           'User Type','Gender', 'Birth Year']])
            show_more = input('\nWould you like to see more raw data? Enter yes or no.\n')
            if show_more.lower() != 'yes':
                break
            else:
                i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data_function(df,city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
        main()
