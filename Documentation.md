# File Storage Web Application - Documentation:

This documentation provides detailed information on the File Storage Web Application, which allows users to store files of any type and name, retrieve files by their versions, and implement a Content Addressable Storage mechanism. The application is composed of two components: the frontend built with React.js and the backend built with Django.

## Frontend:

The frontend of the application is built with React.js and provides a user interface for users to interact with the system. It includes the following features:

1. Login Form: Users can enter their email and password to log in to the application.
2. Dashboard: After successful login, users are redirected to the dashboard page, where they can choose to upload a file or retrieve files they have uploaded.
3. File Upload: Users can upload a file of any format from their system location. The frontend sends a POST request to the backend API endpoint "upload-file/" with the file_name and file_url data.
4. File Retrieval: Users can retrieve files they have uploaded by selecting a file from the dropdown. They can also choose a specific version of the file if available or directly click the "Retrieve" button to get the file location path.

## Backend:

The backend of the application is built with Django and provides the necessary API endpoints to handle file storage and retrieval. It includes the following APIs:

1. POST "/api/upload-file/": Allows users to upload a file and stores the file details in the FileVersion model. The API requires user authentication using a token.
2. GET "/api/get-unique-files/": Retrieves a list of unique file names uploaded by the logged-in user. The API requires user authentication using a token.
3. GET "/api/get-file-versions/": Retrieves a list of version numbers for a specific file uploaded by the user. The API requires user authentication using a token.
4. GET "/api/get-file-version/": Retrieves the file details for a specific version of a file. The API requires user authentication using a token.


# Setup and Running:

## Frontend

npm start

The frontend application will be accessible at http://localhost:3000/

## Backend: 

Create a superuser to access the Django admin panel and manage user details: python manage.py createsuperuser

Run the backend server:

pipenv run python manage.py runserver 0.0.0.0:8001

The backend will be accessible at http://localhost:8001/


# Improvements Required: 
1. Enhance security by implementing user authentication using Django's built-in authentication system or other secure methods like OAuth or JWT.
2. Implement proper error handling and validation in both frontend and backend to provide a more robust user experience.
3. Handle file size limitations, user permission management, and any other security concerns that may arise in a production environment.
4. Use a more robust database like PostgreSQL or MySQL for data storage in a production environment.
5. Implement file storage using a dedicated file storage service like AWS S3 or Google Cloud Storage for better scalability and security.
6. Provide a log-out option in the frontend for users to securely log out from the application.
7. Improve the UI to make user interactions more intuitive and user-friendly.
8. Most important, Unit testing can be improved to handle more scenarios.


# Conclusion: 

The File Storage Web Application is a basic yet functional system that allows users to store, retrieve, and manage files at specified URLs. With further improvements and enhancements, the application can be deployed for production use in a secure and scalable environment.