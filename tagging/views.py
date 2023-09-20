from django.shortcuts import render, redirect
import boto3
#from django.http import HttpResponse
from django.contrib import messages
import pymysql
from random import random, randint
from datetime import date, datetime, timedelta
from django.utils import timezone
import pandas as pd
import numpy as np
import pytz
#import numpy as np

## File Imports
from atlwildin import settings

from tagging.pyscripts.userTagging import *
from tagging.pyscripts.userLevelUpgrade import *



# Initialising database,auth and firebase for further use



def signIn(request):
    return render(request, "tagging/dashboard.html")


def home(request):
    return render(request, "tagging/homepage.html")


def postsignIn(request):

        #return render(request, "tagging/homepage.html", {"email": email})
        return user_dashboard(request)


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "tagging/login.html")


def view_user_data(request):
    return render(request, "tagging/view_user_data.html")

def user_dashboard(request):
    
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']
    cnxn, cursor = mysqlconnect()

    try:
        cursor.execute(f'SELECT Tagger_Name, Level from `wildlife-tagging`.Tagger where UUID="{user_uid}"')
        result = cursor.fetchall()[0]
        user_name, user_level = result[0].replace(u'\xa0', ' '), result[1].replace(u'\xa0', ' ')
        user_name, user_org = result[0].replace(u'\xa0', ' '), result[1].replace(u'\xa0', ' ')
        request.session['userType'] = "Tagger"
    except:
        cursor.execute(f'SELECT Researcher_Name from `wildlife-tagging`.Researcher where UUID="{user_uid}"')
        user_name = cursor.fetchone()[0].replace(u'\xa0', ' ')
        request.session['userType'] = "Researcher"
    lb_df = generate_leaderboard(user_uid)
    user_stats = get_current_user_statistics(user_uid)
    # cursor.execute(f"""SELECT COUNT(Tag_ID)
    #             FROM `wildlife-tagging`.Tag_Info
    #             WHERE Tagged_Date = curdate()
    #             AND 
    #             (SELECT Organization 
    #             FROM `wildlife-tagging`.Tagger
    #             WHERE UUID = Tagger_UUID) = '{user_org}'""")
    cursor.execute(f'SELECT Count(Image_ID) FROM Image')
    num_images = cursor.fetchall()[0][0]

    if request.session['userType'] == "Tagger":
        return render(request, "tagging/dashboard.html", {"lb_df": lb_df,"num_users": len(lb_df),
                                                        "user_name": user_name,
                                                        "user_stats": user_stats,"num_images":num_images})
    else:
        return render(request, "tagging/researcher_dashboard.html", {"lb_df": lb_df,"num_users": len(lb_df),
                                                        "user_name": user_name,
                                                        "user_stats": user_stats,"num_images":num_images})

        

def user_tagging(request):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']
    cnxn, cursor = mysqlconnect()

    result, user_name, user_level = get_user_data(cnxn, cursor, user_uid)
    disabled_date = result[2]

    if (disabled_date != 0 and disabled_date is not None and disabled_date > datetime.now()):
        est = pytz.timezone('US/Eastern')
        fmt = '%Y-%m-%d %H:%M:%S'
        messages.info(request, "Your account has been temporarily disabled until " + str(disabled_date.astimezone(est).strftime(fmt))
        + ". Please contact your researcher.")
        return redirect('/dashboard/')

    rand_img_id, rand_image_loc = generate_random_image(request, cnxn, cursor, user_uid)

    # Get user stats
    user_stats = get_current_user_statistics(user_uid)

    # Set questions based on levels
    isAdvanced = 0
    if user_level == "Advanced":
        isAdvanced = 1

    # Get list of animals

    animal_info_df = pd.read_sql("SELECT Animal_Common_Names, Animal_Scientific_Name FROM Animal", con=cnxn)

    return render(request, "tagging/tagging.html", {"tag_image": rand_image_loc,
                                                    "tag_image_id":rand_img_id,
                                                    "user_name": user_name,
                                                    "user_stats": user_stats,
                                                    "isAdvanced": isAdvanced,
                                                    "animal_info_df": animal_info_df})

def user_leaderboards(request):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']

    cnxn, cursor = mysqlconnect()

    cursor.execute(f'SELECT Tagger_Name, Level from `wildlife-tagging`.Tagger where UUID="{user_uid}"')

    result = cursor.fetchall()[0]
    user_name, user_level = result[0].replace(u'\xa0', ' '), result[1].replace(u'\xa0', ' ')

    # Get leaderboard
    lb_df = generate_leaderboard(user_uid)
    # Get user stats
    user_stats = get_current_user_statistics(user_uid)

    return render(request, "tagging/leaderboard.html", {"lb_df": lb_df,
                                                        "user_name": user_name,
                                                        "user_stats": user_stats})


