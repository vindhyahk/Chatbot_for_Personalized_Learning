from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from utils.lms_utils import LMSManager
    

class ActionProvideLearningRecommendations(Action):
    # Handles course recommendations and enrollment
    def __init__(self):
        super().__init__()
        self.lms = LMSManager()

    def name(self) -> Text:
        return "action_provide_learning_recommendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Processes user input and provides personalized course recommendations
        latest_message = tracker.latest_message['text'].lower()
        user_id = tracker.sender_id

        # Handle feedback responses
        if any(word in latest_message for word in ['helpful', 'thanks', 'good', 'great']):
            response = "I'm glad you found it helpful! You can type 'show my courses' to see your enrolled courses."
            dispatcher.utter_message(text=response)
            return []

        # Extract experience and interest
        experience = None
        interest = None

        if 'beginner' in latest_message:
            experience = 'beginner'
        elif 'intermediate' in latest_message:
            experience = 'intermediate'

        # Determine the interest area
        if 'data' in latest_message or 'science' in latest_message:
            interest = 'data science'
        elif 'web' in latest_message:
            interest = 'web development'
        elif 'mobile' in latest_message or 'app' in latest_message:
            interest = 'mobile apps'
        elif 'ai' in latest_message or 'artificial' in latest_message:
            interest = 'artificial intelligence'

        if experience and interest:
            try:
                # Create course name and description
                course_name = f"{interest.title()} for {experience.title()}s"
                description = f"A curated learning path for {experience}s in {interest}"

                # Define materials based on interest
                materials_dict = {
                    'data science': [
                        {
                            "name": "Coursera Python for Everybody",
                            "url": "https://www.coursera.org/specializations/python"
                        },
                        {
                            "name": "DataCamp Introduction to Python",
                            "url": "https://www.datacamp.com/courses/intro-to-python-for-data-science"
                        }
                    ],
                    'web development': [
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
                    'mobile apps': [
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
                    'artificial intelligence': [
                        {
                            "name": "Fast.ai - Practical Deep Learning",
                            "url": "https://www.fast.ai/"
                        },
                        {
                            "name": "Coursera Machine Learning Specialization",
                            "url": "https://www.coursera.org/specializations/machine-learning-introduction"
                        },
                        {
                            "name": "DeepLearning.AI",
                            "url": "https://www.deeplearning.ai/"
                        },
                        {
                            "name": "Google AI Education",
                            "url": "https://ai.google/education/"
                        }
                    ]
                }

                materials = materials_dict.get(interest.lower(), [])
                
                # Create course and enroll user
                print(f"Creating course for user {user_id}")  # Debug print
                course_id = self.lms.create_course(course_name, description, materials)
                
                if course_id:
                    print(f"Enrolling user {user_id} in course {course_id}")  # Debug print
                    self.lms.enroll_user(user_id, course_id)
                    
                    response = f"🎉 Welcome to {course_name}!\n\n"
                    response += "I've enrolled you in this course. Here are your learning materials:\n\n"
                    
                    for material in materials:
                        response += f"📚 {material['name']}\n"
                        response += f"   {material['url']}\n\n"
                    
                    response += "Type 'show my courses' anytime to see your enrolled courses!"
                else:
                    response = "I'm having trouble setting up your course. Please try again."
            
            except Exception as e:
                print(f"Error in course creation: {e}")  # Debug print
                response = "I encountered an error while setting up your course. Please try again."
        else:
            response = "Please provide both your experience level and coding interest. For example: 'I'm a beginner interested in data science'."

        dispatcher.utter_message(text=response)
        return [SlotSet("experience_level", experience), SlotSet("coding_interest", interest)]
class ActionShowEnrollments(Action):
    # Displays user's enrolled courses and their progress
    def __init__(self):
        super().__init__()
        self.lms = LMSManager()

    def name(self) -> Text:
        return "action_show_enrollments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            user_id = tracker.sender_id
            print(f"Checking enrollments for user: {user_id}")  # Debug print
            
            courses = self.lms.get_user_courses(user_id)
            print(f"Retrieved courses: {courses}")  # Debug print
            
            if courses:
                response = "Here are your enrolled courses:\n\n"
                for course in courses:
                    response += f"📚 {course['name']}\n"
                    response += f"Status: {course['status']}\n"
                    response += f"Enrolled: {course['enrolled_at'][:10]}\n\n"
            else:
                response = "You're not enrolled in any courses yet. Would you like some recommendations?"
            
            dispatcher.utter_message(text=response)
        except Exception as e:
            print(f"Error in ActionShowEnrollments: {e}")  # Debug print
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving your courses.")
        
        return []