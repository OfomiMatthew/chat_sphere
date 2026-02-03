"""
Database migration script to add call_duration and call_status columns to Message table
"""
from app import create_app, db
from sqlalchemy import text

def update_database():
    app = create_app()
    with app.app_context():
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('message')]
            
            with db.engine.connect() as conn:
                if 'call_duration' not in columns:
                    print("Adding call_duration column...")
                    conn.execute(text('ALTER TABLE message ADD COLUMN call_duration INTEGER'))
                    conn.commit()
                    print("✓ call_duration column added")
                else:
                    print("✓ call_duration column already exists")
                
                if 'call_status' not in columns:
                    print("Adding call_status column...")
                    conn.execute(text('ALTER TABLE message ADD COLUMN call_status VARCHAR(20)'))
                    conn.commit()
                    print("✓ call_status column added")
                else:
                    print("✓ call_status column already exists")
            
            print("\n✅ Database updated successfully!")
            
        except Exception as e:
            print(f"\n❌ Error updating database: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    print("Updating database schema...")
    print("-" * 50)
    update_database()
