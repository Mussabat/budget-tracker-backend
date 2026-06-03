from app.database import SessionLocal
from app.models.models import Category, Subcategory

def seed_data():
    db = SessionLocal()

    # Check if already seeded
    if db.query(Category).first():
        print("Database already seeded")
        db.close()
        return

    # Create categories
    categories = [
        Category(name="Food", budget_limit=0.0),
        Category(name="Bills", budget_limit=0.0),
        Category(name="Travel", budget_limit=0.0),
        Category(name="Toiletries", budget_limit=0.0),
    ]

    db.add_all(categories)
    db.commit()

    # Refresh to get IDs
    for category in categories:
        db.refresh(category)

    # Create subcategories
    subcategories = [
        # Food
        Subcategory(name="Rice", category_id=categories[0].id),
        Subcategory(name="Lentil", category_id=categories[0].id),
        Subcategory(name="Oil", category_id=categories[0].id),
        Subcategory(name="Spices", category_id=categories[0].id),
        Subcategory(name="Flour", category_id=categories[0].id),
        Subcategory(name="Sugar", category_id=categories[0].id),
        Subcategory(name="Salt", category_id=categories[0].id),
        Subcategory(name="Onion", category_id=categories[0].id),
        Subcategory(name="Garlic", category_id=categories[0].id),
        Subcategory(name="Ginger", category_id=categories[0].id),
        Subcategory(name="Garlic Ginger Paste", category_id=categories[0].id),
        Subcategory(name="Chili", category_id=categories[0].id),
        Subcategory(name="Ruti", category_id=categories[0].id),
        Subcategory(name="Sauce", category_id=categories[0].id),
        Subcategory(name="Masturd Oil", category_id=categories[0].id),
        Subcategory(name="Vegetables", category_id=categories[0].id),
        Subcategory(name="Fruits", category_id=categories[0].id),
        Subcategory(name="Beef", category_id=categories[0].id),
        Subcategory(name="Chicken", category_id=categories[0].id),
        Subcategory(name="Hilsha", category_id=categories[0].id),
        Subcategory(name="Egg", category_id=categories[0].id),
        Subcategory(name="Srimp", category_id=categories[0].id),
        Subcategory(name="Butter", category_id=categories[0].id),
        Subcategory(name="Milk", category_id=categories[0].id),
        Subcategory(name="Yogurt", category_id=categories[0].id),
        Subcategory(name="Cheese", category_id=categories[0].id),
        Subcategory(name="Noodles", category_id=categories[0].id),
        Subcategory(name="Snacks", category_id=categories[0].id),
        Subcategory(name="Other", category_id=categories[0].id),

        # Bills
        Subcategory(name="Electricity", category_id=categories[1].id),
        Subcategory(name="Council Tax", category_id=categories[1].id),
        Subcategory(name="Rent", category_id=categories[1].id),
        Subcategory(name="Internet", category_id=categories[1].id),
        Subcategory(name="Water", category_id=categories[1].id),
        Subcategory(name="Heating", category_id=categories[1].id),
        Subcategory(name="Other", category_id=categories[1].id),

        # Travel
        Subcategory(name="Tarin", category_id=categories[2].id),
        Subcategory(name="Bus", category_id=categories[2].id),
        Subcategory(name="Uber", category_id=categories[2].id),
        Subcategory(name="Other", category_id=categories[2].id),

        # Toiletries
        Subcategory(name="Bathgel", category_id=categories[3].id),
        Subcategory(name="Razor", category_id=categories[3].id),
        Subcategory(name="Toothpaste", category_id=categories[3].id),
        Subcategory(name="Shampoo", category_id=categories[3].id),
        Subcategory(name="Tissue", category_id=categories[3].id),
        Subcategory(name="Medicine", category_id=categories[3].id),
        Subcategory(name="dishwasher Tablet", category_id=categories[3].id),
        Subcategory(name="Diswasher Liquid", category_id=categories[3].id),
        Subcategory(name="Scrubber", category_id=categories[3].id),
        Subcategory(name="Other", category_id=categories[3].id),
    ]

    db.add_all(subcategories)
    db.commit()
    db.close()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()