import glob

from sentence_transformers import SentenceTransformer, util
from PIL import Image
import pandas as pd

# packages needed: sentence-transformers/pillow/torchvision/pytorch

print('Loading CLIP Model...')
model = SentenceTransformer('clip-ViT-B-32')

# Encode an image:
# img_emb_1 = model.encode(Image.open('img/642_01.jpg'))
# img_emb_2 = model.encode(Image.open('img/668_01.jpg'))

image_names = list(glob.glob('img/*.jpg'))
print("Images:", len(image_names))
img_emb = model.encode([Image.open(filepath) for filepath in image_names],
                       batch_size=128,
                       convert_to_tensor=True,
                       show_progress_bar=True)

processed_images = util.paraphrase_mining_embeddings(img_emb)
NUM_SIMILAR_IMAGES = 10

d = []
# Output the top X duplicate images
for score, image_id1, image_id2 in processed_images:
    # d[(image_names[image_id1][4:-7], image_names[image_id2][4:-7])] = round(score * 100, 3)
    d.append([image_names[image_id1][4:-7], image_names[image_id2][4:-7], round(score, 5)])
    # if (score * 100) > 90:
    #     print("\nScore: {:.3f}%".format(score * 100))
    #     print(image_names[image_id1])
    #     print(image_names[image_id2])

a = pd.DataFrame(d, columns=['item1', 'item2', 'sim'])
a.to_csv('img_sim.csv', index=False)
print('Done....')
