import sys
print(sys.path)  # Print the current PYTHONPATH

from iebank_api import app

if __name__ == '__main__':
    app.run(debug=True)