import os
import sys

from trade import db

def recreateDB():
  os.system("rm -rf trade/site.db")

  db.create_all()

if __name__ == "__main__":
  if sys.argv[1]:
    if sys.argv[1] == "-r" or sys.argv[1] == "--recreateDB":
      recreateDB()