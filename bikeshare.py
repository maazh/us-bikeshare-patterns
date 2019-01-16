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
    print('-'*80)
    #loop which takes in value for the city and checks for correct input. 
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*80,'\n')
    print('Choose a city \n Use: \n 1 for Chicago \n 2 for Washington \n 3 for New York City')
    while(True):
        city = input('Choose a city: ')
        if (city == '1'):
            city = 'Chicago'
            break
        elif(city == '2'):
            city = 'Washington'
            break
        elif(city == '3'):
            city = 'new york city'
            break
        else:
            print('Invalid input, try again')
    print('-'*80)
    print('You chose:', city)
    print('-'*80)
    city = city.lower()
    
    #These booleans shall be used later in conditonal statements to trigger the correct function for filtering by day or month. 
    filter_by_month = False
    filter_by_day = False
    print('Would you like to filter data by \n Select 1 for Month \n Select 2 for Day \n Select 3 for Month and Days \n Select 4 if you don\'t wish to filter by dates \n')
    #loop which takes in value for the days ands months and checks for correct input.
    while(True):
        filter_by = input('Filter by:')
        if (filter_by == '1'):
            filter_by_month = True
            break
        elif(filter_by == '2'):
            filter_by_day = True
            break
        elif(filter_by == '3'):
            filter_by_day = True
            filter_by_month = True
            break
        elif(filter_by == '4'):
            break
        else:
            print('Invalid input, try again')
    print('-'*80)
    #inital filter values of both days and months set to none
    month = 'none'
    day = 'none'
    
    # days arrays converts the integer input taken by the user to a word to increase user experience. 
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # The initial booleans are used to call respective month and day filter functions which take inputs for the various months and days
    if(filter_by_month & filter_by_day):
        month = filter_by_months()
        day = int(filter_by_days())
        day = days[day]
        #print('You', day)
    elif(filter_by_month):
        #month = input('Month is: ')
        month = filter_by_months()
        day = 'all'
    elif(filter_by_day):
        month = 'all'
        day = int(filter_by_days())
        day = days[day]
    else:
        month = 'all'
        day = 'all'

    # Below print functions show the final inputs/decisions taken by the user before procceding to analyize the results. 
    print('You have decided to view',city.capitalize(), 'Dataset.')
    print(city.capitalize(), 'data shall be fitered by', month.capitalize(), 'month(s) and',day.capitalize(),'day(s)')
    filter_by_month = False
    filter_by_day = False
    return city, month, day


def filter_by_days():
    """
    Asks user to specify a day to analyze.

    Returns:
        (str) day - Integer value of the day of week to filter by.
    """
    print('Choose a Day: ' + "\n" 
          + '1 for Monday' + '\n'
          + '2 for Tuesday' + '\n'
          + '3 for Wednesday' + '\n'
          + '4 for Thursday' + '\n'
          + '5 for Friday' + '\n'
          + '6 for Saturday' + '\n'
          + '7 for Sunday' + '\n')
    #loop for taking in input and for checking for right input
    while(True):
        filter_days = 'none'
        try:
            filter_days = int(input('Day is: '))
        except:
            print('Error! Please choose a correct number')
        
        if(type(filter_days) is int and filter_days > 0 and filter_days < 8):
            filter_days = filter_days -1
            break
        else:
            print('Please choose values specified')
    
    print('You chose:', filter_days+1)
    print('-'*80)
    return str(filter_days)


def filter_by_months():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) day - String value of the month to filter by.
    """
    print('Choose a month: ' + "\n" 
          + '1 for January' + '\n'
          + '2 for Feburary' + '\n'
          + '3 for March' + '\n'
          + '4 for April' + '\n'
          + '5 for May' + '\n'
          + '6 for June' + '\n')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_str = 'all'
    while(True):
        filter_month = 'none'
        try:
            filter_month = int(input('Month is: '))
        except:
            print('Error! Please choose a correct number')
        
        if(type(filter_month) is int and filter_month > 0 and filter_month < 7):
            filter_month = filter_month -1
            month_str = months[filter_month]
            break
        elif(type(filter_month) is int and filter_month > 6 and filter_month < 13):
            print('We apologize, but we only have data for the first six months. Try again!')
        else:
            print('Please choose from values specified.')
    print('You chose:', month_str)
    print('-'*80)
    return month_str


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
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    print('-'*80)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    comman_month = df['month'].mode()[0]
    print('The most comman month is: ',comman_month)
    
    # display the most common day of week
    comman_day = df['day_of_week'].mode()[0]
    print('The most comman day of week is: ',comman_day)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    comman_hour = df['hour'].mode()[0]
    print('The most comman hour is: ',comman_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    start_time = time.time()

    # display most commonly used start station
    comman_startstation = df['Start Station'].mode()[0]
    print('The most comman start station is: ',comman_startstation)
    
    # display most commonly used end station
    comman_endstation = df['End Station'].mode()[0]
    print('The most comman end station is: ',comman_endstation)

    # display most frequent combination of start station and end station trip
    df['Start and End station'] = df['Start Station'] + ' ,' + df['End Station']
    comman_all = df['Start and End station'].mode()[0]
    print('Comman combination of start and end station is:', comman_all)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = sum(df['Trip Duration'])
    #print('Total trip duration is',total_duration)
    #conversion to min,sec,hour and day
    m, s = divmod(total_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('Total trip duration is',d,'Days',h,'Hours',m,'minutes',s,'seconds')

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    #print('Total mean duration is',mean_duration)
    #conversion into day,hour,min,sec
    min, sec = divmod(mean_duration, 60)
    hr, min = divmod(min, 60)
    day, hr = divmod(hr, 24)
    print('Total mean duration is',day,'Days',hr,'Hours',min,'minutes',sec,'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types include:')
    print(user_types,'\n')
    
    #Since Washington doesnt have the below values to analyize, a conditional statments acts as a check
    if(city != 'washington'):
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('Gender count:')
        print(gender,'\n')

        # Display earliest, most recent, and most common year of birth
        recent_yob = df['Birth Year'].max()
        earliest_yob = df['Birth Year'].min()
        comman_yob = df['Birth Year'].mode()
        
        #typecast to int allows rounding off year values
        print('Recent Year of Birth:', int(recent_yob))
        print('Earliest Year of Birth:', int(earliest_yob))
        print('Comman Year of Birth:', int(comman_yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def indv_user_stats(df, city):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating Individual User Stats...\n')
    start_time = time.time()
    count = 0
    for index, row in df.iterrows():
        #ask serves as a boolean to whether show next 5 user records or not
        ask = '1'
        #after eveny 5th iteration, prompt user if they want to see more records
        if(count % 5 == 0 ):
            
            ask = input('Would you like to see the Individual User Stats? \n Press \n 0 for No,\n 1 for seeing 5 records at a time \n')

        if(ask == '1'):
                if(city == 'washington'):
                    print( df.loc[index,['User Type', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station']])
                    print('-'*50)
                else:
                    print( df.loc[index,['User Type', 'Gender', 'Birth Year', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station']])
                    print('-'*50)
        else:
            break
        count = count + 1
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def main():
    '''The main function where all the anaylisis functions are called. 
        Returns:
            (object) Dataframe - This is only for independent access of data/analyized data via commands for the programmer/checker. 
    '''
    datas = 'null'
    while True:
        city, month, day = get_filters()
        datas = df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        indv_user_stats(df, city)
        

        restart = input('\nWould you like to restart? \n Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    return datas


if __name__ == "__main__":
    dt = main()