def user_list(request):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']

    cnxn, cursor = mysqlconnect()

    cursor.execute(f'SELECT Researcher_Name, Organization from `wildlife-tagging`.Researcher where UUID="{user_uid}"')

    result = cursor.fetchall()[0]
    user_name, user_org = result[0].replace(u'\xa0', ' '), result[1].replace(u'\xa0', ' ')

    # Get leaderboard
    lb_df = generate_users(user_org)
    # Get user stats
    cursor.execute(f"""SELECT COUNT(Tag_ID)
                FROM `wildlife-tagging`.Tag_Info
                WHERE Tagged_Date = curdate()
                AND 
                (SELECT Organization 
                FROM `wildlife-tagging`.Tagger
                WHERE UUID = Tagger_UUID) = '{user_org}'""")

    total_tagged = cursor.fetchall()[0][0]

    return render(request, "tagging/users_list.html", {"lb_df": lb_df,
                                                        "num_users": len(lb_df),
                                                        "user_name": user_name,
                                                        "user_org": user_org,
                                                        "total_tagged": total_tagged})

def user_profile(request):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']

    cnxn, cursor = mysqlconnect()

    cursor.execute(f'SELECT Tagger_Name, Level, Organization, Email_Address from `wildlife-tagging`.Tagger where UUID="{user_uid}"')

    result = cursor.fetchall()[0]
    user_name, user_level, user_organization, user_email = result[0].replace(u'\xa0', ' '), result[1].replace(u'\xa0', ' '), result[2].replace(u'\xa0', ' '), result[3].replace(u'\xa0', ' ')

    # Get user stats
    user_stats = get_current_user_statistics(user_uid)

    return render(request, "tagging/profile.html", {"user_name": user_name,
                                                    "user_level": user_level,
                                                    "user_organization": user_organization,
                                                    "user_email": user_email,
                                                    "user_stats": user_stats})

def wildlife_data(request):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']
    cnxn, cursor = mysqlconnect()

    cursor.execute(
        f'SELECT Researcher_Name from `wildlife-tagging`.Researcher where UUID="{user_uid}"')

    result = cursor.fetchall()[0]
    username = result[0].replace(u'\xa0', ' ')

    test_start = datetime(2021, 5, 8)
    test_end = datetime.today()
    cis = createImageSummary(test_start, test_end)

    return render(request, "tagging/researcher_wildlife_data.html", {"user_name": username,
                                                                     "lb_df": cis})

def quiz(request):


    # Get user stats

    # Set questions based on levels
    isAdvanced = 1
    # Get list of animals

    


    return render(request, "tagging/quiz.html")


## Utility Functions
def mysqlconnect():
    # To connect MySQL database
    try:
        cnxn = pymysql.connect(
            host='wildlife-tagging.c1df6qqn09wc.us-east-2.rds.amazonaws.com',
            user='admin',
            password = "TaggingIsFun!1128",
            port=3306,
            db='wildlife-tagging',
            )
        print(cnxn)
        cursor = cnxn.cursor()
        print(cursor)
    except Exception as e:
        print("MYSQL ERROR!!")
        print(e)
        return e, e

    return cnxn, cursor


def get_current_user_statistics(user_uid):
    # user_uid = "apovkYcqoQPFwzvojf8u7CqdZ2s1"
    cnxn, cursor = mysqlconnect()

    total_img_tagged = 0
    today_img_tagged = 0
    leaderboard_rank = "N.A."
    target_status = "Incomplete"
    user_level = "Beginner"

    try:
        cursor.execute(f"""
        SELECT * FROM 
            (SELECT Tagger_UUID, COUNT(*) as Total_Tagged, RANK()
            OVER ( order by COUNT(*) desc ) Leaderboard_Rank 
            FROM Tag_Info 
            GROUP BY Tagger_UUID) as temp
        WHERE Tagger_UUID = '{user_uid}'
        """)

        result = [i for i in cursor.fetchone()]
        total_img_tagged, leaderboard_rank = result[1], result[2]
    except Exception as e:
        print(e)

    try:
        cursor.execute(f"""
        SELECT Tagger_UUID, COUNT(*) as Today_Tagged FROM Tag_Info 
        WHERE Tagged_Date = '{date.today()}' and Tagger_UUID = '{user_uid}' 
        GROUP BY Tagger_UUID
        """)

        result = [i for i in cursor.fetchone()]
        today_img_tagged = result[1]
    except Exception as e:
        print(e)

    try:
        cursor.execute(f"SELECT Level FROM Tagger WHERE UUID='{user_uid}'")

        result = [i for i in cursor.fetchone()]
        user_level = result[0]
    except Exception as e:
        print(e)

    return {
        "total_img_tagged": total_img_tagged,
        "today_img_tagged": today_img_tagged,
        "leaderboard_rank": leaderboard_rank,
        "target_status": target_status,
        "user_level": user_level,
    }

