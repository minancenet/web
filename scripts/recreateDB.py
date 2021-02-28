import sys

from minance import db, create_app

def recreateDB():
  app = create_app()
  with app.app_context():
    db.create_all()

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == "-r" or sys.argv[1] == "--recreateDB":
      recreateDB()
      print("DB recreated.")
  else:
    print("No args presented.")