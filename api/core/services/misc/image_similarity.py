import glob

from sentence_transformers import SentenceTransformer, util
from PIL import Image

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

# Output the top X duplicate images
for score, image_id1, image_id2 in processed_images:
    print("\nScore: {:.3f}%".format(score * 100))
    print(image_names[image_id1])
    print(image_names[image_id2])

print('Cone....')
