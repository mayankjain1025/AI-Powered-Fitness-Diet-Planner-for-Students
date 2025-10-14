import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="FitStudent AI",
    page_icon="💪",
    layout="wide"
)

# Initialize session state early
def init_session_state():
    if 'workout_plan' not in st.session_state:
        st.session_state.workout_plan = None
    if 'meal_plan' not in st.session_state:
        st.session_state.meal_plan = None
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False

init_session_state()

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    h1 {
        color: #2c3e50;
    }
    h2 {
        color: #34495e;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("💪 FitStudent AI")
st.markdown("### Your Personalized Fitness & Nutrition Companion")
st.markdown("Get AI-powered workout routines and meal plans tailored to your needs, culture, and budget!")

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input(
        "Enter Gemini API Key", 
        type="password", 
        help="Get your API key from https://makersuite.google.com/app/apikey",
        key="api_key_input"
    )
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.api_configured = True
            st.success("✅ API Key configured!")
        except Exception as e:
            st.error(f"❌ Invalid API Key: {str(e)}")
            st.session_state.api_configured = False
    
    st.markdown("---")
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. Enter your Gemini API key
    2. Fill in your personal details
    3. Select workout or meal plan
    4. Get your personalized plan!
    """)
    
    st.markdown("---")
    st.markdown("### 🔑 Get API Key")
    st.markdown("[Get Gemini API Key](https://makersuite.google.com/app/apikey)")
    
    st.markdown("---")
    st.info("💡 **Tip:** Your data stays private and is never stored!")

# Main content
if not st.session_state.api_configured:
    st.warning("⚠️ Please enter your Gemini API key in the sidebar to continue.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("### 🚀 Getting Started\n\n1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)\n2. Paste it in the sidebar\n3. Start creating your personalized plans!")
else:
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🏋️ Workout Plan", "🍽️ Meal Plan"])
    
    with tab1:
        st.header("Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=15, max_value=50, value=20, key="age")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, key="height")
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=65, key="weight")
        
        with col2:
            fitness_goal = st.selectbox(
                "Fitness Goal",
                ["Weight Loss", "Muscle Gain", "General Fitness", "Endurance", "Flexibility"],
                key="fitness_goal"
            )
            fitness_level = st.selectbox(
                "Current Fitness Level",
                ["Beginner", "Intermediate", "Advanced"],
                key="fitness_level"
            )
            available_time = st.slider("Available Time (minutes/day)", 15, 120, 45, key="time")
            equipment = st.multiselect(
                "Available Equipment",
                ["None (Bodyweight)", "Dumbbells", "Resistance Bands", "Pull-up Bar", "Gym Access"],
                key="equipment"
            )
        
        st.subheader("Cultural & Dietary Preferences")
        col3, col4 = st.columns(2)
        
        with col3:
            culture = st.selectbox(
                "Cultural Background",
                ["Indian", "Chinese", "Mediterranean", "Latin American", "Middle Eastern", "African", "European", "Other"],
                key="culture"
            )
            diet_type = st.selectbox(
                "Dietary Preference",
                ["Vegetarian", "Vegan", "Non-Vegetarian", "Pescatarian", "Eggetarian"],
                key="diet"
            )
        
        with col4:
            budget = st.selectbox(
                "Daily Food Budget",
                ["Very Low ($2-5)", "Low ($5-10)", "Moderate ($10-15)", "Flexible ($15+)"],
                key="budget"
            )
            allergies = st.text_input("Food Allergies/Restrictions (if any)", key="allergies")
        
        cooking_access = st.selectbox(
            "Cooking Facilities",
            ["Full Kitchen", "Microwave Only", "Hot Plate", "No Cooking (Eating Out)"],
            key="cooking"
        )
        
        st.success("✅ Profile saved! Switch to the Workout or Meal Plan tabs to generate your personalized plans.")
    
    with tab2:
        st.header("🏋️ Personalized Workout Plan")
        
        st.info(f"**Current Goal:** {st.session_state.get('fitness_goal', 'Not set')} | **Level:** {st.session_state.get('fitness_level', 'Not set')} | **Time:** {st.session_state.get('time', 0)} min/day")
        
        if st.button("🎯 Generate Workout Plan", key="workout_btn", type="primary"):
            with st.spinner("🏋️ Creating your personalized workout plan..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    equipment_list = st.session_state.get('equipment', [])
                    equipment_str = ', '.join(equipment_list) if equipment_list else 'None (Bodyweight only)'
                    
                    prompt = f"""
                    Create a detailed, personalized workout plan for a student with the following profile:
                    
                    - Age: {st.session_state.get('age', 20)}
                    - Gender: {st.session_state.get('gender', 'Not specified')}
                    - Height: {st.session_state.get('height', 170)} cm, Weight: {st.session_state.get('weight', 65)} kg
                    - Fitness Goal: {st.session_state.get('fitness_goal', 'General Fitness')}
                    - Current Level: {st.session_state.get('fitness_level', 'Beginner')}
                    - Available Time: {st.session_state.get('time', 45)} minutes per day
                    - Equipment: {equipment_str}
                    
                    Please provide:
                    1. A weekly workout schedule (7 days with specific day names)
                    2. Specific exercises for each day with sets, reps, and duration
                    3. Rest days and active recovery suggestions
                    4. Warm-up routine (5-10 minutes)
                    5. Cool-down and stretching routine
                    6. Tips for progression over 4 weeks
                    7. Safety considerations and form tips
                    
                    Make it practical for a busy student with limited time and resources.
                    Format with clear headers, bullet points, and be specific about exercises.
                    Include motivational tips!
                    """
                    
                    response = model.generate_content(prompt)
                    st.session_state.workout_plan = response.text
                    st.success("✅ Workout plan generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating workout plan: {str(e)}")
        
        if st.session_state.workout_plan:
            st.markdown("---")
            st.markdown("### 📋 Your Personalized Workout Plan")
            st.markdown(st.session_state.workout_plan)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    label="📥 Download Workout Plan",
                    data=st.session_state.workout_plan,
                    file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    key="download_workout"
                )
    
    with tab3:
        st.header("🍽️ Personalized Meal Plan")
        
        st.info(f"**Cuisine:** {st.session_state.get('culture', 'Not set')} | **Diet:** {st.session_state.get('diet', 'Not set')} | **Budget:** {st.session_state.get('budget', 'Not set')}")
        
        if st.button("🍳 Generate Meal Plan", key="meal_btn", type="primary"):
            with st.spinner("🍽️ Creating your personalized meal plan..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    allergies_str = st.session_state.get('allergies', '')
                    
                    prompt = f"""
                    Create a detailed, culturally-appropriate meal plan for a student with the following profile:
                    
                    - Age: {st.session_state.get('age', 20)}, Gender: {st.session_state.get('gender', 'Not specified')}
                    - Height: {st.session_state.get('height', 170)} cm, Weight: {st.session_state.get('weight', 65)} kg
                    - Fitness Goal: {st.session_state.get('fitness_goal', 'General Fitness')}
                    - Cultural Background: {st.session_state.get('culture', 'Indian')}
                    - Dietary Preference: {st.session_state.get('diet', 'Vegetarian')}
                    - Daily Budget: {st.session_state.get('budget', 'Low')}
                    - Cooking Facilities: {st.session_state.get('cooking', 'Full Kitchen')}
                    - Allergies/Restrictions: {allergies_str if allergies_str else 'None'}
                    
                    Please provide:
                    1. A 7-day meal plan with day names (Monday to Sunday)
                    2. Each day should include: Breakfast, Mid-Morning Snack, Lunch, Evening Snack, Dinner
                    3. Include culturally familiar foods from {st.session_state.get('culture', 'Indian')} cuisine
                    4. Calorie estimates for each meal and daily total
                    5. Simple, student-friendly recipes with prep time
                    6. Budget-friendly ingredient lists with approximate costs
                    7. Weekly grocery shopping list organized by category
                    8. Daily macronutrient breakdown (protein, carbs, fats)
                    9. Meal prep tips for busy students
                    10. Hydration reminders
                    
                    Make it practical, affordable, and easy to follow for a student lifestyle.
                    Format with clear headers and organized sections.
                    Include cooking tips and time-saving hacks!
                    """
                    
                    response = model.generate_content(prompt)
                    st.session_state.meal_plan = response.text
                    st.success("✅ Meal plan generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error generating meal plan: {str(e)}")
        
        if st.session_state.meal_plan:
            st.markdown("---")
            st.markdown("### 📋 Your Personalized Meal Plan")
            st.markdown(st.session_state.meal_plan)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    label="📥 Download Meal Plan",
                    data=st.session_state.meal_plan,
                    file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    key="download_meal"
                )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>💡 <strong>Pro Tips:</strong> Consistency is key! Track your progress and adjust plans as needed.</p>
    <p>⚠️ <strong>Disclaimer:</strong> This is an AI-generated plan. Consult healthcare professionals before starting any new fitness or diet program.</p>
    <p style='margin-top: 10px; font-size: 12px;'>Made with ❤️ for students | Powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)