# 👚 ReWear – Community Clothing Exchange


---

## 📌 Table of Contents

- [📚 Overview](#-overview)
- [🌟 Features](#-key-features)
- [📂 Project Structure](#-project-structure)
<!-- - [⚙️ How to Use](#️-how-to-use)
- [🧾 Requirements](#-requirements)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📃 License](#-license) -->

---

# Overview: 
Develop ReWear, a web-based platform that enables users to exchange unused clothing 
through direct swaps or a point-based redemption system. The goal is to promote sustainable 
fashion and reduce textile waste by encouraging users to reuse wearable garments instead of 
discarding them. 

---

## 🌟 Key Features

### 🔐 User Authentication
- Email/password signup & login

### 🏠 Landing Page
- Short intro to the platform
- Buttons to:
  - Start Swapping
  - Browse Items
  - List an Item
- Featured items carousel

### 👤 User Dashboard
- View profile and points balance
- Track your uploaded items
- See ongoing and completed swaps

### 👗 Item Detail Page
- Image gallery with item description
- Uploader's basic info
- Options:
  - Request a Swap
  - Redeem via Points
- Availability status (Available / Swapped)

### ➕ Add New Item
- Upload images
- Fill in item title, description, category, type, size, condition, and tags
- Submit item for listing

### 🛠️ Admin Panel
- Approve or reject item listings
- Remove spam or inappropriate content
- Lightweight interface for admins to monitor listings

---

## 📂 Project Structure

```
ReWear/
│
├── Static/
│   └── Uploads/
│
├── templates/
│   ├── Base.html
│   ├── Login.html
|    ├── Sign.html
|    └── Navbar.html
│
├── Config.py
├── db_config.py
├── DATABASE.txt
├── app.py
├── README.md
└── requirements.txt
```

---

## 💡 Why ReWear?

Fast fashion is creating massive waste. Many of us have perfectly wearable clothes sitting in our wardrobes. ReWear gives these clothes a second life. Whether you're swapping with someone or using points to claim an item, you're helping reduce textile waste in a meaningful way.

---

## 🚀 Tech Stack (Example – Modify Based on Your Build)
Adding soon
---

## 🛠️ How to Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/rewear.git
cd rewear
