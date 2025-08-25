# Django Auction Website

A web-based auction platform built using **Django** where users can create auction listings, 
place bids, add items to their watchlist, and post comments. The project includes user authentication, 
category filtering, and an admin interface for managing auctions.

---

## **Features**
- **User Authentication**
  - Register, login, and logout functionality
- **Auction Listings**
  - Create new listings with title, description, image, category, and starting bid
- **Bidding**
  - Users can place bids on active listings
- **Comments**
  - Add comments to listings
- **Watchlist**
  - Add or remove listings from your watchlist
- **Category Filtering**
  - Browse listings by category
- **Close Auction**
  - Owners can close auctions and declare the winner

---

## **Tech Stack**
- **Backend:** Django (Python)
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Django's built-in user authentication system

---

## **Models**
- **User:** Custom user model extending Django's `AbstractUser`
- **Category:** Stores categories for auction listings
- **Listing:** Stores auction details including title, description, image, price, category, owner, and watchlist
- **Bid:** Represents user bids on listings
- **Comment:** Stores comments related to listings

---

## **Installation**

### **1. Clone the repository**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```
2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py makemigrations
python manage.py migrate

5. Create a superuser (for admin panel)
python manage.py createsuperuser


6. Run the development server
python manage.py runserver
