import numpy as np
import cv2 as cv
import json
import os

def k_Means(Image, K):
    
    if len(Image.shape) < 3:
      Z = Image.reshape((-1,1))
    elif len(Image.shape) == 3:
      Z = Image.reshape((-1,3))    

    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    Clustered_Image = res.reshape((Image.shape))
    
    return Clustered_Image

def get_number_of_clusters(json_path):
    
    data = []
    dictionary = {}

    with open(json_path) as f:
      data = json.load(f)
    
    for key, value in data.items():
      number_of_clusters = 0
      for val in value:
          if val == True:
              number_of_clusters += 1

      dictionary[key] = number_of_clusters

    return dictionary

def create_clustered_images():
    #max iter pozriet parameter na zrychlenie k-means
    
    folder_name = "clustered_images" #cesta kde sa maju ulozit vysledne obrazky po k-means
    json_path = "roi-level-cells.json"

    if not os.path.exists(folder_name): 
      os.makedirs(folder_name)

    dict = get_number_of_clusters(json_path)

    for key in dict:
      Clusters = dict[key]
      Input_Image = cv.imread('input_images/{}'.format(key)) #treba spravne nastavit cestu podla toho kde mate ulozene obrazky
      Clustered_Image = k_Means(Input_Image, Clusters)
      output_path = os.path.join(folder_name, key)
      cv.imwrite(output_path, Clustered_Image)


if __name__ == '__main__':
    create_clustered_images()
