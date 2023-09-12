import pymysql
def get_quiz_score(request, cnxn, cursor):
    try:
        animal_type1 = request.POST.get('inlineRadioOptions1')
    except:
        animal_type1 = "NULL"
    try:
        tagged_img_id1 = request.POST.get('animalCommonName1')
    except:
        tagged_img_id1 = "NULL"

    try:
        animal_type2 = request.POST.get('inlineRadioOptions2')
    except:
        animal_type2 = "NULL"
    try:
        tagged_img_id2 = request.POST.get('animalCommonName2')
    except:
        tagged_img_id2 = "NULL"

    try:
        animal_type3 = request.POST.get('inlineRadioOptions3')
    except:
        animal_type3 = "NULL"
    try:
        tagged_img_id3 = request.POST.get('animalCommonName3')
    except:
        tagged_img_id3 = "NULL"

    try:
        animal_type4 = request.POST.get('inlineRadioOptions4')
    except:
        animal_type4 = "NULL"
    try:
        tagged_img_id4 = request.POST.get('animalCommonName4')
    except:
        tagged_img_id4 = "NULL"

    try:
        animal_type5 = request.POST.get('inlineRadioOptions5')
    except:
        animal_type5 = "NULL"
    try:
        tagged_img_id5 = request.POST.get('animalCommonName5')
    except:
        tagged_img_id5 = "NULL"

    try:
        animal_type6 = request.POST.get('inlineRadioOptions6')
    except:
        animal_type6 = "NULL"
    try:
        tagged_img_id6 = request.POST.get('animalCommonName6')
    except:
        tagged_img_id6 = "NULL"

    try:
        animal_type7 = request.POST.get('inlineRadioOptions7')
    except:
        animal_type7 = "NULL"
    try:
        tagged_img_id7 = request.POST.get('animalCommonName7')
    except:
        tagged_img_id7 = "NULL"

    try:
        animal_type8 = request.POST.get('inlineRadioOptions8')
    except:
        animal_type8 = "NULL"
    try:
        tagged_img_id8 = request.POST.get('animalCommonName8')
    except:
        tagged_img_id8 = "NULL"

    try:
        animal_type9 = request.POST.get('inlineRadioOptions9')
    except:
        animal_type9 = "NULL"
    try:
        tagged_img_id9 = request.POST.get('animalCommonName9')
    except:
        tagged_img_id9 = "NULL"

    try:
        animal_type10 = request.POST.get('inlineRadioOptions10')
    except:
        animal_type10 = "NULL"
    try:
        tagged_img_id10 = request.POST.get('animalCommonName10')
    except:
        tagged_img_id10 = "NULL"
    numCorrect = 0

    if animal_type1 == "Mammal" and tagged_img_id1 == "Procyon lotor":
        numCorrect += 1
    if animal_type2 == "Mammal" and tagged_img_id2 == "Cardinalis cardinalis":
        numCorrect += 1
    if animal_type3 == "Mammal" and tagged_img_id3 == "Urocyon cinereoargenteus":
        numCorrect += 1
    if animal_type4 == "Mammal" and tagged_img_id4 == "Tamias":
        numCorrect += 1
    if animal_type5 == "Mammal" and tagged_img_id5 == "Sciurus carolinensis":
        numCorrect += 1
    if animal_type6 == "Mammal" and tagged_img_id6 == "Felis catus":
        numCorrect += 1
    if animal_type7 == "Mammal" and tagged_img_id7 == "Urocyon cinereoargenteus":
        numCorrect += 1
    if animal_type8 == "Mammal" and tagged_img_id8 == "Bombycilla cedrorum":
        numCorrect += 1
    if animal_type9 == "Mammal" and tagged_img_id9 == "":
        numCorrect += 1
    if animal_type10 == "Mammal" and tagged_img_id10 == "":
        numCorrect += 1

    print(numCorrect)
    if numCorrect == 9:
        pass
        # SQL Needs to be inserted

    return numCorrect