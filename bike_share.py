import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv' }


""" using the following lists as an input check """
CITIES = ('all', 'chicago', 'new york', 'washington' )

MONTHS = ('all', 'january', 'february', 'march', 'april', 'may', 'june' )

W_DAYS = ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

y_or_n = ("yes","no")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bike share data.\nnote an input will keep popping up unless it is valid!!!\n')


#Using a while loop to handle invalid inputs

    city = "g"
    while city not in CITIES:
        # get user input for city (chicago, new york city, washington).
        city = str(input("which city you want to see data from chicago, new york, washington?").lower())


    month = "g"
    while month not in MONTHS:
        # get user input for month (all, january, february, ... , june)
        month =str(input('please enter a month (all, january, february, ... , june):').lower())


    day = "g"
    while day not in W_DAYS:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = str(input('please enter a day (all, monday, tuesday, ... sunday):').lower())


    
    return city, month, day



def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # adding a destination column
    df['destination'] = df['Start Station'] + ' to ' + df['End Station']

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

    df.fillna('N.A.')
    return df

def raw_data_input_():
    view_data = ""
    input_error_counter = 3
    while view_data not in y_or_n and input_error_counter > 0:
        view_data = str(input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower())
        input_error_counter -= 1
    if view_data not in y_or_n:
        return y_or_n[-1]
    else:
        return view_data
            
def raw_data(df):
    
    start_loc = 5
    while raw_data_input_() == y_or_n[0]:
        print(df[:start_loc])
        start_loc += 5

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nTimes of Travel Stats...\n')
    start_time = time.time()

    # display the most common month
    m = df['month'].mode()[0]
    print(f"\tthe most common month is {m}.")


    # display the most common day of week
    d = df['day_of_week'].mode()[0]
    print(f"\tthe most common day of week is {d}.")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    pop_hour = int(popular_hour)
    if pop_hour > 12:
        pop_hour -= 12
        print(f"\tthe most common hour is {pop_hour}pm.")
    else:
        print(f"\tthe most common hour is {pop_hour}am.")


    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    

def format_value_counts_(counts:dict, prefix="\t"):
    for key, value in counts.items():
        print(f"{prefix}{key}: {value}")
        

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nStations and Trip Stats...\n')
    start_time = time.time()

    # display most commonly used start station
    ss = df['Start Station'].mode()[0]
    print(f'\tthe most common start station is {ss}.')

    # display most commonly used end station
    es = df['End Station'].mode()[0]
    print(f'\tthe most common end station is {es}.')

    # display most frequent combination of start station and end station trip
    d = df['destination'].mode()[0]
    print(f'\tthe most common destination is {d}.')

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip Duration Stats...\n')
    start_time = time.time()

    # display total travel time
    t = df['Trip Duration'].sum()
    print(f'\tTotal travel time is {t}.')


    # display mean travel time
    a = df['Trip Duration'].mean()
    print(f'\tAverage travel time is {a}.')

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    


def user_stats(df, city):
    """Displays statistics on bikes share users."""

    print('\nUser Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ut = df['User Type'].value_counts().to_dict()
    print("- User Type Counts:")
    format_value_counts_(ut)

    # Display counts of gender
    if city != 'washington':
        g = df['Gender'].value_counts().to_dict()
        print("\n")
        print("'- Gender Counts:")
        format_value_counts_(g)

    # Display earliest, most recent, and most common year of birth
    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print("\n")
        print(f'- Earliest year of birth: {int(earliest_birth)}')
        print(f'- Most recent year of birth: {int(most_recent_birth)}')
        print(f'- Most common year of birth: {int(most_common_birth)}' )

    print("\nThis took %s seconds." % round((time.time() - start_time),4))
    




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        print('-'*40)
        time_stats(df)
        print('-'*40)
        station_stats(df)
        print('-'*40)
        trip_duration_stats(df)
        print('-'*40)
        user_stats(df,city)
        print('-'*40)
        print('-'*40)
        
        restart = ""
        res = 3
        while restart not in y_or_n and res > 0:
            restart = str(input('\nWould you like to run the program again? Enter yes or no.\n').lower())
            res -= 1
            
        if restart == y_or_n[-1] or res <=0:
            break 
    print("="*40)


if __name__ == "__main__":
	main()
