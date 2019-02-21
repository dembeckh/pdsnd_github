import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    get_filter = True
    while get_filter:
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()

        if city in ('chicago', 'new york city', 'washington'):
                get_filter = False
        else:
            print("Not a valid city. Please choose between Chicago, New York City or Washington")

    # get user input for month (all, january, february, ... , june)
    get_filter = True
    while get_filter:
        month = input('For which month do you want to see data (January to June)? Type "all" for no filter. ').lower()

        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
                get_filter = False
        else:
            print('Not a valid choice. Choose a month or \'all\' for no filter.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    get_filter = True
    while get_filter:
        day = input('For which day you want to see data (Monday to Sunday)? Type "all" for no filter. ').lower()

        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                get_filter = False
        else:
            print('Not a valid choice. Choose a day or \'all\' for no filter.')
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        df['month'] = df['Start Time'].dt.month
        popular_month = df['month'].mode()[0]
        print('The most popular month was {}.'.format(popular_month))
    else:
        print('The selected month was {}.'.format(month.title()))

    # display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('The most popular day was {}.'.format(popular_day))
    else:
        print('The selected day was {}.'.format(day.title()))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour was {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: {}.'.format(most_start_station))

    # display most commonly used end station
    most_end_station = df['Start Station'].mode()[0]
    print('Most commonly used end station: {}.'.format(most_end_station))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    most_freq_combination = df['Trip'].mode()[0]
    print('Most frequent combination of start station and end station trip: {}.'.format(most_freq_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df['Trip Duration'].sum()/3600)  #total travel time in hours
    print('Total travel time: {} hours'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = (df['Trip Duration'].mean()/60)  #mean travel time in minutes
    print('Mean travel time: {} minutes.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    df.dropna(axis=0) # Deleting rows with NaNs

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print('No gender data available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = int(df['Birth Year'].min())
        print('Earliest year of birth: {}.'.format(earliest_yob))

        most_recent_yob = int(df['Birth Year'].max())
        print('Most recent year of birth: {}.'.format(most_recent_yob))

        most_common_yob = int(df['Birth Year'].mode())
        print('Most common year of birth: {}.'.format(most_common_yob))
    else:
        print('No birth year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(city):
    df = pd.read_csv(CITY_DATA[city])
    row_index = 0
    while True:
        show_raw_data = input('\nWould you like to view individual trip data?'' Enter yes or no.\n').lower()
        if show_raw_data == 'no':
            break
        else:
            print(df.iloc[row_index: row_index+5])
            row_index += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
