import math
import sys
import os


def if_leap(year):
    '''
    return True if leap year
    '''
    is_leap = True if int(year) % 4 == 0 else False
    return is_leap


def get_day_index(y, m, d):
    '''
    y(year) m(month) d(day)
    if h==0 then Saturday and so on
    '''
    C = math.floor(y/100)
    Y = y % 100
    Gamma = -2*C+math.floor(C/4)
    h = (d + math.floor(26*(m+1)/10) + Y + math.floor(Y/4) + Gamma) % 7
    return h


def make_diary_files(year, is_leap):
    '''
    make diary files.
    Parameters
    __________
    year: <int>
    is_leap: whether leap year or not<bool>
    '''
    os.makedirs(str(year), exist_ok=True)
    day_of_the_week = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thur", "Fri"]
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "Octobar", "November", "December"]
    days_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap:
        days_of_month[1] += 1
    for month_idx, month in enumerate(months):
        days = days_of_month[month_idx]
        if month_idx < 2:
            month_idx_new = 12
            year_new = year - 1
        else:
            month_idx_new = month_idx
            year_new = year
        diary_format = ""
        for d in range(1, days+1):
            day = day_of_the_week[get_day_index(year_new, month_idx_new+1, d)]
            d = str(d).zfill(2)
            diary_format += f"{year},{month},{d},{day}\n\n"

        filename = str(year)+str(month_idx+1).zfill(2)
        f = open(f"{year}/{filename}.txt", 'w')
        f.write(diary_format)
        f.close()


if __name__ == '__main__':
    year = sys.argv[1]
    is_leap = if_leap(year)
    make_diary_files(int(year), is_leap)
