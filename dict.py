class data_ware:
    data = {'class_type': ['Astronomy','Charms','Dark Arts','Defence Against the Dark Arts',\
    'Flying','Herbology','History of Magic','Muggle Studies','Potions','Transfiguration',\
    'Alchemy','Apparition','Arithmancy','Care of Magical Creatures','Divination','Study of Ancient Runes'],\
     'house_type': ['Gryffindor','Hufflepuff','Ravenclaw','Slytherin'],\
     'professor_type': ['Albus Dumbledore','Alecto CArrow','Amycus Carrow',\
     'Aurora Sinistra','Bathsheda Babbling','Bartemius Crouch Jr','Charity Burbage',\
     'Cuthbert Binns','Dolores Umbridge','Filius Flitwick','Firenze','Calatea Merrythought',\
     'Gilderoy Lockhart','Herbert Beery','Horace Slughorn','Mineva McGonagall','Neville Longbottom'\
     'Pomona Sprout','Quirinus Quirrell','Remius Lupin','Rolanda Hooch','Rubeus Hagrid',\
     'Septima Vector','Severus Snape','Silvanus Kettleburn','Sybill Trelawney',\
     'Vindictus Viridian','Wilhelmina Grubbly-Plank']}
    def data_ware_access(self,key,value):
        for i in self.data[key]:
            print("data content: "+ i)
        '''if value in data[key]''' 
    def data_ware_set(self,key,value):
        for i in self.data[key]:
            print("data content: "+ i)
        '''if value in data[key]''' 

    def meow(self):
        print(self.name + ' Meow!')

dat_access = data_ware()
dat_access.data_access('house_type','Ravenclaw')