def generate_leaderboard(user_uid):
    cnxn, cursor = mysqlconnect()
    lb_df = pd.read_sql(f"""
            SELECT * FROM Tagger Left Outer Join 
                (SELECT Tagger_UUID, MAX(Tagged_Date) as Last_Active, COUNT(*) as Total_Tagged, RANK()
                OVER ( order by COUNT(*) desc ) Leaderboard_Rank 
                FROM Tag_Info 
                GROUP BY Tagger_UUID) as temp
                on UUID=Tagger_UUID
            ORDER BY -Leaderboard_Rank DESC
            LIMIT 25
            """, con=cnxn)

    lb_df.drop(['Tagger_UUID'], axis=1, inplace=True)
    lb_df['Last_Active'] = (pd.to_datetime(lb_df['Last_Active'])).dt.strftime("%b %d, %Y")
    #lb_df['Total_Tagged'] = lb_df['Total_Tagged'].
    lb_df['Last_Active'].fillna("-", inplace=True)
    lb_df['Level'].fillna("-", inplace=True)
    lb_df['Organization'].fillna("-", inplace=True)
    lb_df.fillna(0, inplace=True)

    return lb_df

def generate_users(org):
    cnxn, cursor = mysqlconnect()
    lb_df = pd.read_sql(f"""
                SELECT * FROM `wildlife-tagging`.Tagger Left Outer Join 
                (SELECT Tagger_UUID, MAX(Tagged_Date) as Last_Active, COUNT(*) as Total_Tagged
                FROM `wildlife-tagging`.Tag_Info 
                GROUP BY Tagger_UUID) as temp
                on UUID=Tagger_UUID
                WHERE Organization="{org}"
                ORDER BY case when Last_Active is null then 1 else 0 end, -Last_Active
                """, con=cnxn)

    lb_df.drop(['Tagger_UUID'], axis=1, inplace=True)
    lb_df['Last_Active'] = (pd.to_datetime(lb_df['Last_Active'])).dt.strftime("%b %d, %Y")
    lb_df['Last_Active'].fillna("-", inplace=True)
    lb_df['Level'].fillna("-", inplace=True)
    lb_df['Organization'].fillna("-", inplace=True)
    lb_df.fillna(0, inplace=True)
    is_disabled = []

    lb_df['Disabled_Date'] = lb_df['Disabled_Date'].replace(0, datetime.utcnow() - timedelta(days=1))
    lb_df['Disabled_Date'] = pd.to_datetime(lb_df['Disabled_Date']).dt.tz_localize('UTC')
    est = pytz.timezone('US/Eastern')
    fmt = '%Y-%m-%d %H:%M:%S'
    est_list = []



    for disabled_date in lb_df['Disabled_Date']:
        if disabled_date == 0:
            is_disabled.append(False)
        elif disabled_date > timezone.now():
            is_disabled.append(True)
            est_list.append(disabled_date.astimezone(est).strftime(fmt))
        else:
            is_disabled.append(False)
            est_list.append(disabled_date.astimezone(est).strftime(fmt))

    lb_df['Disabled_Date'] = est_list
    lb_df['is_disabled'] = is_disabled
    return lb_df

def disable_user(request, id):
    cnxn, cursor = mysqlconnect()

    cursor.execute(f'UPDATE Tagger SET Disabled_Date = DATE_ADD(NOW(), INTERVAL 4 HOUR) WHERE UUID="{id}"')
    cnxn.commit()

    return redirect('/userlist/')

def modify_images(request):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']
    cnxn, cursor = mysqlconnect()

    cursor.execute(f'SELECT Researcher_Name from `wildlife-tagging`.Researcher where UUID="{user_uid}"')

    result = cursor.fetchall()[0]
    user_name = result[0].replace(u'\xa0', ' ')
    return render(request, "tagging/modify.html", {"user_name": user_name})

def upload_interface(request, msg=""):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']
    cnxn, cursor = mysqlconnect()

    cursor.execute(f'SELECT Researcher_Name from `wildlife-tagging`.Researcher where UUID="{user_uid}"')

    result = cursor.fetchall()[0]
    user_name = result[0].replace(u'\xa0', ' ')

    return render(request, "tagging/uploading.html", {"message": msg, "user_name": user_name})

