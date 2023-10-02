module load cuda gcc python/3.8

python -m venv logic
source logic/bin/activate
pip install python-sat
pip install scipy
pip install xlsxwriter
pip install openpyxl

