# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 19:59:42 2020

@author: Kyle Goldberg
"""

# this file contains the source code for a tool that will generate cards for Prelude to Revolution
# the code could be translated fairly easily to another game with a little bit of effort, but the structure
# would remain largely the same.

# will list all of the function definitions followed by the calls

from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd
import textwrap

# creates a finalized image of a single card by placing each individual aspect of the card on top of 
# the background base img. It will dynamically set distances between text so that nothing overlaps
# if there is too much text on the card and issues are happening, make sure to reduce the font size and change the widths
# also will not work on a mac due to hardcoding the location of the FONTS folder
# currently uses ARIAL font for everything, but could be adjusted
# df = your dataframe containing all of the card info
# row_num = the index of the row you want to create an image for
# dir_string = the directory that contains all of the images
def combine_img(df,row_num,dir_string):
    os.chdir(dir_string)
#define each image based portion of the card (i.e. non text portions)
    
#era
    if (df.era[row_num] == 'generic'):
        era = Image.open('generic.png')
    elif (df.era[row_num]=='turmoil'):
        era = Image.open('turmoil.png')
    elif (df.era[row_num]=='war'):
        era = Image.open('war.png')
    elif (df.era[row_num]=='collapse'):
        era = Image.open('collapse.png')
        
#ap_value
    if (df.ap_value[row_num] == 2):
        ap = Image.open('two.png')
    elif (df.ap_value[row_num] == 4):
        ap = Image.open('four.png')
    elif (df.ap_value[row_num] == 6):
        ap = Image.open('six.png')
        
#faction
    if (df.faction[row_num] == 'rev'):
        faction = Image.open('revolutionary.png')
    elif (df.faction[row_num] == 'gov'):
        faction = Image.open('monarchy.png')
    elif (df.faction[row_num] == 'ntl'):
        faction = Image.open('neutral.png')
        
#dice
    if (df.dice[row_num] == 'w'):
        di = Image.open('w.png')
    elif (df.dice[row_num] == 'o'):
        di = Image.open('o.png')
    elif (df.dice[row_num] == 'ud'):
        di = Image.open('ud.png')
    elif (df.dice[row_num] == 'd'):
        di = Image.open('d.png')
    elif (df.dice[row_num] == 'all'):
        di = Image.open('all.png')
    elif (df.dice[row_num] == 'rev'):
        di = Image.open('rev.png')
    elif (df.dice[row_num] == 'gov'):
        di = Image.open('gov.png')
        
#key_per/event
    if (df.type[row_num] == 'kperson'):
        typ = Image.open('key_per.png')
    elif(df.type[row_num] == 'kevent'):
        typ = Image.open('key_eve.png')

# places all of the corresponding images onto the X/Y plane of the card.        
    img1 = Image.open('background.png')
    img1.paste(era, (10,10))
    img1.paste(ap, (12,40))
    img1.paste(faction, (80,10))
    img1.paste(di, (200,10))

#useful later to define the starting point of where the title will be placed
# pad will always represent the distance in the Y direction that will be moved when moving to a new line
    current_h, pad = 100, 12
    if (df.type[row_num] != 'event'):
        img1.paste(typ, (1,80))
        current_h += 20
    
#write all of the longer text onto the card (i.e. anything non-image based)
#title
    draw = ImageDraw.Draw(img1)
    fontsFolder = 'C:/Windows/Fonts'
    #arial bold
    arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arialbd.ttf'), 13)
    txt = df.title[row_num]
    # the line will break after 40 characters, or the closest SPACE before 40 characters if it were going to cut a word in two
    txt = textwrap.wrap(txt,width = 40)
    
# max width of the card
    MAX_W = 263
# this piece ensures that the text is centered
    for i in range(0,len(txt)):
        w, h = draw.textsize(txt[i], font=arialFont)
        draw.text(((MAX_W - w) / 2, current_h), txt[i],fill = 'black', font=arialFont)
        current_h += h + pad

#prereq        
    if df.prereq[row_num] == df.prereq[row_num]:
        draw = ImageDraw.Draw(img1)
        fontsFolder = 'C:/Windows/Fonts'
        #arial bold italic
        arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arialbi.ttf'), 11)
        txt = df.prereq[row_num]
        txt = textwrap.wrap(txt, width = 50)
        pad = 10
        current_h += 20
        for i in range(0,len(txt)):
            w, h = draw.textsize(txt[i], font=arialFont)
            draw.text(((MAX_W - w) / 2, current_h), txt[i],fill = 'black', font=arialFont)
            current_h += h + pad
#text
    draw = ImageDraw.Draw(img1)
    fontsFolder = 'C:/Windows/Fonts'
    #arial
    arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 10)
    txt = df.text[row_num]
    txt = textwrap.wrap(txt,width = 50)
    current_h += 20
    pad = 12
    for i in range(0,len(txt)):
        w, h = draw.textsize(txt[i], font=arialFont)
        draw.text(((MAX_W - w) / 2, current_h), txt[i],fill = 'black', font=arialFont)
        current_h += h + pad
        
    
#flavor
#need the if statement if there is no flavor text or there will be index errors.
# starts at the bottom of the card
    if df.flavor[row_num] == df.flavor[row_num]:
        draw = ImageDraw.Draw(img1)
        fontsFolder = 'C:/Windows/Fonts'
        arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'ariali.ttf'), 8)
        txt = df.flavor[row_num]
        txt = textwrap.wrap(txt, width = 70)
        pad = 10
        #adjust current_h so that the flavor text is close to the bottom of the card
        current_h = 340 - 10*len(txt)
        
        for i in range(0,len(txt)):
            w, h = draw.textsize(txt[i], font=arialFont)
            draw.text(((MAX_W - w) / 2, current_h), txt[i],fill = 'black', font=arialFont)
            current_h += h + pad
#save the image into a new folder, hardcoded in right now, but could easily be pulled into the function call.        
    os.chdir('C:/Users/KG/Desktop/game_imgs/test_imgs')
#adding card num ensures that duplicate cards will both come in
    img1.save(df.title[row_num]+str(df.cardnum[row_num])+'.png')
    
    
# concatenates two images horizontally    
# im1, im2 = Images
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

#concatenates two images vertically
# im1, im2 = Images
def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

#concatenates all of the cards in a source_loc folder into 6 per page to be more easily printed
    #if there are less than 6 cards will just put a background image card in the space the remained would have gone
    
#source_loc = directory with all of the indv card images (result of combine_img function)
#dest_loc = directory the printable pgs will be written to
#base_loc = directory containing the default background image
def printable_pgs(source_loc, dest_loc, base_loc):
    plain_bg = Image.open(base_loc+'/background.png')
    path, dirs, files = next(os.walk(source_loc))
    file_count = len(files)
    for i in range(0,file_count):
        if i%6 == 0:
            os.chdir(source_loc)
            try:
                a = Image.open(os.listdir(source_loc)[i])
            except IndexError:
                a = plain_bg
            try:
                b = Image.open(os.listdir(source_loc)[i+1])
            except IndexError:
                b = plain_bg         
            try:
                c = Image.open(os.listdir(source_loc)[i+2])
            except IndexError:
                c = plain_bg       
            try:
                d = Image.open(os.listdir(source_loc)[i+3])
            except IndexError:
                d = plain_bg       
            try:
                e = Image.open(os.listdir(source_loc)[i+4])
            except IndexError:
                e = plain_bg                      
            try:
                f = Image.open(os.listdir(source_loc)[i+5])
            except IndexError:
                f = plain_bg                    
            

            horiz_img_1 = get_concat_h(get_concat_h(a,b),c)
            horiz_img_2 = get_concat_h(get_concat_h(d,e),f)
            full_img = get_concat_v(horiz_img_1,horiz_img_2)

            
            os.chdir(dest_loc)
            full_img.save('printable_pg'+str(i)+'.png')
            a.close()
            b.close()
            c.close()
            d.close()
            e.close()
            f.close()
    


# read in the table where the data is all stored. modify to wherever your source is
os.chdir('C:/Users/KG/Desktop/game_imgs')
df = pd.read_excel('table.xlsx',sheet_name = 'DB')

#create an image for each card in the data file
for i in range(0,len(df)):
    combine_img(df = df, row_num = i,dir_string = 'C:/Users/KG/Desktop/game_imgs/')

#create 6 per page printable pages
printable_pgs('C:/Users/KG/Desktop/game_imgs/test_imgs','C:/Users/KG/Desktop/game_imgs/printable_pgs','C:/Users/KG/Desktop/game_imgs/')   