def upload_file(request):
    try:
        user_uid = request.session['uid']
    except:
        return signIn(request)

    user_uid = request.session['uid']
    cnxn, cursor = mysqlconnect()

    files = request.FILES.getlist('myfile', False)
    if not files:
        return upload_interface(request, "No File Uploaded!")
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
    for file in files:
        ext = file.name.split('.')[1]
        bucket.put_object(Key=file.name, Body=file, ContentType = 'image/' + ext)
        name = file.name.replace(' ', '+')
        url = "https://animalsbucket.s3.us-east-2.amazonaws.com/" + name

        cursor.execute(f'''
        INSERT INTO `wildlife-tagging`.Image (UploadDate, CaptureDate, ResearcherUUID, Location, Priority)
        VALUES (NOW(), NOW(), "{user_uid}", "{url}", Priority);
        ''')
        cnxn.commit()

    return upload_interface(request, "File(s) Uploaded Successfully")


def add_IDS(tag_info_df):
    tag_info_df['Animal_ID'] = np.random.randint(1, 3, tag_info_df.shape[0])
    return tag_info_df


def pull_sql_data():
    cnxn, cursor = mysqlconnect()

    query = 'SELECT * FROM Image'
    image_df = pd.read_sql(query, cnxn)
    query = 'SELECT * FROM Tag_Info'
    tag_info_df = pd.read_sql(query, cnxn)
    query = 'SELECT * FROM Animal'
    animal_df = pd.read_sql(query, cnxn)
    query = 'SELECT * FROM Researcher'
    researcher_df = pd.read_sql(query, cnxn)

    # Minor adjustments
    image_df = image_df.rename(columns={'ImageID': 'Image_ID'})

    # Animal_ID 0 has multiple rows
    animal_df = animal_df.drop_duplicates(subset='AnimalID')

    # # Just for testing, should be unnecessary when animal_id column is populated
    # tag_info_df = add_IDS(tag_info_df)

    return image_df, tag_info_df, animal_df, researcher_df


def join_tag_img(tag_info_df, image_df):
    # Convert date columns to datetime objects
    image_df['UploadDate'] = pd.to_datetime(image_df['UploadDate'])
    image_df['CaptureDate'] = pd.to_datetime(image_df['CaptureDate'])
    tag_info_df['Tagged_Date'] = pd.to_datetime(tag_info_df['Tagged_Date'])

    # Join both dataframes based on the Image_ID
    tag_info_df['Image_ID'] = tag_info_df['Image_ID'].astype('int64')
    joined_df = image_df.join(tag_info_df.set_index('Image_ID'), on='Image_ID')
    return joined_df


def mostCommon(df):
    counts = df.value_counts()
    if len(counts) > 0:
        return counts.idxmax()
    return None


def secondMostCommon(df):
    counts = df.value_counts()
    if len(counts) > 1:
        return counts.index[1]
    return None


def createImageSummary(startDate, endDate):
    image_df, tag_info_df, animal_df, researcher_df = pull_sql_data()
    df = join_tag_img(tag_info_df, image_df)

    # Filtering out dates that are out of range
    df = df[(df['UploadDate'] >= startDate) & (df['UploadDate'] <= endDate)]

    # Mapping ids to names from other dfs
    df['Common_Name'] = df.Animal_ID.map(animal_df.set_index('AnimalID').Animal_Common_Names)
    df['Scientific_Name'] = df.Animal_ID.map(animal_df.set_index('AnimalID').Animal_Scientific_Name)
    df['Common_Name'] = df['Common_Name'].str.split(",").str[0]
    df['Researcher_Name'] = df.ResearcherUUID.map(researcher_df.set_index('UUID').Researcher_Name)

    # Renaming Columns
    df['Tag_Count'] = df['Tag_ID']
    df['Most_Tagged_Animal'] = df['Common_Name']
    df['Second_Most_Tagged_Animal'] = df['Common_Name']
    df['Most_Tagged_Type'] = df['Animal_Type']
    df['Second_Most_Tagged_Type'] = df['Animal_Type']
    df['Animal_Present'] = (df['Animal_Present'] == "True").astype(int)

    groups = df.groupby('Image_ID')
    groups = groups.agg({
        'UploadDate': np.max,
        'CaptureDate': np.max,
        'Researcher_Name': np.max,
        'Location': np.max,
        'Tag_Count': pd.Series.count,
        'Animal_Present': np.average,  # Returns percentage of true responses
        'Most_Tagged_Type': mostCommon,
        'Second_Most_Tagged_Type': secondMostCommon,
        'Most_Tagged_Animal': mostCommon,
        'Second_Most_Tagged_Animal': secondMostCommon,
        'Scientific_Name': mostCommon,
    })
    return groups.apply(lambda a: a[:])