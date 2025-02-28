import streamlit as st
import numpy as np
from PIL import Image


image = Image.open('bofsedimage.jpg')
st.image(image, use_column_width=True)

def generate_animation(sedimentation_velocity, particle_size):
    if sedimentation_velocity <= 0:
        return """
        .particle {
            animation: none;
        }
        """
    else:
        particle_size = particle_size * 40 # Use particle_size directly for the particle size
        duration = max(80 / sedimentation_velocity, 0.1)  # Prevent division by zero and ensure a minimum duration
        return f"""
        @keyframes fall {{
            from {{ top: -50px; }}
            to {{ top: calc(100% - {particle_size}px); }}
        }}
        .particle {{
            animation: fall {duration}s infinite;
            width: {particle_size}px;
            height: {particle_size}px;
        }}
        """

# HTML and CSS for the test tube and falling particle animation
html = """
<div class="test-tube-container">
    <div class="test-tube">
        <div class="liquid">
            <div class="particle"></div>
        </div>
        <div class="shine"></div>
    </div>
</div>
<style>
    .test-tube-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 400px;
    }
    .test-tube {
        position: relative;
        width: 80px;
        height: 300px;
        background: linear-gradient(to right, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0.1) 100%);
        border-radius: 0 0 40px 40px;
        overflow: hidden;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
    .test-tube::before {
        content: '';
        position: absolute;
        top: -10px;
        left: 0;
        right: 0;
        height: 20px;
        background: linear-gradient(to right, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.8) 50%, rgba(255,255,255,0.5) 100%);
        border-radius: 40px 40px 0 0;
    }
    .liquid {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 280px;
        background: linear-gradient(to bottom, rgba(173,216,230,0.8) 0%, rgba(135,206,235,0.9) 100%);
        border-radius: 0 0 40px 40px;
    }
    .shine {
        position: absolute;
        top: 0;
        left: 5px;
        width: 15px;
        height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 100%);
        transform: skew(-10deg);
    }
    .particle {
        position: absolute;
        background-color: rgba(255, 0, 0, 0.7);
        border-radius: 50%;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
    }
</style>
"""
# Define the initial position and properties of the biological particle
particle_radius = 0.1  # cm
# Define the properties of the biological buffer system
buffer_viscosity = 1.0  # cP (centipoise)
# Streamlit app
st.markdown("<h1 style='font-size:24px;font-weight:normal;font-style:italic;'>Using the side panel, Adjust Particle & Buffer properties and Centrifugal Force to visualize interactively how different factors influence sedimentation</h1>", unsafe_allow_html=True)
st.sidebar.header("Particle Properties")
particle_size = st.sidebar.slider("Particle Size (cm)", 0.5, 2.0, 1.1, 0.1)
particle_density = st.sidebar.slider("Particle Density (g/cm^3)", 0.5, 2.0, 1.1, 0.1)
st.sidebar.header("Buffer Properties")
buffer_density = st.sidebar.slider("Buffer Density (g/cm^3)", 0.5, 2.0, 1.0, 0.1)
buffer_viscosity = st.sidebar.slider("Buffer Viscosity (cP)", 0.1, 10.0, 1.0, 0.1)
st.sidebar.header("Centrifugal Field")
centrifugal_force = st.sidebar.slider("Centrifugal Field (x **g*)", 1, 10000, 1000, 100)
# Sedimentation rate function
def sedimentation_rate(particle_size, particle_density, buffer_density, centrifugal_force, friction_coefficient, particle_mass):
    return (particle_density - buffer_density) * centrifugal_force * particle_size * particle_mass / friction_coefficient
# Calculate particle mass and friction coefficient
particle_mass = (4/3) * np.pi * particle_radius * particle_density
friction_coefficient = 6 * np.pi * buffer_viscosity * particle_radius
# Calculate sedimentation velocity
st.sidebar.header(':orange[Sedimentation Rate]')
sedimentation_velocity = sedimentation_rate(particle_size, particle_density, buffer_density, centrifugal_force, friction_coefficient, particle_mass)
st.sidebar.markdown(f"The sedimentation rate is: {sedimentation_velocity:.2f} cm/s")

# Injecting the custom HTML/CSS into the Streamlit app
css_animation = generate_animation(sedimentation_velocity, particle_size)
st.markdown(html, unsafe_allow_html=True)  # Ensure this comes before the CSS injection
st.markdown(f"<style>{css_animation}</style>", unsafe_allow_html=True)


st.markdown("""
***Found the App useful or Have a suggestion?*** Kinldy provide your valuable FEEDBACK👉[HERE](https://forms.gle/n6aJuVSSm2zMaFex8)


**Centrifugation: Basics of Sedimentation App** © 2025 by [VISHAL BHOIR](https://linktr.ee/thebioway) is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

""")
