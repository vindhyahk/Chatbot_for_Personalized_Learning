import streamlit as st
import requests
import json
from datetime import datetime

st.title("Learning Assistant Chatbot")

# Initialize chat history and enrolled courses
if "messages" not in st.session_state:
    st.session_state.messages = []
if "enrolled_courses" not in st.session_state:
    st.session_state.enrolled_courses = []

# Define materials for all topics
COURSE_MATERIALS = {
    "web": {
        "name": "Web Development for Beginners",
        "materials": [
            {
                "name": "freeCodeCamp Web Development",
                "url": "https://www.freecodecamp.org/learn/responsive-web-design/"
            },
            {
                "name": "MDN Web Docs",
                "url": "https://developer.mozilla.org/en-US/docs/Learn"
            },
            {
                "name": "The Odin Project",
                "url": "https://www.theodinproject.com/"
            }
        ],
        "description": "A curated learning path for beginners in web development",
        "learning_path": [
            "Start with HTML & CSS basics",
            "Move on to JavaScript",
            "Choose a framework (React, Vue, or Angular)"
        ]
    },
    "data": {
        "name": "Data Science for Beginners",
        "materials": [
            {
                "name": "Coursera Python for Everybody",
                "url": "https://www.coursera.org/specializations/python"
            },
            {
                "name": "DataCamp Introduction to Python",
                "url": "https://www.datacamp.com/courses/intro-to-python-for-data-science"
            },
            {
                "name": "Kaggle Learn",
                "url": "https://www.kaggle.com/learn"
            }
        ],
        "description": "A comprehensive introduction to data science and analysis",
        "learning_path": [
            "Learn Python basics",
            "Master data analysis libraries",
            "Practice with real datasets"
        ]
    },
    "mobile": {
        "name": "Mobile App Development for Beginners",
        "materials": [
            {
                "name": "Android Developer Fundamentals",
                "url": "https://developer.android.com/courses"
            },
            {
                "name": "iOS App Development with Swift",
                "url": "https://developer.apple.com/tutorials/swiftui"
            },
            {
                "name": "React Native Tutorial",
                "url": "https://reactnative.dev/docs/tutorial"
            }
        ],
        "description": "Learn to build mobile apps for iOS and Android",
        "learning_path": [
            "Choose your platform (iOS/Android)",
            "Learn platform basics",
            "Build your first app"
        ]
    },
    "ai": {
        "name": "Artificial Intelligence for Beginners",
        "materials": [
            {
                "name": "Fast.ai - Practical Deep Learning",
                "url": "https://www.fast.ai/"
            },
            {
                "name": "Coursera Machine Learning Specialization",
                "url": "https://www.coursera.org/specializations/machine-learning-introduction"
            },
            {
                "name": "Google AI Education",
                "url": "https://ai.google/education/"
            }
        ],
        "description": "Introduction to AI and machine learning concepts",
        "learning_path": [
            "Learn Python and mathematics basics",
            "Understand ML fundamentals",
            "Practice with AI frameworks"
        ]
    }
}

# Add feedback responses
FEEDBACK_RESPONSES = {
    "thanks": [
        "You're welcome! 😊 Let me know if you need anything else!",
        "Happy to help! 🌟 Feel free to explore more courses!",
        "Glad I could help! 🎉 Don't forget you can check your courses anytime!"
    ],
    "good": [
        "Thank you for the feedback! 🌟 Is there anything else you'd like to learn?",
        "Wonderful! 🎉 Let me know if you want to explore more topics!",
        "Great to hear that! 😊 Feel free to ask about other courses!"
    ],
    "bye": [
        "Goodbye! 👋 Come back anytime to continue learning!",
        "See you later! 🌟 Your courses will be here when you return!",
        "Have a great day! 😊 Don't forget to practice what you've learned!"
    ],
    "hello": [
        "Hi there! 👋 Ready to learn something new?",
        "Hello! 🌟 What would you like to learn today?",
        "Welcome! 😊 I can help you find the perfect course!"
    ]
}

