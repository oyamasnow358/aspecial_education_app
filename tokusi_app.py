import streamlit as st
import json
from streamlit_lottie import st_lottie
import time

# Lottieアニメーションを読み込む関数
@st.cache_data
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: {filepath} not found.")
        return None
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from {filepath}. Is it a valid Lottie JSON?")
        return None

st.set_page_config(layout="wide")

# animation.jsonを読み込む (またはテスト用のLottieファイルを指定)
lottie_animation_path = "animation.json" # または "test_animation.json"
lottie_animation = load_lottiefile(lottie_animation_path)

if lottie_animation:
    st.title("Lottie Animation Test")
    st.write("Loading animation...")

    # アニメーションを表示
    st_lottie(
        lottie_animation,
        speed=1,
        loop=True, # 無限ループで表示
        quality="high",
        height="300px",
        width="300px",
        key="test_animation"
    )
    st.success("Lottie animation should be displayed above.")
else:
    st.error("Failed to load Lottie animation. Check console for details.")

st.write("---")
st.write("Main content would go here after animation.")