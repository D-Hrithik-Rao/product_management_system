# Quick Setup Guide

## Step 1: Backend Setup

1. **Navigate to backend folder:**
   ```powershell
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Make sure MongoDB is running:**
   - If you have MongoDB installed locally, start it
   - Or use MongoDB Atlas (cloud) and update the connection string

5. **Create .env file (optional):**
   - Create a `.env` file in the `backend` folder
   - Add: `MONGODB_URL=mongodb://localhost:27017/`
   - Or for MongoDB Atlas: `MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/`

6. **Start the backend server:**
   ```powershell
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   You should see: `Application startup complete` and `Uvicorn running on http://0.0.0.0:8000`

7. **Test the API:**
   - Open browser: http://localhost:8000/docs
   - You should see FastAPI interactive documentation

## Step 2: Flutter App Setup

1. **Open a NEW terminal/PowerShell window** (keep backend running)

2. **Navigate to project root:**
   ```powershell
   cd "D:\New folder\product_management_system"
   ```

3. **Install Flutter dependencies:**
   ```powershell
   flutter pub get
   ```

4. **Configure API URL for your device:**
   - Open `lib/services/api_service.dart`
   - Change `baseUrl` based on your setup:
     - **Android Emulator**: `const String baseUrl = 'http://10.0.2.2:8000';`
     - **iOS Simulator**: `const String baseUrl = 'http://localhost:8000';`
     - **Physical Device**: `const String baseUrl = 'http://YOUR_COMPUTER_IP:8000';`
       - Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
       - Look for IPv4 Address (e.g., 192.168.1.100)

5. **Run the Flutter app:**
   ```powershell
   flutter run
   ```

## Step 3: Test the Application

1. **Login Screen:**
   - Email: `user@example.com`
   - Password: `Password123`
   - Click Login

2. **Product List Screen:**
   - Should show empty state initially
   - Click the + button to add a product

3. **Add Product Screen:**
   - Enter product name (e.g., "Laptop")
   - Enter price (e.g., 75000)
   - Click "Add Product"
   - Should navigate back and show the product in the list

## Troubleshooting

### Backend won't start:
- Check if port 8000 is already in use
- Verify MongoDB is running
- Check Python version (need 3.8+)

### Flutter can't connect to backend:
- Make sure backend is running
- Check API URL in `api_service.dart`
- For Android emulator, use `10.0.2.2:8000`
- For physical device, use your computer's IP address

### MongoDB connection error:
- Verify MongoDB is running: `mongod` command
- Check connection string in `.env` file
- For MongoDB Atlas, ensure IP whitelist includes your IP

## Quick Commands Reference

**Backend:**
```powershell
cd backend
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Flutter:**
```powershell
flutter pub get
flutter run
```

**Check MongoDB (if installed locally):**
```powershell
mongod
```

