Gold Store Management System
A comprehensive Django REST API backend system for managing a gold trading platform with multiple user types and transaction capabilities.

📋 Overview
This Gold Store Management System is a backend API built with Django REST Framework that facilitates gold trading between manufacturers, retailers, and customers. The system supports user authentication, product management, inventory tracking, and transaction processing.

🏗️ System Architecture
User Types
User: Basic customer account
Retail: Shop owners who can buy from manufacturers and sell to customers
Manufacturers: Gold manufacturers who create and sell products
Core Features
User authentication with JWT tokens
Product creation and management
Inventory tracking
Transaction history
Multi-level trading system (Manufactory → Retail → Customer)
Balance management and deposits

🛠️ Technology Stack
Backend: Django REST Framework
Database: MongoDB Atlas
Authentication: JWT
Password Hashing: SHA256
API: RESTful architecture
