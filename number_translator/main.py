# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 21:45:17 2021

@author: SmashinFries
"""
import sys, random

from PyQt5.uic import loadUi

from PyQt5.QtWidgets import (QApplication, QMainWindow)

h_num = {0:'ゼロ', 1:'いち', 2:'に', 3:'さん', 4:'よん', 5:'ご', 6:'ろく', 7:'なな', 8:'はち', 9:'きゅう'}
h_num_plus = {10:'じゅう', 100:'ひゃく', 1000:'せん', 10000:'まん'}
h_num_spc = {300:'さんびゃく', 600:'ろっぴゃく', 800:'はっぴゃく', 3000:'さんぜん', 8000:'はっせん'}

k_num = {'いち':'一', 'に':'ニ', 'さん':'三', 'よん':'四', 'ご':'五', 'ろく':'六', 'なな':'七', 'はち':'八', 'きゅう':'九', 'じゅう':'十', 'ひゃく':'百', 'せん':'千', 'まん':'万', 'さんびゃく':'三百' , 'ろっぴゃく':'六百' , 'はっぴゃく':'八百', 'さんぜん':'三千', 'はっせん':'八千'}

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("ui/main_window.ui", self)
        self.setWindowTitle("Number Translator")
        self.btn_convert.clicked.connect(self.action)
        self.btn_random.clicked.connect(self.rand)
        
    def action(self):
        text = self.userInput.text()
        h_results, k_results = converter(text)
        
        self.lbl_hir.setText(h_results)
        self.lbl_kj.setText(k_results)
    
    def rand(self):
        rand_num = str(random.randint(0, 9999999))
        text = self.userInput.setText(rand_num)
        h_results, k_results = converter(text)
        
        self.lbl_hir.setText(h_results)
        self.lbl_kj.setText(k_results)


class Conversion:
    def one(num):
        """1"""
        one_out = ""
        # Iterate through each jpn number
        for key, value in h_num.items():
            # if num matches key then add to the output
            if int(num) == key:
                one_out = value
        return(one_out)
        
    def two(num, cut2=0):
        """10"""
        two_out = ""
        temp2 = []
        
        if int(cut2) > 0:
            num = str(cut2)
        # check if first index is 1
        print("Num before loops(2):", num)
        if int(num[0]) == 1:
            two_out = h_num_plus[10]
            temp2.append(h_num_plus[10])
            
        # Grabs correct translation if 20+
        for key, value in h_num.items():
            # find a match for the first index other than 1
            if int(num[0]) == key and key > 1:
                # add the value and then the translation of 10
                two_out = value + h_num_plus[10] 
                temp2.append(value)
                temp2.append(h_num_plus[10])
        
        for key, value in h_num.items():
            if int(num[1]) == key and key > 0:
                two_out += value 
                temp2.append(value) 
        return(two_out, temp2)
    
    def three(num, cut3=0):
        """100"""
        three_out = ""
        temp3 = []
        if int(cut3) > 0:
            num = str(cut3)
        print("num before loops(3):", num)
        # Loop to search for any special translations for first index
        special = [3,6,8]
        for i in special:
            if int(num[0]) == i:
                # Multiply by 100 so that it can match the dict key
                i =  i*100
                three_out = h_num_spc[i]
                temp3.append(h_num_spc[i])
        
        # check if first index is 1
        if int(num[0]) == 1:
            three_out = h_num_plus[100]
            temp3.append(h_num_plus[100])
            
        # Grabs correct translation if first index is 2+
        for key, value in h_num.items(): 
            if int(num[0]) == key and key > 1 and key !=3 and key !=6 and key !=8:
                three_out = value + h_num_plus[100]
                temp3.append(value)
                temp3.append(h_num_plus[100])
        
        cut3 = num[1:]
        two_out, temp2 = Conversion.two(num, cut3)
        three_out += two_out
        temp3 += temp2
        return(three_out, temp3)
    
    def four(num, cut4=0):
        """1,000"""
        four_out = ""
        temp4 = []
        # Same as the three function
        
        if int(cut4) > 0:
            num = str(cut4)
        print("Num before loops(4):", num)
        special = [3,8]
        for i in special:
            if int(num[0]) == i:
                i = i*1000
                four_out = h_num_spc[i]
                temp4.append(h_num_spc[i])
            
        if int(num[0]) == 1:
            four_out = h_num_plus[1000]
            temp4.append(h_num_plus[1000])
        
        for key, value in h_num.items():
            if int(num[0]) == key and key != 3 and key != 8 and key != 1:
                four_out = value + h_num_plus[1000]
                temp4.append(value)
                temp4.append(h_num_plus[1000])
        
        cut4 = num[1:]
        three_out, temp3 = Conversion.three(num, cut4)
        #print("this is three_out!", three_out)
        four_out += three_out
        temp4 += temp3
        return(four_out, temp4)
    
    def five(num, cut5=0):
        """10,000"""
        # No specials this time!
        five_out = ""
        temp5 = []
        
        if int(cut5) > 0:
            num = str(cut5)
        print("Num before loops(5):", num)
        for key, value in h_num.items():
            if int(num[0]) == key:
                five_out = value + h_num_plus[10000]
                temp5.append(value)
                temp5.append(h_num_plus[10000])
        
        cut5 = num[1:]
        four_out, temp4 = Conversion.four(num, cut5)
        five_out += four_out
        temp5 += temp4
        return(five_out, temp5)
    
    def six(num, cut7=0):
        """100,000"""
        six_out = ""
        temp6 = []
        cut65 = num[:2]
        cut6 = num[2:]
        
        if int(cut7) > 0:
            num = cut7
            cut65 = num[:2]
            cut6 = num[2:]
        print("Num before loops(6):", num)
        # convert the first set of 10 and add 'man'
        two_out, temp2 = Conversion.two(cut65)
        six_out = two_out + h_num_plus[10000]
        temp6 += temp2
        temp6.append(h_num_plus[10000])
        
        # finish the string with four()
        four_out, temp4 = Conversion.four(num, cut6)
        six_out += four_out
        temp6 += temp4
        return(six_out, temp6)
    
    def seven(num):
        """1,000,000"""
        seven_out = ""
        temp7 = []
        cut75 = num[:1]
        cut7 = num[1:]
        if int(cut75) == 1:
            seven_out = h_num_plus[100]
            temp7.append(h_num_plus[100])
            
        for key, value in h_num.items():
            if int(cut75) == key and key > 1:
                seven_out = value + h_num_plus[100]
                temp7.append(value)
                temp7.append(h_num_plus[100])
        six_out, temp6 = Conversion.six(num, cut7)
        seven_out += six_out
        temp7 += temp6
        return(seven_out, temp7)
    
def converter(num):
    """Converts the number into Hiragana"""
    
    # Get the length of number (as a string)
    length = len(num)
    kanji_out =''
    # Create output variable for after conversion
    hir_out = ""
    
    ### Directions based on length of number
    # 0-9 #
    
    if num[0] == '0':
        # Got lazy and decided to make any beginning zeroes return an error
        # May change this once I get to QoL updates
        hir_out = "Only zero starts with 0!"
        kanji_out = "\\0-0/"
    else:
        if length == 1:
            hir_out = Conversion.one(num)
            kanji_out = k_num[hir_out]
        
        # 10-99 #
        if length == 2:
            hir_out, temp2 = Conversion.two(num)
            for i in temp2:
                kanji_out += k_num[i]
        
        # 100-999 #
        if length == 3:
            hir_out, temp3 = Conversion.three(num)
            for i in temp3:
                kanji_out += k_num[i]
        
        # 1000-9999 #    
        if length == 4:
            hir_out, temp4 = Conversion.four(num)
            for i in temp4:
                kanji_out += k_num[i]
                
        if length == 5:
            hir_out, temp5 = Conversion.five(num)
            for i in temp5:
                kanji_out += k_num[i]
        
        if length == 6:
            hir_out, temp6 = Conversion.six(num)
            for i in temp6:
                kanji_out += k_num[i]
        
        if length == 7:
            hir_out, temp6 = Conversion.seven(num)
            for i in temp6:
                kanji_out += k_num[i]
            pass
    
    return(hir_out, kanji_out)

def tip():
    """Explain how the number translates"""
    # 
    pass

def main():
    loop = True
    
    while loop == True:
        # Get user input and print #
        user_num = input("Enter a number: ")
        print("\nNumber:", user_num)
        3
        # Call convertor functions
        Conversion.hConverter(user_num)
        #kConverter()
        
        user_loop = input("Search again?[y/n]: ")
        if user_loop == 'y':
            loop = True
        else:
            loop = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = Window()
    win.show()
    sys.exit(app.exec())
    #main()