def get_feedback_response(prompt):
    import random
    if any(word in prompt for word in ["thanks", "thank you", "thx"]):
        return random.choice(FEEDBACK_RESPONSES["thanks"])
    elif any(word in prompt for word in ["good", "great", "awesome", "amazing"]):
        return random.choice(FEEDBACK_RESPONSES["good"])
    elif any(word in prompt for word in ["bye", "goodbye", "see you"]):
        return random.choice(FEEDBACK_RESPONSES["bye"])
    elif any(word in prompt for word in ["hi", "hello", "hey"]):
        return random.choice(FEEDBACK_RESPONSES["hello"])
    return None

def display_course_response(topic):
    course = COURSE_MATERIALS[topic]
    response_text = f"🎉 Welcome to {course['name']}!"
    
    st.markdown(response_text)
    st.write("📚 **Learning Materials:**")
    for material in course['materials']:
        st.markdown(f"• [{material['name']}]({material['url']})")
    
    st.write("\n📝 **Course Description:**")
    st.write(course['description'])
    
    st.info("💡 **Learning Path:**\n" + 
            "\n".join(f"{i+1}. {step}" for i, step in enumerate(course['learning_path'])) +
            "\n\nType 'show my courses' anytime to see your enrolled courses!")
    
    # Add course to enrolled courses
    course_entry = {
        "name": course['name'],
        "enrolled_at": datetime.now().strftime("%Y-%m-%d"),
        "status": "In Progress",
        "materials": course['materials']
    }
    if course_entry not in st.session_state.enrolled_courses:
        st.session_state.enrolled_courses.append(course_entry)
    
    return response_text, course['materials']

def show_enrolled_courses():
    if st.session_state.enrolled_courses:
        response_text = "Here are your enrolled courses:\n\n"
        for course in st.session_state.enrolled_courses:
            response_text += f"📚 {course['name']}\n"
            response_text += f"Status: {course['status']}\n"
            response_text += f"Enrolled: {course['enrolled_at']}\n\n"
            
        st.markdown(response_text)
        
        # Show materials for each course
        for course in st.session_state.enrolled_courses:
            st.write(f"\n**Materials for {course['name']}:**")
            for material in course['materials']:
                st.markdown(f"• [{material['name']}]({material['url']})")
    else:
        st.markdown("You're not enrolled in any courses yet. Would you like some recommendations?")

def check_input_requirements(prompt):
    has_experience = any(word in prompt for word in ["beginner", "intermediate", "advanced"])
    has_topic = any(word in prompt for word in ["web", "data", "science", "mobile", "app", "ai", "artificial"])
    
    if not has_experience and not has_topic:
        return "Please provide both your experience level (beginner/intermediate/advanced) and interest area. For example: 'I'm a beginner interested in web development'"
    elif not has_experience:
        return "Please specify your experience level (beginner/intermediate/advanced). For example: 'I'm a beginner'"
    elif not has_topic:
        return "Please specify what you'd like to learn (web development, data science, mobile apps, or artificial intelligence)"
    return None

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "materials" in message:
            st.write("📚 **Learning Materials:**")
            for material in message["materials"]:
                st.markdown(f"• [{material['name']}]({material['url']})")

# Accept user input
if prompt := st.chat_input("What would you like to learn?"):
    prompt = prompt.lower()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # First check for feedback/greetings
        feedback_response = get_feedback_response(prompt)
        if feedback_response:
            st.markdown(feedback_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": feedback_response
            })
        # Then check for course-related queries
        elif "show my courses" in prompt:
            show_enrolled_courses()
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Showing your enrolled courses"
            })
        else:
            # Check if input meets requirements
            requirement_message = check_input_requirements(prompt)
            if requirement_message:
                st.markdown(requirement_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": requirement_message
                })
            else:
                # Check for topic matches
                topic = None
                if "web" in prompt:
                    topic = "web"
                elif "data" in prompt or "science" in prompt:
                    topic = "data"
                elif "mobile" in prompt or "app" in prompt:
                    topic = "mobile"
                elif "ai" in prompt or "artificial" in prompt:
                    topic = "ai"
                
                if topic:
                    response_text, materials = display_course_response(topic)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "materials": materials
                    })

# Add sidebar with additional information
with st.sidebar:
    st.header("About Learning Assistant")
    st.write("This chatbot helps you find the right programming courses based on your experience level and interests.")
    st.write("Try asking about:")
    st.write("- Web Development")
    st.write("- Data Science")
    st.write("- Mobile Apps")
    st.write("- Artificial Intelligence")