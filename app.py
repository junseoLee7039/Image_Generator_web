from openai import OpenAI
from PIL import Image
import requests
import streamlit as st
from apikey import apikey
from streamlit_carousel import carousel

client = OpenAI(api_key=apikey)
single_img = dict(title="", text="", interval=None, img="")

def generate_images(img_description, num_of_images, quality):
    quality_mapping = {
        'low': ('standard', "512x512"),  # DALL-E 2 model
        'medium': ('standard', "1024x1024"),  # DALL-E 3 model
        'high': ('hd', "1792x1024")  # DALL-E 3 model
    }
    
    model_quality, size = quality_mapping.get(quality, ('standard', "1024x1024"))
    model = "dall-e-2" if size == "512x512" else "dall-e-3"
    
    image_gallery = []
    for i in range(num_of_images):
        try:
            img_response = client.images.generate(
                model=model,
                prompt=img_description,
                size=size,
                quality=model_quality,
                n=1
            )
            image_url = img_response.data[0].url
            new_image = single_img.copy()
            new_image["title"] = f"Image {i+1}"
            new_image["text"] = img_description
            new_image["img"] = image_url
            image_gallery.append(new_image)
        except Exception as e:
            print(f"Failed to generate image due to an error: {e}")
            return None
    
    return image_gallery

# Page configuration
st.set_page_config(page_title="Junseo Tools", page_icon=":camera:", layout="wide")
st.title("Junseo's Image Store")
st.subheader("POWERED BY Junseo's Generative Models")

# Image description input
img_description = st.text_input("Enter a description for the image")

# Number of images to generate
num_of_images = st.number_input("Select the number of images you want to generate", min_value=1, max_value=10, value=1)

# Image quality selection
quality_options = ['low', 'medium', 'high']
quality_option = st.selectbox("Select the quality of the images", quality_options)

if st.button("Generate Images"):
    generated_images = generate_images(img_description, num_of_images, quality_option)
    if generated_images:
        carousel(items=generated_images, width=1)
        
        # Display and provide download buttons for each image
        for img in generated_images:
            st.image(img["img"], caption=img["title"])
            img_data = requests.get(img["img"]).content
            st.download_button(label=f"Download {img['title']}", data=img_data, file_name=f"{img['title']}.png", mime="image/png")
    else:
        st.error("Failed to generate images due to an internal error.")
