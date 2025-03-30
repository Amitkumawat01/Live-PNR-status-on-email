import os
import cv2
import numpy as np
from tqdm import tqdm
import pickle
from sklearn.linear_model import LogisticRegression

numTolabel = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "+",
    11: "-",
    12: "=",
    13: "?",
}
labelTonum = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "+": 10,
    "-": 11,
    "=": 12,
    "?": 13,
}

def test_labels(Labels):
    i=0
    for lbl in Labels:
        # print(lbl)
        for l in lbl:
            if (
                l != "1"
                and l != "2"
                and l != "3"
                and l != "4"
                and l != "5"
                and l != "6"
                and l != "7"
                and l != "8"
                and l != "9"
                and l != "0"
                and l != "+"
                and l != "-"
                and l != "="
                and l != "?"
            ):
                print(lbl)
                print(i)
        i += 1

def segment_image(image, start_point):
    flag = 0
    start = start_point
    end = 149
    for i in range(start_point, 149):
        if flag==0 and sum(image[:,i]/100):
            start = i - 2
            flag=1
        
        if flag and sum(image[:,i]/100)==0:
            end = i + 2
            break

    finalImage = image[:, start:end]
    return finalImage, end

def process_image_data(path,Xtrain,ytrain):
    for imageIndex in tqdm(range(len(Xtrain))):
        dfX = []
        dfy = []
        
        image = cv2.imread(os.path.join(path, Xtrain[imageIndex]), cv2.IMREAD_UNCHANGED)
        trans_mask = image[:, :, 3] == 0
        image[trans_mask] = [255, 255, 255, 255]
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        image = cv2.bitwise_not(image)
        image = cv2.resize(image, (150, 30))
        # cv2.imwrite("test_image/Image1.png",image)
        end_point = 0
        
        for i in range(len(ytrain[imageIndex])):
            finalImage, end_point = segment_image(image, end_point)
            # print(finalImage.shape)
            finalImage = cv2.resize(finalImage, (25, 25))
            # pr=labelTonum[ytrain[imageIndex][i]]
            # cv2.imwrite("test_image/Image:"+str(pr)+".png", finalImage)
            finalImage = finalImage.flatten()
            dfX.append(finalImage)
            lebel = ytrain[imageIndex][i]
            dfy.append(labelTonum[lebel])
            # print(lebel)
            if lebel == "?":
                break

    return dfX,dfy

def get_test_train_data(imageList,Labels,splitRatio):
    Xtrain = []
    ytrain = []

    Xtest = []
    ytest = []

    count = len(imageList) * splitRatio
    i = 0
    for imageFile in imageList:
        if i < count:
            #  add to train list
            Xtrain.append(imageFile)
            labelIndex = int(imageFile.split(".")[0])
            ytrain.append(Labels[labelIndex])
        else:
            Xtest.append(imageFile)
            labelIndex = int(imageFile.split(".")[0])
            ytest.append(Labels[labelIndex])
        i += 1
    return Xtrain,ytrain,Xtest,ytest

def cal_accuracy(predictions,dfy):
    count = 0
    for i in range(len(predictions)):
        if predictions[i] == dfy[i]:
            count += 1
    
    return count/len(predictions)


if __name__=='__main__':

    path = "dataset"
    imageList = os.listdir(path)
    imageList.remove("lable.txt")

    with open("dataset/lable.txt", "r") as file:
        Labels = file.readlines()

    Labels = [line.rstrip("\n") for line in Labels]

    train_test_split_ratio = 0.999
    Xtrain,ytrain,Xtest,ytest = get_test_train_data(imageList,Labels,train_test_split_ratio)
    dfX_train,dfy_train = process_image_data(path,Xtrain,ytrain)
    dfX_test,dfy_test = process_image_data(path,Xtest,ytest)


    classifier = LogisticRegression(random_state=0, max_iter=4000)
    classifier.fit(dfX_train, dfy_train)
    predictions = classifier.predict(dfX_test)

    print("ACCURACY OF THE MODEL: ",cal_accuracy(predictions,dfy_test))

    model_path = "./model.sav"
    pickle.dump(classifier, open(model_path, "wb"))