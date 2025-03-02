import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import os

API_KEY = os.getenv("AIzaSyDY1qvVkqiGZRSipzTfseOhE7GEs6_DyCk")

st.title("🌍 AI-Powered Travel Planner ✈️")
st.write("Enter your travel details to get estimated traveling cost details for various travel modes including 🚖 cab, 🚆 train, 🚌 bus, and ✈️ flight.")

# User inputs
source = st.text_input("📍 Source:")
destination = st.text_input("📍 Destination:")
budget = st.number_input("💰 Budget (in your currency):", min_value=0, step=100)
travel_time = st.selectbox("⏰ Preferred Travel Time:", ["🌅 Morning", "🌞 Afternoon", "🌆 Evening", "🌙 Night", "Anytime"])
num_travelers = st.number_input("👥 Number of Travelers:", min_value=1, step=1)
preferred_mode = st.multiselect("🚗 Preferred Mode of Transport:", ["🏍️ Bike", "🚖 Cab", "🚌 Bus", "🚆 Train", "✈️ Flight", "Any"])

if st.button("🛫 Plan My Trip"):
    if source and destination:
        with st.spinner("🔄 Fetching all travel options...."):
            chat_template = ChatPromptTemplate(messages=[
                ("system", """You are an AI-Powered Travel Planner assistant that provides users with the best travel options based on their requirements.
                Given source to destination, you must give the distance and provide information about the best travel options like bike, cab, bus, train, and flight.
                Each option should have the estimated cost, travel time, distance, and any relevant details like stops, and traffic details.
                Additionally, consider budget, preferred travel time, number of travelers, and preferred mode of transport.
                You can also provide information about the best food items available between the source and destination.
                Convince while presenting the results in a clear, easy-to-read format.
                Ensure responses are in the selected language."""),

                ("human", """
                Find travel options from {source} to {destination} with estimated costs.
                Budget: {budget}.
                Preferred travel time: {travel_time}.
                Number of travelers: {num_travelers}.
                Preferred mode(s): {preferred_mode}.
                """)
            ])
            
            chat_model = ChatGoogleGenerativeAI(api_key="AIzaSyDY1qvVkqiGZRSipzTfseOhE7GEs6_DyCk", model="gemini-2.0-flash-exp")
            parser = StrOutputParser()
            
            chain = chat_template | chat_model | parser
            
            raw_input = {
                "source": source,
                "destination": destination,
                "budget": budget,
                "travel_time": travel_time,
                "num_travelers": num_travelers,
                "preferred_mode": ", ".join(preferred_mode)
            }
            
            response = chain.invoke(raw_input)
            
            st.success("✅ Estimated Travel and Costs:")
            travel_modes = response.split("\n")
            for mode in travel_modes:
                st.markdown(mode)
    else:
        st.warning("⚠️ Please enter both source and destination locations.")
