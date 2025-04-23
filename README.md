# 🛒 Kenya Food Price Tracker 

A smart, web-scraped food price monitoring and SMS-based comparison service that helps Kenyans make cost-effective grocery decisions across major supermarket chains.

---

## Project Overview

This platform provides up-to-date pricing on fresh produce and general food items (e.g., maize flour, rice, cooking oil) scraped from leading Kenyan supermarkets. Users receive alerts, compare prices, and subscribe to premium plans for specialized services such as promotions or targeted alerts.

---

## Objectives

1. **Scrape** food prices from:
   - Naivas
   - Carrefour
   - QuickMart

2. **Store scraped data** into a database with timestamps for future trend analysis.

3. **Create user accounts** with:
   - Free plans (limited access)
   - Premium plans:
     - Full market comparison
     - Promo and deal alerts
     - SMS notifications

4. **Integrate M-PESA payments (via KCB BUNI API)**:
   - Users pay to activate premium services
   - System tracks token validity and sends expiry reminders via SMS

5. **Compare prices** for key items across supermarkets and regions in real-time.

6. **Enable two-way SMS communication**:
   - Users can request prices or submit crowdsourced data
   - Bot replies with relevant info or logs new data

7. **(Optional)** Analyze weekly/monthly price trends using:
   - `pandas` for data manipulation
   - `matplotlib` for visualizations

8. **(Optional)** Deploy the app on a cloud platform such as:
   - Heroku
   - Google App Engine
   - Azure App Service
   - DigitalOcean App Platform

---

## Tech Stack

- **Backend**: Python
- **Scraping**: Selinium
- **Database**: MongoDB 
- **Payments**: M-PESA via KCB BUNI API
- **SMS**: Africa's Talking API (sandbox)
- **Data Analysis**: Pandas, Matplotlib
- **Deployment**: Heroku / DigitalOcean / GCP / Azure

---

## Impact

- Empowers Kenyans with **price transparency**
- Promotes **consumer savings**
- Supports **SMEs and families** in budgeting
- Opens up **data for research and policy analysis**

---

## Expected Deliverables

- User onboarding and token management
- Scraper services with automatic scheduling
- Premium service access control
- Visual reports for pricing trends (optional)
- Live cloud deployment with SSL (optional)

---

## 📅 Timeline (optional Tasks)
> The optional Tasks and deliverables depend on the time I will have to spare
---

## 📝 License

This project may be released as MIT-license and will be developed further for commercialization and scaling.




