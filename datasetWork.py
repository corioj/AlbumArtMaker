# DOWNLOAD DATASET HERE
#!unzip -q mini-edges2shoes.zip
!unzip -q Albums.zip
# genre dictionary
genre_dict = {
    "slowcore" : 0,
    "trap" : 1,
    "dance pop" : 2,
    "alternative metal" : 3,
    "shoegaze" : 4,
    "k pop" : 5,
    "indietronica" : 6,
    "indie rock" : 7,
    "emo rap" : 8,
    "house" : 9,
    "pop punk" : 10,
    "singer songwriter" : 11,
    "progressive house" : 12,
    "j pop" : 13,
    "punk" : 14,
    "classical" : 15,
    "glitchcore" : 16,
    "grunge" : 17,
    "trance" : 18,
    "neo-psychedelic" : 19,
    "noise pop" : 20,
    "post punk" : 21,
    "minimal techno" : 22,
    "post rock" : 23,
    "experimental rock" : 24,
    "vaporwave" : 25,
    "glitch" : 26,
    "ambient pop" : 27,
    "drone" : 28,
    "nightcore" : 29
}

# It is then available under directory '/content'.
# starts at AlbumArt0.jpg
# ends at AlbumArt157114.jpg
# align them with their genres in CSV file
# iterate over csvs in order of images saved, grab genrers and make them into array (num_Images x 1)
fileNames = ['/content/ProjectData1First.csv','/content/ProjectData2.csv', '/content/ProjectData.csv4', 
             '/content/ProjectData1.csv', '/content/ProjectData.csv3']

print(fileNames) # ordering should be _, 1First, 2, 4, 1, 3

genres = torch.tensor([genre_dict[val] for val in pd.read_csv('/content/ProjectData.csv')["genre"]])
for file in fileNames:
    genrescolumn = [genre_dict[val] for val in pd.read_csv(file)["genre"]]
    genrevals = torch.tensor(genrescolumn)
    torch.cat(genres, genrevals, 1)


##BUILD DATALOADER USING data_loader = torch.utils.data.DataLoader()
#tr_dt = Edges2Shoes('./mini-edges2shoes', 'train', transform)
#train_loader = DataLoader(tr_dt, batch_size=4, shuffle=True)
#te_dt = Edges2Shoes('./mini-edges2shoes', 'val', transform)
#test_loader = DataLoader(te_dt, batch_size=5, shuffle=False)
class AlbumCovers(Dataset):
    def __init__(self, transform=None):

        self.transform = transform
        self.files = glob.glob('./Albums/*')

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        img = Image.open(self.files[idx])
        img = np.asarray(img)
        if self.transform:
            img = self.transform(img)
        return img


# batch_size = ???
# genres = 30

# this shoould contain our jpgs
files = glob.glob('./Albums/*')
# relying on this being a UNIQUE random sample, or else implementation needs to be redone

##BUILD DATALOADER USING data_loader = torch.utils.data.DataLoader()
dt = AlbumCovers(transform = transform)

# HOW TO SELECT A GOOD PROPORTION OF TRAIN, TESTING IMAGES PER GENRE??? Just training is fine. No need for val or test
# HOW TO SELECT A GOOD BATCH SIZE? 32 or 64 is typically used. idk the semantics exactly

#glob glob the filepath and THEN do random sampling from it

# HOW TO SELECT A GOOD PROPORTION OF TRAIN, VAL, AND TESTING IMAGES PER GENRE???
# HOW TO SELECT A GOOD BATCH SIZE?

he uses embed to push the labels into each image. FOR i, (images, labels) IN enumerate(dataloader)
so maybe do self.labels = genres, self.images = T

#train_data = []
#for i in range(len(x_data)):
#   train_data.append([x_data[i], labels[i]])

#trainloader = torch.utils.data.DataLoader(train_data, shuffle=True, batch_size=100)
#i1, l1 = next(iter(trainloader))
#print(i1.shape)

# for row in each csv, delete /Users/johncorio/Documents/EECS 442 Files/project/AlbumArt/ from 'Art Link' col
train_data = []
for file in ['ProjectData.csv', 'ProjectData1First.csv','ProjectData2.csv', 
            'ProjectData.csv4', 'ProjectData1.csv', 'ProjectData.csv3']:
    data = pd.read_csv(file)
    genres = np.array([genre_dict[val] for val in data["Genre"]])
    images = [[st.replace('/Users/johncorio/Documents/EECS 442 Files/project/AlbumArt/', '') for st in data['Art Link']]]
    for i in range(len(genres)):
        train_data.append([images[i], genres[i]])