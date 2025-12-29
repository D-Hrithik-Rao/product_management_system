# Product Management System

A complete full-stack product management application with FastAPI backend and Flutter mobile app.

## Project Overview

This system consists of:
- **Backend**: FastAPI REST API with MongoDB database
- **Mobile App**: Flutter Material UI application with three screens (Login, Product List, Add Product)

## Tech Stack

### Backend
- Python 3.8+
- FastAPI
- MongoDB (Official Python driver)
- Pydantic for data validation

### Mobile
- Flutter (Material UI)
- http package for API calls

## Project Structure

```
product_management_system/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── lib/
│   ├── main.dart            # Flutter app entry point
│   ├── screens/
│   │   ├── login_screen.dart
│   │   ├── product_list_screen.dart
│   │   └── add_product_screen.dart
│   └── services/
│       └── api_service.dart # API service layer
└── README.md
```

## Backend Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB installed and running locally, or MongoDB Atlas account

### Installation Steps

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Create a `.env` file in the `backend` directory
   - Copy from `.env.example` and update MongoDB URL if needed:
     ```
     MONGODB_URL=mongodb://localhost:27017/
     ```
   - For MongoDB Atlas, use:
     ```
     MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
     ```

5. **Start MongoDB (if running locally):**
   ```bash
   # Windows
   mongod
   
   # macOS (if installed via Homebrew)
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

6. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: `http://localhost:8000`

7. **Verify the server is running:**
   - Open browser: `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`

## MongoDB Setup

### Database Configuration
- **Database Name**: `productdb`
- **Collection**: `products`
- **Fields**:
  - `name` (string)
  - `price` (number)
  - `createdAt` (date)

The database and collection will be created automatically when the first product is added.

### MongoDB Installation

**Windows:**
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Install and start MongoDB service

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install mongodb
sudo systemctl start mongod
```

## API Endpoints

### 1. POST /api/login
Login with hardcoded credentials.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

### 2. GET /api/products
Get all products.

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "string",
      "name": "Laptop",
      "price": 75000
    }
  ]
}
```

### 3. POST /api/products
Add a new product.

**Request:**
```json
{
  "name": "Wireless Mouse",
  "price": 799
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Product added successfully"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "Invalid product data"
}
```

## Flutter App Setup

### Prerequisites
- Flutter SDK installed
- Android Studio / VS Code with Flutter extensions
- Android emulator or physical device

### Installation Steps

1. **Install dependencies:**
   ```bash
   flutter pub get
   ```

2. **Configure API URL:**
   - Open `lib/services/api_service.dart`
   - Update `baseUrl` based on your setup:
     - **Local development**: `http://localhost:8000`
     - **Android Emulator**: `http://10.0.2.2:8000`
     - **iOS Simulator**: `http://localhost:8000`
     - **Physical Device**: `http://YOUR_COMPUTER_IP:8000`

3. **Run the app:**
   ```bash
   flutter run
   ```

### Android Emulator Note

**Important**: When using Android emulator, change the API base URL to:
```dart
const String baseUrl = 'http://10.0.2.2:8000';
```

The `10.0.2.2` address is a special alias to your host machine's localhost from the Android emulator.

## App Features

### Screen 1: Login Screen
- Email and password input fields
- Form validation (email format, password length)
- Loading indicator during authentication
- Error handling with Snackbar messages
- Navigates to Product List on successful login

**Valid Credentials:**
- Email: `user@example.com`
- Password: `Password123`

### Screen 2: Product List Screen
- Displays all products in a scrollable list
- Product name (bold) and price
- Pull-to-refresh functionality
- Empty state message when no products exist
- FloatingActionButton to add new products
- Loading and error states

### Screen 3: Add Product Screen
- Product name input field
- Price input field (numeric keyboard)
- Form validation (name required, price > 0)
- Loading indicator during submission
- Success/error Snackbar messages
- Auto-refreshes product list after successful addition

## Error Handling

### Mobile App
- Network connectivity errors
- Server unreachable scenarios
- API failure responses
- Form validation errors
- User-friendly error messages via Snackbars

### Backend
- Missing required fields validation
- Invalid data type handling
- Database connection errors
- Proper HTTP status codes (200, 201, 400, 401, 500)

## Testing the Application

1. **Start Backend:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start MongoDB** (if running locally)

3. **Run Flutter App:**
   ```bash
   flutter run
   ```

4. **Test Flow:**
   - Login with `user@example.com` / `Password123`
   - View empty product list
   - Add a product using the FAB button
   - Verify product appears in the list
   - Add more products to test the list

## Troubleshooting

### Backend Issues
- **MongoDB Connection Error**: Ensure MongoDB is running and URL is correct
- **Port Already in Use**: Change port in uvicorn command or stop conflicting service
- **Module Not Found**: Ensure virtual environment is activated and dependencies are installed

### Flutter Issues
- **Network Error**: Verify backend is running and API URL is correct
- **Android Emulator Connection**: Use `http://10.0.2.2:8000` instead of `localhost`
- **Build Errors**: Run `flutter clean` and `flutter pub get`

## Development Notes

- Clean folder structure with separation of concerns
- Readable variable names and code comments
- Consistent error handling patterns
- Material Design UI components
- Proper async/await handling
- No dead code or unused imports

## License

This project is created for technical evaluation purposes.
