# IBMeal – Institution-Based Meal Ordering System  

## Overview  
IBMeal is a **Telegram-based meal ordering platform** that provides institutional workers, students, and hospital staff with instant access to **healthy and affordable meals**.  

## Features  
- **AI-Powered Meal Recommendations** – Uses **GPT-4o** to process user queries and suggest suitable meals.  
- **Seamless Ordering Process** – Users select meals from a categorized menu or enter custom dietary requests.  
- **Order Number System** – Ensures accuracy and efficiency in meal delivery.  
- **Integrated Payment System** – Users can fund their accounts via **Flask API** or manually through the admin panel.  
- **Dispatch System** – Riders receive orders, verify order numbers, and deliver meals.  

Here is a link to the slide deck: [View Slide Deck](https://docs.google.com/presentation/d/1X02nVwF5IqeThPnMOuYzv_jjisxALgRYAh2ax-qt25s/edit?usp=sharing)

## System Flow  
```plaintext
                   +----------------------+
                   |    Telegram Bot UI   |
                   +-----------+----------+
                               |
                               v
                   +-----------+----------+
                   |  Query Processing    |
                   |      (GPT-4o)        |
                   +-----------+----------+
                               |
                               v
    +------------------------------------------------------+
    |  Returns:                                            |
    |    • Meal                                            |
    |    • Price                                           |
    |                                                      |
    +------------------------------------------------------+
                               |
                               v
                   +----------------------+
                   | User Receives Order # |
                   +----------------------+
                               |
                               v
                   +----------------------+
                   | Dispatch Riders Deliver |
                   | Meal Based on Order #  |
                   +----------------------+
```

## How to Set Up  

### 1. Clone the Repository  
```bash
git clone https://github.com/jeeryblessed/ibmeal.git
cd ibmeal
```

### 2. Start the Bot  
```bash
python core.py
```

### 3. Funding User Accounts  
Users can **fund their accounts** by:  
1. **Running Flask API for Payment Processing**  
   - Navigate to the payment directory:  
     ```bash
     cd pay_flask
     ```
   - Start the Flask server:  
     ```bash
     flask run
     ```
   - Replace the payment URL inside the `def __admin_menu(self):` function in `worker.py`.  

2. **Manually via the Admin Panel**  
   - Admins can add balance directly from the bot’s admin site.  

3. **Directly in the SQLite Database**  
   - Users can update the balance manually in the database if needed.  

## GPT-4o Model Integration  
The **GPT-4o model** is used in `worker.py` for query processing.  

**Code Reference:**  
```python
def __order_menu(self):
    """User menu to order products from the shop."""
    log.debug("Displaying __order_menu")
```

## Acknowledgments  
This project is built on top of **[Telegram-Shop-Greed](https://github.com/givecodeme/Telegram-Shop-Greed)**. Credit goes to the original contributors.  

## License  
This project is open-source and available for contributions! 🚀  
