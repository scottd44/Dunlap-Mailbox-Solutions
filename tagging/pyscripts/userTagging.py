from random import randint

import pymysql

def get_user_data(cnxn, cursor, user_uid):
    cursor.execute(f'SELECT Tagger_Name, Level, Disabled_Date from `wildlife-tagging`.Tagger where UUID="{user_uid}"')

    result = cursor.fetchall()[0]
    user_name, user_level = result[0].replace(u'\xa0', ' '), result[1].replace(u'\xa0', ' ')
    print('hello')
    print(result)

    return result, user_name, user_level

def generate_random_image(request, cnxn, cursor, user_uid):
    if request.POST:

        if request.POST.get('animal_present') == 'on':
            animal_present = True
        else:
            animal_present = False

        try:
            animal_type = request.POST.get('inlineRadioOptions')
        except:
            animal_type = "NULL"

        try:
            animal_comment = request.POST.get('optional_comment')
        except:
            animal_comment = "NULL"

        try:
            tagged_img_id = request.POST.get('img_id')
        except:
            tagged_img_id = "NULL"

        try:
            sql = f"""
            INSERT INTO Tag_Info (Tagged_Date, Tagger_UUID, Image_ID, Animal_Present, Animal_Type, Animal_Comment)
            VALUES (
            '{date.today()}',
            '{user_uid}',
            '{tagged_img_id}',
            '{animal_present}',
            '{animal_type}',
            '{animal_comment}'
            )
            """

            cursor.execute(sql)
            cnxn.commit()
        except Exception as e:
            print(e)

    cursor.execute(f"SELECT Image_ID FROM Tag_Info where Tagger_UUID = '{user_uid}'")
    old_tagged_images = tuple([i[0] for i in cursor.fetchall()])

    if len(old_tagged_images) > 1:
        print(f"SELECT Image_ID, Location FROM Image where Image_ID not in {old_tagged_images}")
        cursor.execute(f"SELECT Image_ID, Location FROM Image where Image_ID not in {old_tagged_images}")
    else:
        cursor.execute(f"SELECT Image_ID, Location FROM Image")

    # Change logic in future
    image_list = [i for i in cursor.fetchall()]

    rand_image = image_list[randint(0, len(image_list)-1)]
    rand_img_id, rand_image_loc = rand_image[0], rand_image[1]

    return rand_img_id, rand_image_loc