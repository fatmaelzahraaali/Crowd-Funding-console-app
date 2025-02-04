import re 
import pickle
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, password ,phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.projects = []  # This is where projects are stored for the user
    
    
#project info 
class Project:
    def __init__(self, title, details, target, start_date, end_date):
        self.title = title
        self.details = details
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
    
    @staticmethod
    def validate_date(date_string):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
class Authentication:
    def __init__(self,filename="users.pkl",project_file='project.pkl'):
        self.users = {} #dict to store users with email as a key
        self.filename = filename
        self.project_file = project_file
        self.users = self.load_users()
    ############## save and load users ###############
    def save_users(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.users, file)

    def load_users(self):
        try:
            with open(self.filename, "rb") as file:
                users = pickle.load(file)
                for user in users.values():
                    if not hasattr(user, 'projects'):
                        user.projects = []  # Ensure 'projects' attribute exists
                return users
        except (FileNotFoundError, EOFError):
            return {}
        
    ############## save and load projects #################    
    def save_projects(self):
        with open(self.project_file, "wb") as file:
            pickle.dump([user.projects for user in self.users.values()], file)
    
    def load_projects(self):
        try:
            with open(self.project_file, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []
        
    ############### registeration ###############
    def register(self):
        print("Please provide the following details to register:")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        password = input("Password: ")
        confirm_password = input("Confirm Password: ")
        phone_number = input("Mobile Phone: ")

        if password != confirm_password:
            print("Passwords do not match!")
            return
        
        if not self.validate_phone(phone_number):
            print("Error: Invalid phone number format!")
            return False
        
        if not self.validate_email(email):
            print("Error: Invalid email format!")
            return False
        
        user = User(first_name,last_name,email,password,phone_number)
        self.users[email]=user
        self.save_users()
        print("User registered successfully!")
        return True
    
    @staticmethod
    def validate_email(email):
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    
    @staticmethod
    def validate_phone(phone):
        return re.match(r'^(010|011|012|015)\d{8}$', phone)
   ################ login #################
    def login(self,email):

        password = input("Password: ")
        if email in self.users:
            user = self.users[email]
            if user.password == password:
                print("Login successful!")
                return True
            else:
                print("Incorrect password!")
                return False
        else:
            print("User not found!")
            return False

    ################ create project #################
    def create_project(self, email):
        user = self.users[email]
        print("\nCreate a new fundraising project!")
        title = input("Project Title: ")
        details = input("Project Details: ")
        target = float(input("Target Amount (EGP): "))
        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")

        if not Project.validate_date(start_date):
            print("Invalid start date format!")
            return
        
        if not Project.validate_date(end_date):
            print("Invalid end date format!")
            return
        
        project = Project(title, details, target, start_date, end_date)
        user.projects.append(project)
        self.save_projects()  # Save updates to file

        print("Project created successfully!")    
    ############## View Projects #############
    def view_projects(self, email):
        self.load_projects() 
        user = self.users[email]
        if user.projects:
            print("\nYour Projects:")
            for i , project in enumerate(user.projects):
                print(f"{i+1}. {project.title} | Target: {project.target} EGP | Start: {project.start_date} | End: {project.end_date}")
        else:
            print("You have no projects yet!")

    ############## edit project #############
    def edit_project(self, email):
        user = self.users[email]
        if not user.projects:
            print("You have no projects to edit!")
            return
        
        self.view_projects(email)
        project_num = int(input("\nEnter project number to edit: ")) - 1
        
        if project_num < 0 or project_num >= len(user.projects):
            print("Invalid project number!")
            return
        
        project = user.projects[project_num]
        title = input(f"New Title (Current: {project.title}): ") or project.title
        details = input(f"New Details (Current: {project.details}): ") or project.details
        target = float(input(f"New Target Amount (Current: {project.target}): ") or project.target)
        start_date = input(f"New Start Date (Current: {project.start_date}): ") or project.start_date
        end_date = input(f"New End Date (Current: {project.end_date}): ") or project.end_date
        
        if not Project.validate_date(start_date):
            print("Invalid start date format!")
            return
        
        if not Project.validate_date(end_date):
            print("Invalid end date format!")
            return
        
        project.title = title
        project.details = details
        project.target = target
        project.start_date = start_date
        project.end_date = end_date
        self.save_projects()
        print("Project updated successfully!")
    ######### main menu ########
    def start(self):
        while True:
            print("\n1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                if self.register():
                    break
            elif choice == '2':
                email = input("Enter your email to login: ")
                if self.login(email):
                    while True:
                        print("\n1. Create Project")
                        print("2. View Projects")
                        print("3. Edit Project")
                        print("4. Logout")
                        
                        option = input("Choose an option: ")
                        
                        if option == '1':
                            self.create_project(email)
                        elif option == '2':
                            self.view_projects(email)
                        elif option == '3':
                            self.edit_project(email)
                        elif option == '4':
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice!")
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid option! Please try again.")   
        
auth_sys=Authentication()
#auth_sys.register()
#auth_sys.login()
auth_sys.start()
