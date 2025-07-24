import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter    
import numpy as np
import matplotlib.pyplot as plt    

st.set_page_config(page_title="Photo Editor", layout="centered")
st.title("Photo Editor Web App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
else:
    st.warning("Please upload an image file.")
    st.stop()

st.image(image, caption="Your Uploaded Image", use_container_width=True)
original_image = image.copy()

# Rotation 
st.sidebar.subheader("Image Rotation")
rotation_options = st.sidebar.selectbox("Choose rotation", ["0°", "90°", "180°", "270°"])

if rotation_options == "90°":
    image = image.rotate(-90, expand=True)
elif rotation_options == "180°":
    image = image.rotate(180, expand=True)
elif rotation_options == "270°":
    image = image.rotate(-270, expand=True)
    

#Basic Filters
st.sidebar.header("Edit Options:")
filter_options = st.sidebar.selectbox("Choose a filter:", ["None", "Invert Colors", "Grayscale", "Old Film", "Outlines"])

if filter_options == "Invert Colors":
    image = Image.fromarray(255 - np.array(image))

elif filter_options == "Grayscale":
    image = image.convert("L").convert("RGB")

elif filter_options == "Old Film":
    sepia_image = np.array(image)
    tr = [0.393, 0.769, 0.189]
    tg = [0.349, 0.686, 0.168]
    tb = [0.272, 0.534, 0.131]
    
    r = sepia_image[:, :, 0]
    g = sepia_image[:, :, 1]
    b = sepia_image[:, :, 2]

    sepia_r = r * tr[0] + g * tr[1] + b * tr[2]
    sepia_g = r * tg[0] + g * tg[1] + b * tg[2]
    sepia_b = r * tb[0] + g * tb[1] + b * tb[2]

    sepia = np.stack([sepia_r, sepia_g, sepia_b], axis=2)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    image = Image.fromarray(sepia)

elif filter_options == "Outlines":
    image = image.filter(ImageFilter.FIND_EDGES)

#Adjusting Brightness and Contrast
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0, 0.1)
saturation = st.sidebar.slider("Saturation", 0.5, 2.0, 1.0, 0.1)

enhancer = ImageEnhance.Brightness(image)
image = enhancer.enhance(brightness)

enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(contrast)

enhancer = ImageEnhance.Sharpness(image)
image = enhancer.enhance(sharpness)

enhancer = ImageEnhance.Color(image)
image = enhancer.enhance(saturation)

st.image(image, caption="Edited Image", use_container_width=True)

#RGB
st.sidebar.subheader("Color Channels")
show_channels = st.sidebar.checkbox("Show Color Channels")

if show_channels:
    image_array = np.array(image)
    r, g, b = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]
    
    red_img = np.zeros_like(image_array)
    green_img = np.zeros_like(image_array)
    blue_img = np.zeros_like(image_array)

    red_img[:, :, 0] = r
    green_img[:, :, 1] = g
    blue_img[:, :, 2] = b
    
    st.subheader("Color Channels")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(red_img, caption="Red Channel", use_container_width=True)

    with col2:
        st.image(green_img, caption="Green Channel", use_container_width=True)

    with col3:
        st.image(blue_img, caption="Blue Channel", use_container_width=True)

#colormap
# st.sidebar.subheader("Image Adjustments")
apply_colormap = st.sidebar.checkbox("Show Colormapped Image")
color_map = st.sidebar.selectbox(
    "Select a colormap",
    ["viridis", "plasma", "inferno", "magma", "cividis", "hot", "cool", "gray"]
)

if apply_colormap:
    st.subheader("Color Mapped Image")
    gray_image = image.convert("L")
    gray_array = np.array(gray_image)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(gray_array, cmap=color_map)
    plt.axis("off")
    st.pyplot(fig)

# Original Image vs Edited Image
st.subheader("Original Image vs Edited Image")
col1, col2 = st.columns(2)
with col1:
    st.image(original_image, caption="Original Image", use_container_width=True)

with col2:
    st.image(image, caption="Edited Image", use_container_width=True)

# Download button
st.sidebar.subheader("Save Your Image")
if st.sidebar.button("Download Edited Image"):
    image.save("edited_image.jpg")
    st.success("Image saved as 'edited_image.jpg'!")