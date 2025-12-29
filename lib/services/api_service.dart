import 'dart:convert';
import 'package:http/http.dart' as http;

// API base URL configuration:
// - Web/iOS Simulator: http://localhost:8000
// - Android Emulator: http://10.0.2.2:8000
// - Physical Device: http://YOUR_COMPUTER_IP:8000 (find IP with: ipconfig)
const String baseUrl = 'http://localhost:8000';

class ApiService {
  // Login API call
  static Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        try {
          final errorData = jsonDecode(response.body);
          if (errorData['message'] != null) {
            throw Exception(errorData['message']);
          } else {
            throw Exception('Login failed');
          }
        } catch (e) {
          throw Exception('Login failed');
        }
      }
    } on http.ClientException {
      throw Exception('Network error: Unable to reach server');
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  // Get all products
  static Future<List<Map<String, dynamic>>> getProducts() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/products'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<Map<String, dynamic>>.from(data['data']);
      } else {
        throw Exception('Failed to fetch products');
      }
    } on http.ClientException {
      throw Exception('Network error: Unable to reach server');
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  // Add new product
  static Future<Map<String, dynamic>> addProduct(String name, double price) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/products'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'name': name,
          'price': price,
        }),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 201) {
        return jsonDecode(response.body);
      } else {
        try {
          final errorData = jsonDecode(response.body);
          if (errorData['message'] != null) {
            throw Exception(errorData['message']);
          } else {
            throw Exception('Failed to add product');
          }
        } catch (e) {
          throw Exception('Failed to add product');
        }
      }
    } on http.ClientException {
      throw Exception('Network error: Unable to reach server');
    } catch (e) {
      throw Exception(e.toString());
    }
  }
}

